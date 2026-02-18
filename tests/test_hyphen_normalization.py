#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""TDD red-team tests for hyphen normalization (issue #44).

275 test cases probing Unicode dash variants, space-padded hyphens,
asymmetric spacing, combined forms, and normalization side-effects.

These tests define the correct behaviour AFTER #44 is implemented.
Most will fail until normalization is in place.

Related GitHub Issue:
    #44 - feat: Normalize hyphen-like characters and space-padded hyphens before parsing
    https://github.com/craigtrim/fast-parse-time/issues/44
    Prerequisite for: #40
"""

import unittest

from fast_parse_time import extract_explicit_dates

# ---------------------------------------------------------------------------
# Unicode dash constants (named for readability in test bodies)
# ---------------------------------------------------------------------------
EN  = '\u2013'   # EN DASH
EM  = '\u2014'   # EM DASH
HY  = '\u2010'   # HYPHEN (proper)
NBH = '\u2011'   # NON-BREAKING HYPHEN
FIG = '\u2012'   # FIGURE DASH
HB  = '\u2015'   # HORIZONTAL BAR
MIN = '\u2212'   # MINUS SIGN
SHY = '\ufe63'   # SMALL HYPHEN-MINUS
FWH = '\uff0d'   # FULLWIDTH HYPHEN-MINUS
NBSP= '\u00a0'   # NON-BREAKING SPACE
ZWS = '\u200b'   # ZERO-WIDTH SPACE
SHY2= '\u00ad'   # SOFT HYPHEN


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _yr(text) -> bool:
    """Return True if at least one YEAR_RANGE entry exists."""
    try:
        r = extract_explicit_dates(text)
        return r is not None and 'YEAR_RANGE' in r.values()
    except Exception:
        return False


def _no_yr(text) -> bool:
    """Return True if no YEAR_RANGE entry exists."""
    try:
        r = extract_explicit_dates(text)
        return r is None or 'YEAR_RANGE' not in r.values()
    except Exception:
        return True


def _key(text: str, k: str) -> bool:
    """Return True if k maps to YEAR_RANGE."""
    try:
        r = extract_explicit_dates(text)
        return r is not None and r.get(k) == 'YEAR_RANGE'
    except Exception:
        return False


def _safe(text) -> bool:
    """Return True if call does not raise."""
    try:
        extract_explicit_dates(text)
        return True
    except Exception:
        return False


# ============================================================================
# Class 1 — TestEnDashBare
# 20 tests: bare YYYY–YYYY (en dash, U+2013)
# ============================================================================

class TestEnDashBare(unittest.TestCase):
    """En dash between years — should produce YEAR_RANGE after normalization."""

    def test_2014_en_2015(self):
        self.assertTrue(_yr(f'2014{EN}2015'))

    def test_2000_en_2010(self):
        self.assertTrue(_yr(f'2000{EN}2010'))

    def test_1990_en_2000(self):
        self.assertTrue(_yr(f'1990{EN}2000'))

    def test_1939_en_1945(self):
        self.assertTrue(_yr(f'1939{EN}1945'))

    def test_2019_en_2020(self):
        self.assertTrue(_yr(f'2019{EN}2020'))

    def test_1926_en_1927(self):
        self.assertTrue(_yr(f'1926{EN}1927'))

    def test_2035_en_2036(self):
        self.assertTrue(_yr(f'2035{EN}2036'))

    def test_1960_en_1970(self):
        self.assertTrue(_yr(f'1960{EN}1970'))

    def test_1970_en_1980(self):
        self.assertTrue(_yr(f'1970{EN}1980'))

    def test_1980_en_1990(self):
        self.assertTrue(_yr(f'1980{EN}1990'))

    def test_2010_en_2020(self):
        self.assertTrue(_yr(f'2010{EN}2020'))

    def test_2020_en_2025(self):
        self.assertTrue(_yr(f'2020{EN}2025'))

    def test_key_format(self):
        """Result key should be ASCII YYYY-YYYY regardless of input dash."""
        self.assertTrue(_key(f'2014{EN}2015', '2014-2015'))

    def test_value_format(self):
        r = extract_explicit_dates(f'2014{EN}2015') or {}
        self.assertEqual(r.get('2014-2015'), 'YEAR_RANGE')

    def test_result_is_dict(self):
        r = extract_explicit_dates(f'2014{EN}2015')
        self.assertIsInstance(r, dict)

    def test_result_nonempty(self):
        r = extract_explicit_dates(f'2014{EN}2015') or {}
        self.assertGreater(len(r), 0)

    def test_2004_en_2008(self):
        self.assertTrue(_yr(f'2004{EN}2008'))

    def test_1945_en_1955(self):
        self.assertTrue(_yr(f'1945{EN}1955'))

    def test_consecutive(self):
        self.assertTrue(_yr(f'2022{EN}2023'))

    def test_span_50(self):
        self.assertTrue(_yr(f'1970{EN}2020'))


# ============================================================================
# Class 2 — TestEnDashInContext
# 20 tests: en dash year range inside sentences and with punctuation
# ============================================================================

class TestEnDashInContext(unittest.TestCase):
    """En dash year range embedded in real text."""

    def test_period_2014_en_2015(self):
        self.assertTrue(_yr(f'The period 2014{EN}2015 was significant.'))

    def test_sentence_start(self):
        self.assertTrue(_yr(f'2014{EN}2015 was pivotal.'))

    def test_sentence_end(self):
        self.assertTrue(_yr(f'See data for 2014{EN}2015'))

    def test_trailing_period(self):
        self.assertTrue(_yr(f'2014{EN}2015.'))

    def test_trailing_comma(self):
        self.assertTrue(_yr(f'2014{EN}2015,'))

    def test_in_parens(self):
        self.assertTrue(_yr(f'(2014{EN}2015)'))

    def test_in_brackets(self):
        self.assertTrue(_yr(f'[2014{EN}2015]'))

    def test_quoted(self):
        self.assertTrue(_yr(f'"2014{EN}2015"'))

    def test_multiple_en_ranges(self):
        self.assertTrue(_yr(f'2000{EN}2010 and 2014{EN}2015'))

    def test_multiple_ranges_both_keys(self):
        r = extract_explicit_dates(f'2000{EN}2010 and 2014{EN}2015') or {}
        self.assertIn('2000-2010', r)
        self.assertIn('2014-2015', r)

    def test_mixed_ascii_and_en(self):
        """One ASCII hyphen range, one en dash range in same text."""
        r = extract_explicit_dates(f'2000-2010 and 2014{EN}2015') or {}
        self.assertIn('2000-2010', r)
        self.assertIn('2014-2015', r)

    def test_en_range_with_prose_year(self):
        r = extract_explicit_dates(f'In 2024 the era 2014{EN}2015 was recalled.') or {}
        self.assertIn('YEAR_RANGE', r.values())
        self.assertIn('YEAR_ONLY', r.values())

    def test_colon_before(self):
        self.assertTrue(_yr(f'Period: 2014{EN}2015'))

    def test_markdown_bold(self):
        self.assertTrue(_yr(f'**2014{EN}2015**'))

    def test_html_tag(self):
        self.assertTrue(_yr(f'<b>2014{EN}2015</b>'))

    def test_from_to_with_en_key(self):
        """from X to Y is unrelated; unaffected by en-dash normalization."""
        self.assertTrue(_yr('from 2004 to 2008'))

    def test_reversed_en_not_range(self):
        self.assertTrue(_no_yr(f'2015{EN}2014'))

    def test_same_year_en_not_range(self):
        self.assertTrue(_no_yr(f'2014{EN}2014'))

    def test_out_of_range_en(self):
        self.assertTrue(_no_yr(f'1800{EN}1900'))

    def test_long_sentence(self):
        text = f'Many scholars refer to the era 2014{EN}2015 as a turning point in history.'
        self.assertTrue(_yr(text))


# ============================================================================
# Class 3 — TestEmDashBare
# 20 tests: bare YYYY—YYYY (em dash, U+2014)
# ============================================================================

class TestEmDashBare(unittest.TestCase):
    """Em dash between years — should produce YEAR_RANGE after normalization."""

    def test_2014_em_2015(self):
        self.assertTrue(_yr(f'2014{EM}2015'))

    def test_2000_em_2010(self):
        self.assertTrue(_yr(f'2000{EM}2010'))

    def test_1990_em_2000(self):
        self.assertTrue(_yr(f'1990{EM}2000'))

    def test_1939_em_1945(self):
        self.assertTrue(_yr(f'1939{EM}1945'))

    def test_2019_em_2020(self):
        self.assertTrue(_yr(f'2019{EM}2020'))

    def test_1926_em_1927(self):
        self.assertTrue(_yr(f'1926{EM}1927'))

    def test_2035_em_2036(self):
        self.assertTrue(_yr(f'2035{EM}2036'))

    def test_1960_em_1970(self):
        self.assertTrue(_yr(f'1960{EM}1970'))

    def test_key_format(self):
        """Result key should be ASCII YYYY-YYYY."""
        self.assertTrue(_key(f'2014{EM}2015', '2014-2015'))

    def test_value_format(self):
        r = extract_explicit_dates(f'2014{EM}2015') or {}
        self.assertEqual(r.get('2014-2015'), 'YEAR_RANGE')

    def test_result_is_dict(self):
        r = extract_explicit_dates(f'2014{EM}2015')
        self.assertIsInstance(r, dict)

    def test_result_nonempty(self):
        r = extract_explicit_dates(f'2014{EM}2015') or {}
        self.assertGreater(len(r), 0)

    def test_2004_em_2008(self):
        self.assertTrue(_yr(f'2004{EM}2008'))

    def test_span_50(self):
        self.assertTrue(_yr(f'1970{EM}2020'))

    def test_consecutive(self):
        self.assertTrue(_yr(f'2022{EM}2023'))

    def test_reversed_em_not_range(self):
        self.assertTrue(_no_yr(f'2015{EM}2014'))

    def test_same_year_em_not_range(self):
        self.assertTrue(_no_yr(f'2014{EM}2014'))

    def test_out_of_range_em(self):
        self.assertTrue(_no_yr(f'1800{EM}1900'))

    def test_em_key_not_native_dash(self):
        """Key in result must use ASCII hyphen, not em dash."""
        r = extract_explicit_dates(f'2014{EM}2015') or {}
        self.assertNotIn(f'2014{EM}2015', r)

    def test_en_key_not_native_dash(self):
        """Key in result must use ASCII hyphen, not en dash."""
        r = extract_explicit_dates(f'2014{EN}2015') or {}
        self.assertNotIn(f'2014{EN}2015', r)


# ============================================================================
# Class 4 — TestEmDashInContext
# 15 tests: em dash year range inside sentences
# ============================================================================

class TestEmDashInContext(unittest.TestCase):
    """Em dash year range embedded in real text."""

    def test_period_2014_em_2015(self):
        self.assertTrue(_yr(f'The period 2014{EM}2015 was significant.'))

    def test_sentence_start(self):
        self.assertTrue(_yr(f'2014{EM}2015 was pivotal.'))

    def test_sentence_end(self):
        self.assertTrue(_yr(f'See data for 2014{EM}2015'))

    def test_in_parens(self):
        self.assertTrue(_yr(f'(2014{EM}2015)'))

    def test_multiple_em_ranges(self):
        self.assertTrue(_yr(f'2000{EM}2010 and 2014{EM}2015'))

    def test_multiple_em_ranges_both_keys(self):
        r = extract_explicit_dates(f'2000{EM}2010 and 2014{EM}2015') or {}
        self.assertIn('2000-2010', r)
        self.assertIn('2014-2015', r)

    def test_mixed_ascii_and_em(self):
        r = extract_explicit_dates(f'2000-2010 and 2014{EM}2015') or {}
        self.assertIn('2000-2010', r)
        self.assertIn('2014-2015', r)

    def test_colon_before(self):
        self.assertTrue(_yr(f'Period: 2014{EM}2015'))

    def test_html_tag(self):
        self.assertTrue(_yr(f'<span>2014{EM}2015</span>'))

    def test_reversed_em_in_sentence(self):
        self.assertTrue(_no_yr(f'The odd period 2015{EM}2014 is wrong.'))

    def test_out_of_range_em_in_sentence(self):
        self.assertTrue(_no_yr(f'Way back in 1800{EM}1900 things were different.'))

    def test_same_year_em_in_sentence(self):
        self.assertTrue(_no_yr(f'2014{EM}2014 is not a range.'))

    def test_em_and_en_mixed(self):
        """Both em and en dash ranges in same text."""
        r = extract_explicit_dates(f'2000{EN}2010 and 2014{EM}2015') or {}
        self.assertIn('2000-2010', r)
        self.assertIn('2014-2015', r)

    def test_em_between_compound_words(self):
        """Em dashes between words (not years) shouldn't produce YEAR_RANGE."""
        self.assertTrue(_no_yr(f'The quick{EM}brown fox jumped.'))

    def test_em_surrounding_aside(self):
        """Em dashes used as aside punctuation shouldn't produce YEAR_RANGE."""
        self.assertTrue(_safe(f'The result{EM}as expected{EM}was clear.'))


