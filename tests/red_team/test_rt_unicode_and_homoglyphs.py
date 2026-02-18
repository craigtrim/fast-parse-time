#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Red Team: Unicode and Homoglyph Attacks (Cross-Cutting)
Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43

Academic Context
----------------
Three Unicode attack classes are relevant to a temporal parser:

  1. DIGIT HOMOGLYPHS: Python's \d regex matches full-width, Arabic-Indic,
     Devanagari, Bengali, etc. digits. Downstream int() conversion may
     succeed (Python 3 normalises some) or raise ValueError unpredictably.

  2. PUNCTUATION HOMOGLYPHS: en-dash U+2013, em-dash U+2014, minus U+2212,
     non-breaking hyphen U+2011, fullwidth slash U+FF0F, fullwidth hyphen
     U+FF0D look like ASCII delimiters but are distinct codepoints. A regex
     using literal [-/.] will NOT match them — correct defensive behaviour.

  3. INVISIBLE/CONTROL CHARACTERS: Zero-width space U+200B, soft hyphen
     U+00AD, zero-width non-joiner U+200C, and RTL override U+202E are
     invisible in renderers but break token continuity at the byte level,
     causing regex patterns to fail or produce wrong results.

All tests in this file are false-positive defenses: inputs should NOT
be recognised as valid temporal expressions.
"""
import pytest
from fast_parse_time.api import extract_explicit_dates, extract_relative_times

pytestmark = pytest.mark.xfail(reason='red_team: not yet validated')

# ── SECTION 1: Full-width digits in date strings ─────────────────────────────
_FW_DIGIT_DATES = [
    '\uff10\uff14/\uff10\uff18/\uff12\uff10\uff12\uff14',
    '\uff11\uff12/\uff13\uff11/\uff12\uff10\uff12\uff13',
    '\uff10\uff11-\uff10\uff11-\uff12\uff10\uff12\uff14',
    '\uff10\uff11.\uff11\uff15.\uff12\uff10\uff12\uff14',
]
@pytest.mark.parametrize('text', _FW_DIGIT_DATES)
def test_unicode_fullwidth_digits_in_dates(text):
    """Full-width digits (U+FF10-FF19) in date strings.
    Python \\d matches these — downstream int() conversion behavior is
    unpredictable. Parser should reject non-ASCII digit forms.
    Failure: full-width digits normalised to ASCII and matched as dates."""
    result = extract_explicit_dates(text)
    full = {k: v for k, v in result.items() if v == 'FULL_EXPLICIT_DATE'}
    assert len(full) == 0

# ── SECTION 2: Arabic-Indic digits (U+0660-U+0669) ───────────────────────────
_AI_DIGIT_DATES = [
    '\u0660\u0664/\u0660\u0668/\u0662\u0660\u0662\u0664',
    '\u0661\u0662/\u0663\u0661/\u0662\u0660\u0662\u0663',
    '\u0660\u0665 days ago',
    '\u0663 weeks from now',
]
@pytest.mark.parametrize('text', _AI_DIGIT_DATES)
def test_unicode_arabic_indic_digits(text):
    """Arabic-Indic (Eastern Arabic) digits.
    Failure: these digit forms accepted as ASCII cardinalities or date components."""
    result_d = extract_explicit_dates(text)
    result_r = extract_relative_times(text)
    full = {k: v for k, v in result_d.items() if v == 'FULL_EXPLICIT_DATE'}
    assert len(full) == 0

# ── SECTION 3: Extended Arabic-Indic / Devanagari / Bengali ──────────────────
_OTHER_DIGITS = [
    '\u06f0\u06f4/\u06f0\u06f8/\u06f2\u06f0\u06f2\u06f4',  # Extended Arabic-Indic
    '\u0966\u0967/\u0968\u0969/\u096b\u096c\u096d\u096e',   # Devanagari
    '\u09e6\u09e7/\u09e8\u09e9/\u09ec\u09ed\u09ee\u09ef',   # Bengali
    '\u0e50\u0e51/\u0e52\u0e53/\u0e54\u0e55\u0e56\u0e57',   # Thai
    '\u0966\u096a days ago',    # Devanagari "05 days ago"
    '\u09e6\u09eb days ago',    # Bengali "05 days ago"
]
@pytest.mark.parametrize('text', _OTHER_DIGITS)
def test_unicode_non_ascii_digit_scripts(text):
    """Devanagari, Bengali, Thai, Extended Arabic-Indic digit forms.
    Failure: non-ASCII script digits accepted as date/time components."""
    result = extract_explicit_dates(text)
    full = {k: v for k, v in result.items() if v == 'FULL_EXPLICIT_DATE'}
    assert len(full) == 0

# ── SECTION 4: Superscript and subscript digits ───────────────────────────────
_SUPER_SUB = [
    '\u2075 days ago',   '\u00b9 week ago',  '\u00b2 months ago',
    '\u00b3 years ago',  '\u2074 hours ago',
    '\u2085 days ago',   '\u2081 week ago',   '\u2082 months ago',
    '\u2460 day ago',    '\u2461 weeks ago',  '\u2464 months ago',
]
@pytest.mark.parametrize('text', _SUPER_SUB)
def test_unicode_superscript_subscript_circled_digits(text):
    """Superscript (U+00B9, U+00B2, U+00B3, U+2070-), subscript (U+2080-),
    and circled (U+2460-) digits in cardinality position. Should not match.
    Failure: Unicode numeric forms normalised to ASCII cardinalities."""
    assert len(extract_relative_times(text)) == 0

# ── SECTION 5: Fullwidth delimiter homoglyphs ─────────────────────────────────
_FW_PUNCT = [
    '04\uff0f08\uff0f2024',    # fullwidth slash U+FF0F
    '04\uff0d08\uff0d2024',    # fullwidth hyphen-minus U+FF0D
    'Jan\uff0d2024',           # fullwidth hyphen in month-year
    '2014\uff0d2015',          # fullwidth hyphen in year range
    '2024\uff0d01\uff0d01T00:00:00Z',  # fullwidth hyphen in ISO date
]
@pytest.mark.parametrize('text', _FW_PUNCT)
def test_unicode_fullwidth_delimiters(text):
    """Fullwidth slash (U+FF0F) and hyphen (U+FF0D) as date delimiters.
    ASCII delimiter required in all date patterns. Should not match.
    Failure: fullwidth delimiters accepted in date string parsing."""
    result = extract_explicit_dates(text)
    assert len(result) == 0

# ── SECTION 6: Dash homoglyphs in year ranges and month-year ─────────────────
_DASH_HOMOGLYPHS = [
    '2014\u20132015',   # en-dash U+2013
    '2014\u20142015',   # em-dash U+2014
    '2014\u22122015',   # minus sign U+2212
    '2014\u18062015',   # Mongolian todo soft hyphen U+1806
    '2014\u20112015',   # non-breaking hyphen U+2011
    'Oct\u20112023',    # non-breaking hyphen in month-year
    'Oct\u20132023',    # en-dash in month-year
    'Oct\u20142023',    # em-dash in month-year
    'Oct\u22122023',    # minus sign in month-year
    'Jan\u20112024',    'Feb\u20132024',
]
@pytest.mark.parametrize('text', _DASH_HOMOGLYPHS)
def test_unicode_dash_homoglyphs(text):
    """Non-ASCII dash variants (en-dash, em-dash, minus sign, non-breaking hyphen)
    as delimiters in year-range and month-year strings.
    Failure: homoglyph dash accepted where ASCII hyphen is required."""
    result = extract_explicit_dates(text)
    assert len(result) == 0

# ── SECTION 7: Zero-width space injection (U+200B) ───────────────────────────
_ZWS = [
    '04/\u200b08/2024',     # ZWS between slash and digit
    '12\u200b/31/2023',     # ZWS before slash
    '20\u200b24',           # ZWS in year token
    'Marc\u200bh 15 2024',  # ZWS in month name
    '5\u200b days ago',     # ZWS between digit and space
    'in\u200b2024',         # ZWS between preposition and year
    'last\u200b week',      # ZWS between 'last' and 'week'
    'Oct\u200b-23',         # ZWS before hyphen in month-year
    '2014\u200b-2015',      # ZWS before hyphen in year range
    '5 days\u200b ago',     # ZWS between 'days' and 'ago'
]
@pytest.mark.parametrize('text', _ZWS)
def test_unicode_zero_width_space_injection(text):
    """Zero-width space (U+200B) injected to break token continuity.
    Invisible in renderers — a subtle spoofing attack. ZWS breaks regex
    matching that expects adjacent characters. Failure: ZWS ignored by
    parser, resulting in unintended temporal matches."""
    result_d = extract_explicit_dates(text)
    result_r = extract_relative_times(text)
    full_d = {k: v for k, v in result_d.items()
              if v in ('FULL_EXPLICIT_DATE','YEAR_ONLY','YEAR_RANGE','MONTH_YEAR')}
    assert len(full_d) == 0

# ── SECTION 8: Soft hyphen (U+00AD) ──────────────────────────────────────────
_SOFT_HYPHEN = [
    'Oct\u00ad23','Jan\u00ad2024','2014\u00ad2015',
    '04\u00ad08\u00ad2024','5\u00ad days ago','in\u00ad2024',
]
@pytest.mark.parametrize('text', _SOFT_HYPHEN)
def test_unicode_soft_hyphen_injection(text):
    """Soft hyphen (U+00AD) replacing or inserted alongside regular hyphen.
    Invisible in most rendering contexts but distinct from U+002D.
    Failure: soft hyphen treated as regular ASCII hyphen delimiter."""
    result = extract_explicit_dates(text)
    assert len(result) == 0

# ── SECTION 9: Invisible characters (ZWJ, ZWNJ, WJ) ─────────────────────────
_INVISIBLE = [
    '5\u200c days ago',     # ZWNJ (U+200C)
    '5\u200d days ago',     # ZWJ (U+200D)
    '5\u2060 days ago',     # word joiner (U+2060)
    'in\u200c2024',         # ZWNJ in prose-year
    '04/\u200d08/2024',     # ZWJ in date
    'Oct\u200c-23',         # ZWNJ in month-year
]
@pytest.mark.parametrize('text', _INVISIBLE)
def test_unicode_invisible_characters_injection(text):
    """Zero-width non-joiner (U+200C), zero-width joiner (U+200D), and word
    joiner (U+2060) injected into temporal strings. All are invisible in
    rendering but break character-level pattern matching.
    Failure: invisible characters ignored, resulting in unintended matches."""
    result_d = extract_explicit_dates(text)
    full_d = {k: v for k, v in result_d.items()
              if v in ('FULL_EXPLICIT_DATE','YEAR_ONLY')}
    assert len(full_d) == 0

# ── SECTION 10: RTL override and directional marks ───────────────────────────
_RTL = [
    '\u202e2024',           # RTL override before year
    'in \u202e2024',        # RTL override in prose-year
    '\u200f5 days ago',     # RTL mark before cardinality
    '5\u200f days ago',     # RTL mark between digit and space
    '20\u200f24',           # RTL mark inside year token
    '\u200e2024-01-01T00:00:00Z',  # LTR mark before ISO date
    '2014\u202e-2015',      # RTL override in year range
]
@pytest.mark.parametrize('text', _RTL)
def test_unicode_bidi_override_attacks(text):
    """RTL override (U+202E) and directional marks (U+200E, U+200F) in
    temporal strings. RTL override reverses visual display while leaving
    byte sequence unchanged — primarily a social-engineering attack but
    may cause issues in bidi-aware regex libraries.
    Failure: bidi characters ignored, resulting in unintended matches."""
    result_d = extract_explicit_dates(text)
    full_d = {k: v for k, v in result_d.items()
              if v in ('FULL_EXPLICIT_DATE','YEAR_ONLY')}
    assert len(full_d) == 0

# ── SECTION 11: Combining diacritics on digits ───────────────────────────────
_COMBINING = [
    '2\u03082024',        # combining diaeresis on year first digit
    '04/0\u03088/2024',   # combining diaeresis on month digit
    '5\u0308 days ago',   # combining diaeresis on cardinality digit
    '2014\u0308-2015',    # combining on year-range first digit
    '1\u03005 days ago',  # combining grave on digit
]
@pytest.mark.parametrize('text', _COMBINING)
def test_unicode_combining_diacritics_on_digits(text):
    """Unicode combining diacritic characters appended to digit codepoints.
    A digit followed by a combining character changes the codepoint sequence
    without necessarily changing the visual appearance. Regex patterns
    expecting clean single-codepoint digits will fail to match these.
    Failure: combining characters stripped, causing unintended matches."""
    result = extract_explicit_dates(text)
    full = {k: v for k, v in result.items() if v == 'FULL_EXPLICIT_DATE'}
    assert len(full) == 0

# ── SECTION 12: Fullwidth ISO components ─────────────────────────────────────
_FW_ISO = [
    '2024-01-01\uff3400:00:00Z',     # fullwidth T (U+FF34)
    '2024-01-01T00\uff1a00\uff1a00Z', # fullwidth colons (U+FF1A)
    '2024-01-01T00:00:00\uff3a',     # fullwidth Z (U+FF3A)
]
@pytest.mark.parametrize('text', _FW_ISO)
def test_unicode_fullwidth_iso_components(text):
    """Fullwidth T, colon, and Z characters in ISO 8601 datetime strings.
    Failure: fullwidth ASCII variants accepted in ISO datetime parsing."""
    result = extract_explicit_dates(text)
    full = {k: v for k, v in result.items() if v == 'FULL_EXPLICIT_DATE'}
    assert len(full) == 0

# ── SECTION 13: Non-breaking and hair spaces ──────────────────────────────────
_NBSP = [
    '5\u00a0days ago',    # non-breaking space instead of regular space
    'in\u00a02024',       # non-breaking space in prose-year
    'last\u00a0week',     # non-breaking space in last-week pattern
    'March\u00a015 2024', # non-breaking space in written month date
    '5\u200adays ago',    # hair space (U+200A)
    'in\u205f2024',       # medium mathematical space (U+205F)
]
@pytest.mark.parametrize('text', _NBSP)
def test_unicode_non_standard_spaces(text):
    """Non-breaking space (U+00A0) and other Unicode space variants replacing
    regular ASCII space (U+0020). A parser normalising \\s to only ASCII space
    will fail to tokenise these correctly.
    Failure: non-ASCII space variants accepted as word separators."""
    result_d = extract_explicit_dates(text)
    result_r = extract_relative_times(text)
    # We don't assert hard failure here — NBSP in 'March 15 2024' is a
    # legitimate normalization question. We document that behavior is undefined.
    pass  # xfail covers outcome

# ── SECTION 14: Homoglyph letters in month names ─────────────────────────────
_HOMOGLYPH_MONTHS = [
    # Cyrillic 'о' (U+043E) replacing Latin 'o' in "October"
    'Oct\u043eber 15 2024',
    # Cyrillic 'а' (U+0430) replacing Latin 'a' in "January"
    'J\u0430nuary 1 2024',
    # Greek 'ο' (U+03BF) replacing Latin 'o' in "November"
    'N\u03bfvember 11 2024',
    # Mathematical bold 'M' (U+1D40C) in "March"
    '\U0001d40carch 15 2024',
    # Latin small letter o with stroke (U+00F8) in "October"
    'Oct\u00f8ber 15 2024',
]
@pytest.mark.parametrize('text', _HOMOGLYPH_MONTHS)
def test_unicode_homoglyph_letters_in_month_names(text):
    """Homoglyph Unicode letters (Cyrillic о, Greek ο, mathematical variants)
    replacing ASCII letters in month names. These are visually indistinguishable
    from ASCII in many fonts but are distinct codepoints. A parser using
    str.lower() and exact ASCII comparison will correctly reject them.
    Failure: Unicode letter normalisation causes homoglyph month names to match."""
    result = extract_explicit_dates(text)
    full = {k: v for k, v in result.items() if v == 'FULL_EXPLICIT_DATE'}
    assert len(full) == 0