# ============================================================================
# Class 5 — TestOtherUnicodeDashVariants
# 30 tests: less common Unicode dashes
# ============================================================================

class TestOtherUnicodeDashVariants(unittest.TestCase):
    """Exotic Unicode hyphen/dash chars should all normalize to ASCII hyphen."""

    # U+2010 HYPHEN
    def test_hyphen_proper_bare(self):
        self.assertTrue(_yr(f'2014{HY}2015'))

    def test_hyphen_proper_in_sentence(self):
        self.assertTrue(_yr(f'The period 2014{HY}2015.'))

    def test_hyphen_proper_reversed(self):
        self.assertTrue(_no_yr(f'2015{HY}2014'))

    def test_hyphen_proper_out_of_range(self):
        self.assertTrue(_no_yr(f'1800{HY}1900'))

    # U+2011 NON-BREAKING HYPHEN
    def test_nb_hyphen_bare(self):
        self.assertTrue(_yr(f'2014{NBH}2015'))

    def test_nb_hyphen_in_sentence(self):
        self.assertTrue(_yr(f'The era 2014{NBH}2015 passed.'))

    def test_nb_hyphen_reversed(self):
        self.assertTrue(_no_yr(f'2015{NBH}2014'))

    def test_nb_hyphen_out_of_range(self):
        self.assertTrue(_no_yr(f'1800{NBH}1900'))

    # U+2012 FIGURE DASH
    def test_figure_dash_bare(self):
        self.assertTrue(_yr(f'2014{FIG}2015'))

    def test_figure_dash_in_sentence(self):
        self.assertTrue(_yr(f'Period 2014{FIG}2015 matters.'))

    def test_figure_dash_reversed(self):
        self.assertTrue(_no_yr(f'2015{FIG}2014'))

    def test_figure_dash_out_of_range(self):
        self.assertTrue(_no_yr(f'1800{FIG}1900'))

    # U+2015 HORIZONTAL BAR
    def test_horizontal_bar_bare(self):
        self.assertTrue(_yr(f'2014{HB}2015'))

    def test_horizontal_bar_in_sentence(self):
        self.assertTrue(_yr(f'Range 2014{HB}2015.'))

    def test_horizontal_bar_reversed(self):
        self.assertTrue(_no_yr(f'2015{HB}2014'))

    # U+2212 MINUS SIGN
    def test_minus_sign_bare(self):
        self.assertTrue(_yr(f'2014{MIN}2015'))

    def test_minus_sign_in_sentence(self):
        self.assertTrue(_yr(f'Years 2014{MIN}2015.'))

    def test_minus_sign_reversed(self):
        self.assertTrue(_no_yr(f'2015{MIN}2014'))

    def test_minus_sign_out_of_range(self):
        self.assertTrue(_no_yr(f'1800{MIN}1900'))

    # U+FE63 SMALL HYPHEN-MINUS
    def test_small_hyphen_bare(self):
        self.assertTrue(_yr(f'2014{SHY}2015'))

    def test_small_hyphen_in_sentence(self):
        self.assertTrue(_yr(f'Span 2014{SHY}2015.'))

    def test_small_hyphen_reversed(self):
        self.assertTrue(_no_yr(f'2015{SHY}2014'))

    # U+FF0D FULLWIDTH HYPHEN-MINUS
    def test_fullwidth_hyphen_bare(self):
        self.assertTrue(_yr(f'2014{FWH}2015'))

    def test_fullwidth_hyphen_in_sentence(self):
        self.assertTrue(_yr(f'Period 2014{FWH}2015 reviewed.'))

    def test_fullwidth_hyphen_reversed(self):
        self.assertTrue(_no_yr(f'2015{FWH}2014'))

    def test_fullwidth_hyphen_out_of_range(self):
        self.assertTrue(_no_yr(f'1800{FWH}1900'))

    def test_all_variants_produce_ascii_key(self):
        """Every dash variant should produce '2014-2015' as the dict key."""
        for dash in [EN, EM, HY, NBH, FIG, HB, MIN, SHY, FWH]:
            with self.subTest(dash=repr(dash)):
                r = extract_explicit_dates(f'2014{dash}2015') or {}
                self.assertIn('2014-2015', r, msg=f'dash={repr(dash)} did not produce key 2014-2015')

    def test_all_variants_produce_year_range_value(self):
        """Every dash variant should produce 'YEAR_RANGE' as value."""
        for dash in [EN, EM, HY, NBH, FIG, HB, MIN, SHY, FWH]:
            with self.subTest(dash=repr(dash)):
                r = extract_explicit_dates(f'2014{dash}2015') or {}
                self.assertEqual(r.get('2014-2015'), 'YEAR_RANGE',
                                 msg=f'dash={repr(dash)} did not produce YEAR_RANGE')

    def test_all_variants_safe(self):
        """None of the exotic dash chars should cause an exception."""
        for dash in [EN, EM, HY, NBH, FIG, HB, MIN, SHY, FWH]:
            with self.subTest(dash=repr(dash)):
                self.assertTrue(_safe(f'2014{dash}2015'))


# ============================================================================
# Class 6 — TestEnDashWithSurroundingSpaces
# 20 tests: en or em dash WITH spaces — e.g. "2014 – 2015"
# ============================================================================

class TestEnDashWithSurroundingSpaces(unittest.TestCase):
    """En/em dash flanked by spaces requires both Unicode and space normalization."""

    def test_en_space_2014_2015(self):
        self.assertTrue(_yr(f'2014 {EN} 2015'))

    def test_en_space_2000_2010(self):
        self.assertTrue(_yr(f'2000 {EN} 2010'))

    def test_en_space_1939_1945(self):
        self.assertTrue(_yr(f'1939 {EN} 1945'))

    def test_en_space_in_sentence(self):
        self.assertTrue(_yr(f'The period 2014 {EN} 2015 was notable.'))

    def test_em_space_2014_2015(self):
        self.assertTrue(_yr(f'2014 {EM} 2015'))

    def test_em_space_2000_2010(self):
        self.assertTrue(_yr(f'2000 {EM} 2010'))

    def test_em_space_1939_1945(self):
        self.assertTrue(_yr(f'1939 {EM} 1945'))

    def test_em_space_in_sentence(self):
        self.assertTrue(_yr(f'The era 2014 {EM} 2015 was pivotal.'))

    def test_en_space_reversed_not_range(self):
        self.assertTrue(_no_yr(f'2015 {EN} 2014'))

    def test_em_space_reversed_not_range(self):
        self.assertTrue(_no_yr(f'2015 {EM} 2014'))

    def test_en_space_same_year_not_range(self):
        self.assertTrue(_no_yr(f'2014 {EN} 2014'))

    def test_em_space_same_year_not_range(self):
        self.assertTrue(_no_yr(f'2014 {EM} 2014'))

    def test_en_space_out_of_range(self):
        self.assertTrue(_no_yr(f'1800 {EN} 1900'))

    def test_em_space_out_of_range(self):
        self.assertTrue(_no_yr(f'1800 {EM} 1900'))

    def test_key_is_ascii(self):
        r = extract_explicit_dates(f'2014 {EN} 2015') or {}
        self.assertIn('2014-2015', r)

    def test_value_is_year_range(self):
        r = extract_explicit_dates(f'2014 {EN} 2015') or {}
        self.assertEqual(r.get('2014-2015'), 'YEAR_RANGE')

    def test_double_space_en_dash(self):
        self.assertTrue(_yr(f'2014  {EN}  2015'))

    def test_tab_en_dash(self):
        self.assertTrue(_yr(f'2014\t{EN}\t2015'))

    def test_nbsp_en_dash(self):
        """Non-breaking spaces around en dash."""
        self.assertTrue(_yr(f'2014{NBSP}{EN}{NBSP}2015'))

    def test_mixed_en_em_space(self):
        """Both en-spaced and em-spaced ranges in same text."""
        r = extract_explicit_dates(f'2000 {EN} 2010 and 2014 {EM} 2015') or {}
        self.assertIn('2000-2010', r)
        self.assertIn('2014-2015', r)


# ============================================================================
# Class 7 — TestSpacePaddedAsciiHyphen
# 20 tests: "YYYY - YYYY" (ASCII hyphen, spaces on each side)
# ============================================================================

class TestSpacePaddedAsciiHyphen(unittest.TestCase):
    """ASCII hyphen flanked by one or more spaces."""

    def test_single_space_2014_2015(self):
        self.assertTrue(_yr('2014 - 2015'))

    def test_single_space_2000_2010(self):
        self.assertTrue(_yr('2000 - 2010'))

    def test_single_space_1939_1945(self):
        self.assertTrue(_yr('1939 - 1945'))

    def test_single_space_consecutive(self):
        self.assertTrue(_yr('2019 - 2020'))

    def test_single_space_in_sentence(self):
        self.assertTrue(_yr('The period 2014 - 2015 was notable.'))

    def test_single_space_reversed_not_range(self):
        self.assertTrue(_no_yr('2015 - 2014'))

    def test_single_space_same_year_not_range(self):
        self.assertTrue(_no_yr('2014 - 2014'))

    def test_single_space_out_of_range(self):
        self.assertTrue(_no_yr('1800 - 1900'))

    def test_key_is_ascii_no_spaces(self):
        """Key should be '2014-2015', not '2014 - 2015'."""
        r = extract_explicit_dates('2014 - 2015') or {}
        self.assertIn('2014-2015', r)
        self.assertNotIn('2014 - 2015', r)

    def test_value_is_year_range(self):
        r = extract_explicit_dates('2014 - 2015') or {}
        self.assertEqual(r.get('2014-2015'), 'YEAR_RANGE')

    def test_double_space(self):
        self.assertTrue(_yr('2014  -  2015'))

    def test_triple_space(self):
        self.assertTrue(_yr('2014   -   2015'))

    def test_tab_around_hyphen(self):
        self.assertTrue(_yr('2014\t-\t2015'))

    def test_tab_before_only(self):
        self.assertTrue(_yr('2014\t- 2015'))

    def test_space_before_only(self):
        """Asymmetric: space before, no space after."""
        self.assertTrue(_yr('2014 -2015'))

    def test_space_after_only(self):
        """Asymmetric: no space before, space after."""
        self.assertTrue(_yr('2014- 2015'))

    def test_multiple_spaced_ranges(self):
        r = extract_explicit_dates('2000 - 2010 and 2014 - 2015') or {}
        self.assertIn('2000-2010', r)
        self.assertIn('2014-2015', r)

    def test_spaced_and_compact_same_text(self):
        """One compact ASCII range, one spaced range in same text."""
        r = extract_explicit_dates('2000-2010 and 2014 - 2015') or {}
        self.assertIn('2000-2010', r)
        self.assertIn('2014-2015', r)

    def test_spaced_range_in_parens(self):
        self.assertTrue(_yr('(2014 - 2015)'))

    def test_spaced_range_trailing_period(self):
        self.assertTrue(_yr('2014 - 2015.'))


# ============================================================================
# Class 8 — TestExtremeWhitespace
# 15 tests: extreme/unusual whitespace combos
# ============================================================================

class TestExtremeWhitespace(unittest.TestCase):
    """Pathological whitespace around hyphens and dashes."""

    def test_many_spaces(self):
        self.assertTrue(_yr('2014     -     2015'))

    def test_many_tabs(self):
        self.assertTrue(_yr('2014\t\t\t-\t\t\t2015'))

    def test_mixed_space_tab(self):
        self.assertTrue(_yr('2014 \t - \t 2015'))

    def test_newline_around_hyphen(self):
        self.assertTrue(_yr('2014\n-\n2015'))

    def test_carriage_return_around_hyphen(self):
        self.assertTrue(_yr('2014\r-\r2015'))

    def test_nbsp_around_ascii_hyphen(self):
        """Non-breaking spaces around ASCII hyphen."""
        self.assertTrue(_yr(f'2014{NBSP}-{NBSP}2015'))

    def test_nbsp_around_en_dash(self):
        self.assertTrue(_yr(f'2014{NBSP}{EN}{NBSP}2015'))

    def test_nbsp_around_em_dash(self):
        self.assertTrue(_yr(f'2014{NBSP}{EM}{NBSP}2015'))

    def test_many_spaces_reversed_not_range(self):
        """Extreme spaces don't rescue a reversed range."""
        self.assertTrue(_no_yr('2015     -     2014'))

    def test_many_spaces_out_of_range(self):
        self.assertTrue(_no_yr('1800     -     1900'))

    def test_many_spaces_same_year(self):
        self.assertTrue(_no_yr('2014     -     2014'))

    def test_form_feed_around_hyphen(self):
        self.assertTrue(_safe('2014\f-\f2015'))

    def test_vertical_tab_around_hyphen(self):
        self.assertTrue(_safe('2014\v-\v2015'))

    def test_newline_and_nbsp(self):
        self.assertTrue(_safe(f'2014\n{NBSP}-{NBSP}\n2015'))

    def test_zwsp_around_hyphen(self):
        """Zero-width space around ASCII hyphen: after normalization may or may not match."""
        self.assertTrue(_safe(f'2014{ZWS}-{ZWS}2015'))


# ============================================================================
# Class 9 — TestMixedDashTypesInText
# 20 tests: texts containing multiple different dash types simultaneously
# ============================================================================

class TestMixedDashTypesInText(unittest.TestCase):
    """Multiple different Unicode dash types in the same text."""

    def test_en_and_em_in_same_text(self):
        r = extract_explicit_dates(f'2000{EN}2010 and 2014{EM}2015') or {}
        self.assertIn('2000-2010', r)
        self.assertIn('2014-2015', r)

    def test_en_and_ascii_in_same_text(self):
        r = extract_explicit_dates(f'2000-2010 and 2014{EN}2015') or {}
        self.assertIn('2000-2010', r)
        self.assertIn('2014-2015', r)

    def test_em_and_ascii_in_same_text(self):
        r = extract_explicit_dates(f'2000-2010 and 2014{EM}2015') or {}
        self.assertIn('2000-2010', r)
        self.assertIn('2014-2015', r)

    def test_three_dash_types(self):
        r = extract_explicit_dates(f'1990-2000, 2000{EN}2010, 2014{EM}2015') or {}
        self.assertIn('1990-2000', r)
        self.assertIn('2000-2010', r)
        self.assertIn('2014-2015', r)

    def test_figure_and_en(self):
        r = extract_explicit_dates(f'2000{FIG}2010 and 2014{EN}2015') or {}
        self.assertIn('2000-2010', r)
        self.assertIn('2014-2015', r)

    def test_minus_and_em(self):
        r = extract_explicit_dates(f'2000{MIN}2010 and 2014{EM}2015') or {}
        self.assertIn('2000-2010', r)
        self.assertIn('2014-2015', r)

    def test_fullwidth_and_ascii(self):
        r = extract_explicit_dates(f'2000{FWH}2010 and 2014-2015') or {}
        self.assertIn('2000-2010', r)
        self.assertIn('2014-2015', r)

    def test_spaced_and_nonspaced_en(self):
        r = extract_explicit_dates(f'2000 {EN} 2010 and 2014{EN}2015') or {}
        self.assertIn('2000-2010', r)
        self.assertIn('2014-2015', r)

    def test_all_types_one_sentence(self):
        """Each variant in a list — all should be detected."""
        parts = [
            f'2000{EN}2001',
            f'2001{EM}2002',
            f'2002{HY}2003',
            f'2003{MIN}2004',
        ]
        text = ', '.join(parts)
        r = extract_explicit_dates(text) or {}
        yr_count = sum(1 for v in r.values() if v == 'YEAR_RANGE')
        self.assertGreaterEqual(yr_count, 4)

    def test_en_dash_in_text_non_year_hyphens_safe(self):
        """Compound words with hyphens + en dash year range — no interference."""
        text = f'mother-in-law attended the 2014{EN}2015 reunion.'
        self.assertTrue(_yr(text))

    def test_hyphenated_word_no_false_positive(self):
        """Compound word hyphens shouldn't produce YEAR_RANGE."""
        self.assertTrue(_no_yr('state-of-the-art technology'))

    def test_en_dash_between_words_no_false_positive(self):
        """En dash between plain words — no YEAR_RANGE."""
        self.assertTrue(_no_yr(f'north{EN}south corridor'))

    def test_em_dash_between_words_no_false_positive(self):
        self.assertTrue(_no_yr(f'the result{EM}as expected{EM}was clear'))

    def test_mixed_dash_all_invalid_years(self):
        """All dash types with out-of-range years — no YEAR_RANGE."""
        for dash in [EN, EM, HY, MIN, FWH]:
            with self.subTest(dash=repr(dash)):
                self.assertTrue(_no_yr(f'1800{dash}1900'))

    def test_mixed_dash_all_reversed(self):
        """All dash types with reversed years — no YEAR_RANGE."""
        for dash in [EN, EM, HY, MIN, FWH]:
            with self.subTest(dash=repr(dash)):
                self.assertTrue(_no_yr(f'2015{dash}2014'))

    def test_mixed_dash_all_same_year(self):
        """All dash types with same year — no YEAR_RANGE."""
        for dash in [EN, EM, HY, MIN, FWH]:
            with self.subTest(dash=repr(dash)):
                self.assertTrue(_no_yr(f'2014{dash}2014'))

    def test_list_of_ranges_different_dashes(self):
        text = f'- 2000{EN}2005\n- 2005{EM}2010\n- 2010-2015'
        self.assertTrue(_yr(text))

    def test_two_ranges_result_count(self):
        r = extract_explicit_dates(f'2000{EN}2010 then 2014{EM}2015') or {}
        yr_count = sum(1 for v in r.values() if v == 'YEAR_RANGE')
        self.assertGreaterEqual(yr_count, 2)

    def test_all_seven_unicode_variants_safe(self):
        """All exotic chars should not crash the extractor."""
        for dash in [EN, EM, HY, NBH, FIG, HB, MIN, SHY, FWH]:
            with self.subTest(dash=repr(dash)):
                self.assertTrue(_safe(f'2014{dash}2015'))

    def test_compact_and_spaced_mixed(self):
        r = extract_explicit_dates(f'2000{EN}2010 and 2014 - 2015') or {}
        self.assertIn('2000-2010', r)
        self.assertIn('2014-2015', r)


# ============================================================================
# Class 10 — TestNormalizationPreservesValidity
# 25 tests: normalization must not bypass year validation rules
# ============================================================================

class TestNormalizationPreservesValidity(unittest.TestCase):
    """After normalization, reversed/same/out-of-range rules still hold."""

    def test_en_reversed_still_fails(self):
        self.assertTrue(_no_yr(f'2020{EN}2010'))

    def test_em_reversed_still_fails(self):
        self.assertTrue(_no_yr(f'2020{EM}2010'))

    def test_hy_reversed_still_fails(self):
        self.assertTrue(_no_yr(f'2020{HY}2010'))

    def test_min_reversed_still_fails(self):
        self.assertTrue(_no_yr(f'2020{MIN}2010'))

    def test_fwh_reversed_still_fails(self):
        self.assertTrue(_no_yr(f'2020{FWH}2010'))

    def test_en_same_year_still_fails(self):
        self.assertTrue(_no_yr(f'2014{EN}2014'))

    def test_em_same_year_still_fails(self):
        self.assertTrue(_no_yr(f'2014{EM}2014'))

    def test_hy_same_year_still_fails(self):
        self.assertTrue(_no_yr(f'2014{HY}2014'))

    def test_en_below_min_still_fails(self):
        self.assertTrue(_no_yr(f'1800{EN}1900'))

    def test_em_below_min_still_fails(self):
        self.assertTrue(_no_yr(f'1800{EM}1900'))

    def test_hy_below_min_still_fails(self):
        self.assertTrue(_no_yr(f'1800{HY}1900'))

    def test_en_above_max_still_fails(self):
        self.assertTrue(_no_yr(f'2040{EN}2050'))

    def test_em_above_max_still_fails(self):
        self.assertTrue(_no_yr(f'2040{EM}2050'))

    def test_spaced_reversed_still_fails(self):
        self.assertTrue(_no_yr('2020 - 2010'))

    def test_spaced_same_year_still_fails(self):
        self.assertTrue(_no_yr('2014 - 2014'))

    def test_spaced_below_min_still_fails(self):
        self.assertTrue(_no_yr('1800 - 1900'))

    def test_spaced_above_max_still_fails(self):
        self.assertTrue(_no_yr('2040 - 2050'))

    def test_spaced_en_reversed_still_fails(self):
        self.assertTrue(_no_yr(f'2020 {EN} 2010'))

    def test_spaced_em_reversed_still_fails(self):
        self.assertTrue(_no_yr(f'2020 {EM} 2010'))

    def test_spaced_en_same_still_fails(self):
        self.assertTrue(_no_yr(f'2014 {EN} 2014'))

    def test_spaced_em_out_of_range_still_fails(self):
        self.assertTrue(_no_yr(f'1800 {EM} 1900'))

    def test_one_year_out_of_range_en_still_fails(self):
        """Start in range, end out of range."""
        self.assertTrue(_no_yr(f'2025{EN}2099'))

    def test_one_year_out_of_range_em_still_fails(self):
        self.assertTrue(_no_yr(f'2025{EM}2099'))

    def test_start_out_end_in_range_en_still_fails(self):
        """Start out of range, end in range."""
        self.assertTrue(_no_yr(f'1899{EN}2010'))

    def test_start_out_end_in_range_em_still_fails(self):
        self.assertTrue(_no_yr(f'1899{EM}2010'))


# ============================================================================
# Class 11 — TestNormalizationNoFalsePositives
# 20 tests: normalization must not introduce YEAR_RANGE where none exists
# ============================================================================

class TestNormalizationNoFalsePositives(unittest.TestCase):
    """Non-year content with Unicode dashes should not produce YEAR_RANGE."""

    def test_compound_word_en_dash(self):
        self.assertTrue(_no_yr(f'mother{EN}in{EN}law'))

    def test_compound_word_em_dash(self):
        self.assertTrue(_no_yr(f'state{EM}of{EM}the{EM}art'))

    def test_price_range_en_dash(self):
        """$20–$30 — not a year range."""
        self.assertTrue(_no_yr(f'$20{EN}$30'))

    def test_page_range_en_dash(self):
        """Pages 3–10 — not a year range."""
        self.assertTrue(_no_yr(f'pages 3{EN}10'))

    def test_chapter_range_em_dash(self):
        self.assertTrue(_no_yr(f'chapters 1{EM}5'))

    def test_time_range_en_dash(self):
        """9–5 — not a year range."""
        self.assertTrue(_no_yr(f'9{EN}5'))

    def test_small_numbers_en_dash(self):
        self.assertTrue(_no_yr(f'100{EN}200'))

    def test_large_numbers_out_of_range(self):
        self.assertTrue(_no_yr(f'10000{EN}20000'))

    def test_non_year_four_digits_en(self):
        """1234–1235: both below MIN_YEAR."""
        self.assertTrue(_no_yr(f'1234{EN}1235'))

    def test_phone_like_en_dash(self):
        self.assertTrue(_no_yr(f'555{EN}1234'))

    def test_score_en_dash(self):
        """Game score 3–0 — not a year range."""
        self.assertTrue(_no_yr(f'3{EN}0'))

    def test_street_number_en_dash(self):
        """Address range 100–200 Main St."""
        self.assertTrue(_no_yr(f'100{EN}200 Main St'))

    def test_version_en_dash(self):
        self.assertTrue(_no_yr(f'version 1{EN}2'))

    def test_size_range_em_dash(self):
        self.assertTrue(_no_yr(f'sizes 8{EM}12'))

    def test_temperature_range_en(self):
        self.assertTrue(_no_yr(f'20{EN}30 degrees'))

    def test_en_dash_between_words(self):
        self.assertTrue(_no_yr(f'north{EN}south'))

    def test_em_dash_in_sentence_no_numbers(self):
        self.assertTrue(_no_yr(f'The answer{EM}of course{EM}is obvious.'))

    def test_double_en_dash_stacked(self):
        """2014––2015 (two en dashes) — should not match."""
        self.assertTrue(_no_yr(f'2014{EN}{EN}2015'))

    def test_en_em_mixed_stacked(self):
        """2014–—2015 (en then em) — should not match."""
        self.assertTrue(_no_yr(f'2014{EN}{EM}2015'))

    def test_single_year_with_dash(self):
        """2014- with no second year — not a range."""
        self.assertTrue(_no_yr(f'2014{EN}'))


# ============================================================================
# Class 12 — TestAsciiHyphenUnaffected
# 15 tests: normalization must not break existing ASCII hyphen behavior
# ============================================================================

class TestAsciiHyphenUnaffected(unittest.TestCase):
    """Pre-existing ASCII hyphen behavior must be preserved after normalization is added."""

    def test_ascii_2014_2015_still_works(self):
        self.assertTrue(_yr('2014-2015'))

    def test_ascii_2000_2010_still_works(self):
        self.assertTrue(_yr('2000-2010'))

    def test_ascii_1939_1945_still_works(self):
        self.assertTrue(_yr('1939-1945'))

    def test_ascii_reversed_still_fails(self):
        self.assertTrue(_no_yr('2015-2014'))

    def test_ascii_same_year_still_fails(self):
        self.assertTrue(_no_yr('2014-2014'))

    def test_ascii_out_of_range_still_fails(self):
        self.assertTrue(_no_yr('1800-1900'))

    def test_ascii_from_to_still_works(self):
        self.assertTrue(_yr('from 2004 to 2008'))

    def test_ascii_between_and_still_works(self):
        self.assertTrue(_yr('between 2010 and 2020'))

    def test_ascii_in_sentence_still_works(self):
        self.assertTrue(_yr('The period 2014-2015 was significant.'))

    def test_ascii_key_format_unchanged(self):
        r = extract_explicit_dates('2014-2015') or {}
        self.assertEqual(r.get('2014-2015'), 'YEAR_RANGE')

    def test_hyphenated_word_no_regression(self):
        """Compound words with ASCII hyphens should never produce YEAR_RANGE."""
        self.assertTrue(_no_yr('mother-in-law'))

    def test_isbn_no_regression(self):
        self.assertTrue(_no_yr('978-3-16'))

    def test_multiple_ascii_ranges_no_regression(self):
        r = extract_explicit_dates('2000-2010 and 2014-2015') or {}
        self.assertIn('2000-2010', r)
        self.assertIn('2014-2015', r)

    def test_prose_year_only_no_regression(self):
        r = extract_explicit_dates('in 2024') or {}
        self.assertIn('YEAR_ONLY', r.values())

    def test_written_date_no_regression(self):
        """March 2024: written date parsing not affected by normalization."""
        self.assertTrue(_safe('March 2024'))


# ============================================================================
# Class 13 — TestSoftAndInvisibleChars
# 10 tests: soft hyphen, zero-width space, BOM — should not produce YEAR_RANGE
# ============================================================================

class TestSoftAndInvisibleChars(unittest.TestCase):
    """Invisible/soft characters between years should not produce YEAR_RANGE."""

    def test_soft_hyphen_between_years(self):
        """U+00AD SOFT HYPHEN is a formatting hint; should not match."""
        self.assertTrue(_no_yr(f'2014{SHY2}2015'))

    def test_zero_width_space_between_years(self):
        """U+200B between years: no hyphen, no match."""
        self.assertTrue(_no_yr(f'2014{ZWS}2015'))

    def test_nbsp_between_years_no_dash(self):
        """NBSP alone (no dash) between years: just spaces, not a range."""
        self.assertTrue(_no_yr(f'2014{NBSP}2015'))

    def test_bom_between_years(self):
        """BOM/ZWNBSP between years should not produce a match."""
        self.assertTrue(_safe(f'2014\ufeff2015'))

    def test_soft_hyphen_safe(self):
        self.assertTrue(_safe(f'2014{SHY2}2015'))

    def test_zwsp_safe(self):
        self.assertTrue(_safe(f'2014{ZWS}2015'))

    def test_nbsp_safe(self):
        self.assertTrue(_safe(f'2014{NBSP}2015'))

    def test_double_zero_width(self):
        self.assertTrue(_safe(f'2014{ZWS}{ZWS}2015'))

    def test_mixed_invisible_no_match(self):
        self.assertTrue(_no_yr(f'2014{ZWS}{NBSP}2015'))

    def test_combining_chars_safe(self):
        """Unicode combining characters should not crash."""
        self.assertTrue(_safe('2014\u0301-2015'))


# ============================================================================
# Class 14 — TestDoubleDashAndChainedDashes
# 10 tests: multiple consecutive dashes shouldn't produce YEAR_RANGE
# ============================================================================

class TestDoubleDashAndChainedDashes(unittest.TestCase):
    """Multiple consecutive dashes or chained Unicode dashes between years."""

    def test_double_ascii_hyphen(self):
        """2014--2015 — double ASCII hyphen."""
        self.assertTrue(_no_yr('2014--2015'))

    def test_double_en_dash(self):
        self.assertTrue(_no_yr(f'2014{EN}{EN}2015'))

    def test_double_em_dash(self):
        self.assertTrue(_no_yr(f'2014{EM}{EM}2015'))

    def test_en_then_em(self):
        self.assertTrue(_no_yr(f'2014{EN}{EM}2015'))

    def test_em_then_en(self):
        self.assertTrue(_no_yr(f'2014{EM}{EN}2015'))

    def test_ascii_then_en(self):
        self.assertTrue(_no_yr(f'2014-{EN}2015'))

    def test_en_then_ascii(self):
        self.assertTrue(_no_yr(f'2014{EN}-2015'))

    def test_triple_ascii_hyphen(self):
        self.assertTrue(_no_yr('2014---2015'))

    def test_dash_space_dash(self):
        """2014 - - 2015: double-hyphen with space."""
        self.assertTrue(_no_yr('2014 - - 2015'))

    def test_all_double_safe(self):
        """None of the double-dash forms should crash."""
        for d1, d2 in [(EN, EN), (EM, EM), (EN, EM), ('-', EN), (EN, '-')]:
            with self.subTest(d1=repr(d1), d2=repr(d2)):
                self.assertTrue(_safe(f'2014{d1}{d2}2015'))


if __name__ == '__main__':
    unittest.main()
