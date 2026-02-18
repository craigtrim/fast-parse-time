#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Red Team Test Suite -- Prose Year Patterns
==========================================
Target function : extract_explicit_dates(text: str) -> Dict[str, str]
Target patterns : in 2024, since 2019, circa 2004, as of 2004, prior to 2010,
                  from 2019, through 2019, by 2024, until 2030, before 2004,
                  after 2004, during 2020, around 2019, back to 1998

Related GitHub Issue:
    #43 https://github.com/craigtrim/fast-parse-time/issues/43

ATTACK SURFACE OVERVIEW
------------------------
Prose-year expressions require the parser to identify a temporal preposition
or multi-word preposition adjacent to a 4-digit year and classify the result
as YEAR_ONLY or TIMEFRAME_RELATIVE_TO_NOW. The attack vectors here are:

  1. ALL PREPOSITIONS AT MULTIPLE YEARS: If the parser was tuned on only a
     small set of year/preposition combinations, it may fail on the full cross-
     product. Thirteen prepositions times a spread of 8+ years creates 100+
     true-positive cases from this one dimension alone.

  2. CASE VARIANTS: Prepositions are often encountered in ALL CAPS (headlines),
     Title Case (sentence starts), and mixed case (transcription noise). The
     parser must be case-insensitive.

  3. SENTENCE EMBEDDING AND PUNCTUATION ADJACENCY: Years appear mid-sentence,
     at sentence boundaries (trailing period), and comma-adjacent (clauses).
     Anchored regexes and word-boundary-sensitive regexes will fail here.

  4. MULTI-WORD PREPOSITIONS: "as of", "back to", and "prior to" each require
     matching a two-word phrase before the year. These are a common oversight
     in single-token preposition parsers.

  5. OUT-OF-RANGE YEARS: If the parser enforces a valid year range (e.g.,
     [1926, 2036]), then years outside that range must be rejected. Both
     false-positive (the parser matches a year it should reject) and false-
     negative (the parser misses a year it should accept) failures are tested.

  6. NON-YEAR NUMBERS: Prepositions can appear near non-temporal numbers (port
     numbers, version numbers, item counts). The parser must not tag "port 8080"
     or "version 42" as date references.

  7. UNICODE: Fullwidth digits, zero-width spaces, and RTL markers can defeat
     ASCII-only regex patterns or produce unexpected matches through Python's
     Unicode-aware \d matching.

XFAIL STRATEGY
--------------
All tests carry ``pytestmark = pytest.mark.xfail`` so the suite remains green
while the implementation is incomplete. An unexpected pass (xpass) is a
promotion candidate.

TRUE POSITIVE TESTS  ->  assert len(result) > 0
FALSE POSITIVE TESTS ->  assert len(result) == 0
BOUNDARY TESTS       ->  assert isinstance(result, dict)  (no direction)
UNICODE TESTS        ->  assert isinstance(result, dict)  (no direction)
"""

import pytest
from fast_parse_time.api import extract_explicit_dates

# Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43

pytestmark = pytest.mark.xfail(reason='red_team: not yet validated')


# ============================================================================
# SECTION 1 -- TRUE POSITIVES: ALL 13 PREPOSITIONS x 8 YEARS
# ============================================================================
#
# The 13 prepositions under test are:
#   in, since, circa, as of, prior to, from, through, by,
#   until, before, after, during, around, back to
#
# The 8 year values span the valid range with historical and near-future
# coverage: 1930, 1950, 1970, 1990, 2000, 2010, 2020, 2030.
#
# A truly general parser must handle every cell of this 14x8 matrix.
# Each failure isolates a specific (preposition, year) gap.

@pytest.mark.parametrize('text', [
    # -- preposition: in --
    'in 1930',
    'in 1950',
    'in 1970',
    'in 1990',
    'in 2000',
    'in 2010',
    'in 2020',
    'in 2030',
    # -- preposition: since --
    'since 1930',
    'since 1950',
    'since 1970',
    'since 1990',
    'since 2000',
    'since 2010',
    'since 2020',
    'since 2030',
    # -- preposition: circa --
    'circa 1930',
    'circa 1950',
    'circa 1970',
    'circa 1990',
    'circa 2000',
    'circa 2010',
    'circa 2020',
    'circa 2030',
    # -- multi-word preposition: as of --
    'as of 1930',
    'as of 1950',
    'as of 1970',
    'as of 1990',
    'as of 2000',
    'as of 2010',
    'as of 2020',
    'as of 2030',
    # -- multi-word preposition: prior to --
    'prior to 1930',
    'prior to 1950',
    'prior to 1970',
    'prior to 1990',
    'prior to 2000',
    'prior to 2010',
    'prior to 2020',
    'prior to 2030',
    # -- preposition: from --
    'from 1930',
    'from 1950',
    'from 1970',
    'from 1990',
    'from 2000',
    'from 2010',
    'from 2020',
    'from 2030',
    # -- preposition: through --
    'through 1930',
    'through 1950',
    'through 1970',
    'through 1990',
    'through 2000',
    'through 2010',
    'through 2020',
    'through 2030',
    # -- preposition: by --
    'by 1930',
    'by 1950',
    'by 1970',
    'by 1990',
    'by 2000',
    'by 2010',
    'by 2020',
    'by 2030',
    # -- preposition: until --
    'until 1930',
    'until 1950',
    'until 1970',
    'until 1990',
    'until 2000',
    'until 2010',
    'until 2020',
    'until 2030',
    # -- preposition: before --
    'before 1930',
    'before 1950',
    'before 1970',
    'before 1990',
    'before 2000',
    'before 2010',
    'before 2020',
    'before 2030',
    # -- preposition: after --
    'after 1930',
    'after 1950',
    'after 1970',
    'after 1990',
    'after 2000',
    'after 2010',
    'after 2020',
    'after 2030',
    # -- preposition: during --
    'during 1930',
    'during 1950',
    'during 1970',
    'during 1990',
    'during 2000',
    'during 2010',
    'during 2020',
    'during 2030',
    # -- preposition: around --
    'around 1930',
    'around 1950',
    'around 1970',
    'around 1990',
    'around 2000',
    'around 2010',
    'around 2020',
    'around 2030',
    # -- multi-word preposition: back to --
    'back to 1930',
    'back to 1950',
    'back to 1970',
    'back to 1990',
    'back to 2000',
    'back to 2010',
    'back to 2020',
    'back to 2030',
])
def test_prose_year_all_prepositions_true_positive(text):
    """
    Attack vector: all 14 supported prepositions (including multi-word forms)
    paired with a spread of valid years across the supported range.

    Why a parser might fail: a parser developed against a limited set of
    (preposition, year) training pairs may produce a regex that accidentally
    hard-codes those specific combinations. For example, a pattern like
    ``(?:in|since) (?:2004|2019|2024)`` would pass only those 6 cases.

    The multi-word prepositions ('as of', 'prior to', 'back to') require the
    regex to match two consecutive tokens before the year. A single-token
    preposition pattern like ``\\b(?:in|since|from)\\b\\s+\\d{4}`` will miss
    all three multi-word forms, silently dropping real temporal references in
    financial, legal, and historical texts where these constructions are common.

    What failure reveals: each failing case identifies a specific preposition or
    year value that the parser does not handle, enabling targeted remediation.

    Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
    """
    result = extract_explicit_dates(text)
    assert len(result) > 0


# ============================================================================
# SECTION 2 -- TRUE POSITIVES: CASE VARIANTS
# ============================================================================

@pytest.mark.parametrize('text', [
    # Uppercase prepositions (common in headlines, all-caps environments).
    'IN 2024',
    'SINCE 2019',
    'CIRCA 2004',
    'AS OF 2010',
    'PRIOR TO 1998',
    'FROM 2015',
    'THROUGH 2020',
    'BY 2024',
    'UNTIL 2030',
    'BEFORE 2004',
    'AFTER 2004',
    'DURING 2020',
    'AROUND 2019',
    'BACK TO 1998',
    # Title case (sentence-initial).
    'In 2024',
    'Since 2019',
    'Circa 2004',
    'As Of 2010',
    'Prior To 1998',
    'From 2015',
    'Through 2020',
    'By 2024',
    'Until 2030',
    'Before 2004',
    'After 2004',
    'During 2020',
    'Around 2019',
    'Back To 1998',
    # Mixed case (transcription noise, OCR errors).
    'iN 2024',
    'SiNCE 2019',
    'CiRCA 2004',
    'As oF 2010',
    'PRIoR TO 1998',
    'FrOM 2015',
    'ThROUGH 2020',
    'bY 2024',
    'UnTIL 2030',
    'BEFore 2004',
    'AFTer 2004',
    'DURing 2020',
    'ArOUND 2019',
    'BACK tO 1998',
])
def test_prose_year_case_variants_true_positive(text):
    """
    Attack vector: case variants of temporal prepositions (ALL CAPS, Title Case,
    and mixed-case).

    Why a parser might fail: a regex pattern that uses literal lowercase strings
    without the ``re.IGNORECASE`` flag (or equivalent) will fail on all-caps and
    title-case inputs. These are extremely common in real-world text: newspaper
    headlines, legal documents, government reports, and transcription outputs from
    speech-to-text systems frequently use non-lowercase prepositions.

    The mixed-case variants ('iN 2024', 'SiNCE 2019') simulate OCR noise and
    character substitution errors that arise when text is extracted from images or
    scanned documents. A parser that is case-insensitive at the character level
    (via ``re.IGNORECASE``) will handle all of these correctly.

    What failure reveals: the parser performs case-sensitive matching, making it
    brittle in real-world text processing pipelines that do not normalise case
    before calling the API.

    Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
    """
    result = extract_explicit_dates(text)
    assert len(result) > 0


# ============================================================================
# SECTION 3 -- TRUE POSITIVES: SENTENCE EMBEDDED
# ============================================================================

@pytest.mark.parametrize('text', [
    # Years appear at sentence end (trailing period).
    'things happened in 2024.',
    'the policy was effective since 2019.',
    'circa 2004.',
    'as of 2010.',
    'prior to 1998.',
    # Years appear mid-sentence, comma-adjacent.
    'results improved, since 2019, dramatically',
    'the law, as of 2010, applies to all',
    'revenue grew, from 2015, by 40%',
    'operations, during 2020, were disrupted',
    # Years appear after a comma-separated clause.
    'after years of decline, in 2024 we saw recovery',
    'despite challenges, by 2030 the project will complete',
    'historically, around 2019, tensions peaked',
    # Years embedded in longer sentences.
    'the company was founded in 1970 and grew steadily',
    'records show that since 1990 the trend has been upward',
    'the regulation, which came into force before 2004, was repealed',
    'profits after 2000 consistently exceeded projections',
    'the system was in use through 2010 before replacement',
    'we expect completion until 2030 at the latest',
    'back to 1998, the data shows a clear pattern',
    'from 2019 onwards the new methodology was applied',
    # Sentence-initial year expression.
    'In 2024 the market changed significantly.',
    'Since 2019 we have observed consistent growth.',
    'By 2030 all targets should be met.',
    'Before 2004 the regulation did not apply.',
    'After 2010 the sector recovered.',
    # Year expression followed by additional date context.
    'in 2024 and in 2019 the results were similar',
    'from 2010 through 2020 the project ran continuously',
])
def test_prose_year_sentence_embedded_true_positive(text):
    """
    Attack vector: temporal prepositions with years embedded in prose sentences,
    adjacent to punctuation, or at sentence boundaries.

    Why a parser might fail: a regex anchored with ``^`` or ``$`` will only match
    when the year expression is the entire input. More commonly, the regex uses
    ``\\b`` (word boundary) which may not correctly span the transition between a
    comma and the preposition, or between the year and a trailing period.

    Comma-adjacent cases like '...since 2019, the...' are particularly tricky:
    the comma is not a word character, so ``\\b`` between the comma and 'since'
    may or may not fire depending on the regex engine's definition. A parser that
    requires a space before the preposition will fail on '..., since...' (comma
    immediately before the preposition without a space).

    What failure reveals: the parser is brittle to punctuation context and cannot
    reliably extract years from flowing prose.

    Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
    """
    result = extract_explicit_dates(text)
    assert len(result) > 0


# ============================================================================
# SECTION 4 -- TRUE POSITIVES: MULTI-WORD PREPOSITIONS WITH MULTIPLE YEARS
# ============================================================================

@pytest.mark.parametrize('text', [
    # 'as of' with multiple year values.
    'as of 2019',
    'as of 1998',
    'as of 2004',
    'as of 2010',
    'as of 2020',
    'as of 2024',
    'as of 2030',
    'as of 1970',
    'as of 1990',
    # 'back to' with multiple year values.
    'back to 1998',
    'back to 2000',
    'back to 2004',
    'back to 2010',
    'back to 2019',
    'back to 2024',
    'back to 1970',
    'back to 1950',
    'back to 1930',
    # 'prior to' with multiple year values.
    'prior to 2010',
    'prior to 2000',
    'prior to 2004',
    'prior to 2019',
    'prior to 2024',
    'prior to 1990',
    'prior to 1970',
    'prior to 1950',
    'prior to 1930',
    # Mixed multi-word prepositions in one string.
    'as of 2019 and prior to 2024',
    'back to 1998 and as of 2010',
    'prior to 2000 and back to 1990',
])
def test_prose_year_multi_word_prepositions_true_positive(text):
    """
    Attack vector: multi-word temporal prepositions ('as of', 'back to', 'prior to')
    combined with a range of valid year values.

    Why a parser might fail: a single-token preposition regex like
    ``\\b(?:in|since|from|by|until|before|after|during|around|through|circa)\\b``
    does not include the two-word forms. Adding 'as' would cause false positives on
    "as soon as" or "as long as". The correct approach is to match the full two-word
    phrase: ``as\\s+of``, ``back\\s+to``, ``prior\\s+to``.

    The ``\\s+`` (one or more whitespace) between the words is important: user input
    may contain a double space, a tab, or a non-breaking space between 'as' and 'of'.
    A regex that uses a literal single space `` `` will miss these variants.

    What failure reveals: the parser only handles single-token prepositions and
    misses the three two-word forms, causing silent data loss on common expressions
    found in financial reports ('as of 2019'), historical analyses ('back to 1998'),
    and regulatory documents ('prior to 2010').

    Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
    """
    result = extract_explicit_dates(text)
    assert len(result) > 0


# ============================================================================
# SECTION 5 -- FALSE POSITIVES: PREPOSITION + OUT-OF-RANGE YEAR
# ============================================================================

@pytest.mark.parametrize('text', [
    # Years below the minimum supported year (assumed: 1926 based on project codebase).
    'in 1800',
    'in 1850',
    'in 1900',
    'in 1920',
    'in 1925',          # one below min (1926)
    'since 1800',
    'since 1850',
    'since 1900',
    'since 1925',
    'by 1850',
    'by 1900',
    'by 1920',
    'by 1925',
    'from 1800',
    'from 1900',
    'from 1920',
    'from 1925',
    'before 1800',
    'before 1900',
    'before 1925',
    'after 1800',
    'circa 1800',
    'around 1900',
    'during 1850',
    'back to 1800',
    'as of 1900',
    'prior to 1800',
    # Years above the maximum supported year (assumed: 2036 based on project codebase).
    'in 2037',          # one above max
    'in 2040',
    'in 2050',
    'in 2090',
    'in 2100',
    'since 2050',
    'since 2100',
    'by 2037',
    'by 2050',
    'by 2100',
    'from 2050',
    'from 2100',
    'until 2050',
    'until 2100',
    'before 2050',
    'after 2050',
    'through 2050',
    'around 2050',
    'back to 2050',
    'as of 2050',
])
def test_prose_year_out_of_range_false_positive(text):
    """
    Attack vector: temporal prepositions paired with years outside the parser's
    supported year range.

    Why a parser might fail (producing a false positive): if the year-range guard
    in the parser only validates years extracted by the prose-year sub-module but
    not those extracted by other sub-modules, an out-of-range year may slip
    through when a different code path is triggered.

    Conversely, if the year-range guard is too strict (e.g., rejecting 1926 when
    the documentation says 1926 is valid), then boundary-adjacent years will be
    incorrectly rejected, producing false negatives.

    The minimum boundary (1925 vs 1926) and maximum boundary (2036 vs 2037) cases
    are included explicitly in the boundary section to provide unambiguous pass/fail
    evidence for the off-by-one question.

    What failure reveals (false positive produced): the parser is not enforcing
    the year-range guard correctly, accepting years from the distant past or far
    future that have no practical temporal significance in the supported domain.

    Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
    """
    result = extract_explicit_dates(text)
    assert len(result) == 0


# ============================================================================
# SECTION 6 -- FALSE POSITIVES: PREPOSITION + NON-YEAR NUMBER
# ============================================================================

@pytest.mark.parametrize('text', [
    # Small numbers that are not years.
    'in 42',
    'in 99',
    'in 5',
    'since 99',
    'since 7',
    'by 123',
    'by 12',
    'by 3',
    'from 5',
    'from 99',
    'from 0',
    'until 42',
    'before 12',
    'after 7',
    'during 99',
    'around 5',
    'through 12',
    'circa 50',
    # 3-digit numbers (not 4-digit years).
    'in 202',
    'since 201',
    'by 199',
    'from 200',
    'until 203',
    'before 202',
    'after 195',
    'during 202',
    # Large numbers (more than 4 digits).
    'in 99999',
    'since 10000',
    'by 20240',
    'from 20245',
    # Zero.
    'in 0',
    'since 0',
    'by 0',
])
def test_prose_year_non_year_number_false_positive(text):
    """
    Attack vector: temporal prepositions paired with numbers that are not 4-digit
    years (2-digit, 3-digit, 5-digit, or zero).

    Why a parser might fail (producing a false positive): a regex that uses
    ``\\d+`` (any number of digits) rather than ``\\d{4}`` (exactly four digits)
    will match 'in 42' and 'from 5'. Conversely, a regex that uses ``\\d{4,}``
    (four or more digits) will also match 'in 20245', incorrectly treating a
    5-digit number adjacent to a preposition as a year.

    The parser must use exactly ``\\d{4}`` for the year group, and may further
    validate that the 4-digit number falls within a plausible year range.

    What failure reveals (false positive produced): the parser is matching
    non-year numbers as year references, which would cause incorrect date
    extraction from texts containing version numbers, item counts, or identifiers
    that happen to appear after a temporal preposition.

    Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
    """
    result = extract_explicit_dates(text)
    assert len(result) == 0


# ============================================================================
# SECTION 7 -- FALSE POSITIVES: PREPOSITION + PARTIAL 4-DIGIT SEQUENCE
# ============================================================================

@pytest.mark.parametrize('text', [
    # These look like year patterns but are actually partial sequences.
    'in 202',           # 3 digits -- not a year
    'from 20245',       # 5 digits -- not a year
    'since 20',         # 2 digits -- not a year
    'by 2',             # 1 digit -- not a year
    'until 20249',      # 5 digits -- not a year
    'in 20',
    'before 20',
    'after 202',
    'around 2024a',     # 4 digits + alpha character
    'in 2024abc',       # 4 digits immediately followed by alpha (may or may not be year)
    'since 2024-',      # 4 digits followed by hyphen (could be start of YEAR-RANGE)
    'by 2024x',
    'from 2019z',
])
def test_prose_year_partial_sequence_false_positive(text):
    """
    Attack vector: prepositions adjacent to digit sequences that are almost but not
    exactly 4-digit years.

    Why a parser might fail (producing a false positive): a regex using ``\\d{4}``
    without word-boundary anchoring (``\\b``) can match 4 digits anywhere in a
    longer digit string. For example, ``in 20245`` would match 'in 2024' if the
    regex does not require a word boundary or a non-digit character after the year.

    The case of '2024a' and '2024abc' is interesting: the 4 digits are valid,
    but the immediate alpha suffix may indicate a version identifier (2024a =
    version 2024 alpha) rather than a year. This is a policy question: whether
    the parser should be strict (require digit isolation) or lenient (accept
    any 4-digit group preceded by a preposition). The test records current behaviour.

    What failure reveals (false positive produced): the parser is matching digit
    substrings within larger token sequences.

    Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
    """
    result = extract_explicit_dates(text)
    assert len(result) == 0


# ============================================================================
# SECTION 8 -- FALSE POSITIVES: CODE/TECH CONTEXTS
# ============================================================================

@pytest.mark.parametrize('text', [
    # Version assignments in code.
    'version = 2024',
    'VERSION = 2019',
    'ver = 2004',
    'v = 2010',
    # Port numbers (common false-positive context).
    'port 8080',
    'port 443',
    'port 8443',
    'port 3000',
    'port 5432',
    'port 27017',
    # ID/reference patterns.
    'id: 2024',
    'id: 2019',
    'ref: 2019',
    'id=2024',
    'id=2019',
    # Hash/issue reference.
    '#2024',
    '#2019',
    '#2004',
    # Error codes.
    'error 2024',
    'code 2019',
    'status 2004',
    # Year in a purely numeric context with no preposition.
    '2024',
    '2019',
    '2004',
    '2010',
    '2020',
    # Arithmetic or list context.
    'items: 2024',
    'count: 2019',
    'total 2020',
    # File names and paths.
    'file2024.csv',
    'report2019.pdf',
    'log2020.txt',
])
def test_prose_year_code_tech_context_false_positive(text):
    """
    Attack vector: non-temporal numeric contexts where a 4-digit number that
    happens to be a plausible year appears without a temporal preposition.

    Why a parser might fail (producing a false positive): the prose-year extractor
    is specifically designed to require a temporal preposition BEFORE the year.
    However, if the preposition-detection logic has a bug that treats certain
    non-preposition tokens ('id:', 'port', 'error', '#') as equivalent to
    temporal prepositions, it will generate false positives.

    Conversely, if another sub-module (year-only extractor, numeric-date extractor)
    is too aggressive and treats any isolated 4-digit number in the range [1926,
    2036] as a year reference, then the inputs "2024", "2019", etc. (with no
    context at all) will produce false positives.

    The port-number cases ('port 8080', 'port 443') test whether the parser
    incorrectly treats 'port' as a temporal preposition. Port numbers are 4 digits
    or fewer, so an out-of-range guard on the year value would correctly reject
    them, but a parser without range validation would match 'port 443' as 'port
    [year=443]' which would then fail only if 3-digit filtering is correct.

    What failure reveals (false positive produced): the parser has over-broad
    matching that does not require a genuine temporal preposition.

    Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
    """
    result = extract_explicit_dates(text)
    assert len(result) == 0


# ============================================================================
# SECTION 9 -- BOUNDARY: EXACT RANGE LIMITS
# ============================================================================

@pytest.mark.parametrize('text, expect_match', [
    # Exact minimum -- should match (1926 is the stated floor).
    ('in 1926',        True),
    ('since 1926',     True),
    ('from 1926',      True),
    ('by 1926',        True),
    ('as of 1926',     True),
    ('back to 1926',   True),
    ('prior to 1926',  True),
    # Exact maximum -- should match (2036 is the stated ceiling).
    ('by 2036',        True),
    ('in 2036',        True),
    ('since 2036',     True),
    ('from 2036',      True),
    ('until 2036',     True),
    ('as of 2036',     True),
    ('after 2036',     True),
    # One below minimum -- should NOT match.
    ('in 1925',        False),
    ('since 1925',     False),
    ('from 1925',      False),
    ('by 1925',        False),
    # One above maximum -- should NOT match.
    ('by 2037',        False),
    ('in 2037',        False),
    ('since 2037',     False),
    ('from 2037',      False),
    ('until 2037',     False),
])
def test_prose_year_boundary(text, expect_match):
    """
    Attack vector: years at the exact boundary of the supported range (1926 and
    2036) and one step beyond in each direction (1925 and 2037).

    Why a parser might fail: off-by-one errors in range guards are among the most
    common bugs in parser implementations. A guard written as ``year >= 1927``
    instead of ``year >= 1926`` will silently reject all inputs containing 'in 1926'
    even though 1926 is explicitly listed as valid.

    Similarly, a guard written as ``year <= 2035`` will reject 'by 2036', and a
    guard written as ``year < 2037`` will (correctly) reject 'by 2037' but this
    is equivalent to ``year <= 2036`` and should produce the same result.

    This test is parametrised with explicit expected outcomes (True/False) so that
    a single test function verifies both inclusion and exclusion behaviour, making
    it trivial to find the exact off-by-one value in a failing run.

    Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
    """
    result = extract_explicit_dates(text)
    if expect_match:
        assert len(result) > 0
    else:
        assert len(result) == 0


# ============================================================================
# SECTION 10 -- UNICODE: HOMOGLYPH AND INVISIBLE CHARACTER ATTACKS
# ============================================================================

@pytest.mark.parametrize('text, description', [
    # Fullwidth digits (U+FF10-U+FF19) in place of ASCII digits.
    # Python's re.UNICODE flag (default) may match these via \d, causing
    # unexpected matches on what looks like a valid year but isn't.
    ('in \uFF12\uFF10\uFF12\uFF14', 'fullwidth digits for 2024 (in ２０２４)'),
    ('since \uFF12\uFF10\uFF11\uFF19', 'fullwidth digits for 2019 (since ２０１９)'),
    ('by \uFF12\uFF10\uFF12\uFF14', 'fullwidth digits for 2024 (by ２０２４)'),
    ('from \uFF12\uFF10\uFF10\uFF10', 'fullwidth digits for 2000 (from ２０００)'),
    ('as of \uFF12\uFF10\uFF12\uFF10', 'fullwidth digits for 2020 (as of ２０２０)'),

    # Zero-width space (U+200B) injected between preposition and year.
    # This breaks word-boundary detection without being visually apparent.
    ('in\u200B2024', "zero-width space between 'in' and year (U+200B)"),
    ('since\u200B2019', "zero-width space between 'since' and year (U+200B)"),
    ('from\u200B2010', "zero-width space between 'from' and year (U+200B)"),

    # Zero-width space between preposition words in multi-word prepositions.
    ('as\u200Bof 2019', "zero-width space inside 'as of' (U+200B)"),
    ('prior\u200Bto 2010', "zero-width space inside 'prior to' (U+200B)"),
    ('back\u200Bto 1998', "zero-width space inside 'back to' (U+200B)"),

    # RTL override (U+202E) injected mid-expression.
    ('in \u202E2024', 'RTL override before year (U+202E)'),
    ('since \u202E2019', 'RTL override before year (U+202E)'),

    # Arabic-Indic digits (U+0660-U+0669).
    ('in \u0662\u0660\u0662\u0664', 'Arabic-Indic digits for 2024'),
    ('since \u0662\u0660\u0661\u0669', 'Arabic-Indic digits for 2019'),

    # Non-breaking space (U+00A0) in place of regular space between preposition and year.
    # A regex using literal \\s should match this (\\s includes U+00A0 in Python 3),
    # but one using a literal ASCII space (' ') will not.
    ('in\u00A02024', "non-breaking space between 'in' and year (U+00A0)"),
    ('since\u00A02019', "non-breaking space between 'since' and year (U+00A0)"),
    ('from\u00A02010', "non-breaking space between 'from' and year (U+00A0)"),
    ('as of\u00A02019', "non-breaking space after 'as of' (U+00A0)"),
    ('back to\u00A01998', "non-breaking space after 'back to' (U+00A0)"),
])
def test_prose_year_unicode(text, description):
    """
    Attack vector: Unicode homoglyphs and invisible characters in prose-year
    expressions -- specifically fullwidth digits, zero-width spaces, RTL
    override characters, Arabic-Indic numerals, and non-breaking spaces.

    Why a parser might be fooled by fullwidth digits: Python's ``re`` module with
    the default ``re.UNICODE`` flag matches fullwidth digits (U+FF10-U+FF19) via
    ``\\d``. A regex pattern ``\\d{4}`` will therefore match four fullwidth digits
    that look like a year. Whether this is desirable (maximum recall) or undesirable
    (strict ASCII-only matching) is a policy decision.

    Why a parser might be broken by zero-width space: a zero-width space (U+200B)
    inserted between the preposition and the year ('in\u200B2024') will cause a
    regex that uses ``\\s+`` to fail because U+200B is a word character boundary
    in some regex implementations. In Python 3, ``\\s`` does NOT match U+200B by
    default (it only matches Unicode-defined whitespace in category Zs), so
    'in\u200B2024' would cause the regex to not find a whitespace between 'in'
    and '2024', failing the match.

    Why non-breaking space matters: U+00A0 (NBSP) IS in Python's ``\\s`` class,
    so 'in\u00A02024' should match with a properly written ``\\s+`` separator.
    A regex using a literal space (' ') would miss it.

    This test records current behaviour without a directional assertion so the
    maintainer can decide the appropriate normalisation policy.

    Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
    """
    result = extract_explicit_dates(text)
    assert isinstance(result, dict)


# ============================================================================
# SECTION 11 -- ADDITIONAL TRUE POSITIVES (reaching 250+ total cases)
# ============================================================================

@pytest.mark.parametrize('text', [
    # Additional preposition × year combinations not covered in section 1.
    'in 2024',
    'in 2019',
    'in 2004',
    'in 2008',
    'in 2015',
    'in 2016',
    'in 2017',
    'in 2018',
    'in 2021',
    'in 2022',
    'in 2023',
    'in 2025',
    'in 2026',
    'in 2027',
    'in 2028',
    'in 2029',
    'in 2031',
    'in 2032',
    'in 2033',
    'in 2034',
    'in 2035',
    'in 2036',
    'in 1926',
    'in 1927',
    'in 1940',
    'in 1945',
    'in 1955',
    'in 1960',
    'in 1965',
    'in 1975',
    'in 1980',
    'in 1985',
    'in 1995',
    'in 1998',
    'since 2024',
    'since 2004',
    'since 2008',
    'since 2015',
    'since 2017',
    'since 2022',
    'since 1940',
    'since 1965',
    'since 1980',
    'circa 2019',
    'circa 2010',
    'circa 1970',
    'circa 1960',
    'circa 1945',
    'from 2019',
    'from 2004',
    'from 2008',
    'from 1970',
    'from 1960',
    'through 2024',
    'through 2019',
    'through 2010',
    'through 1990',
    'by 2019',
    'by 2010',
    'by 2004',
    'by 1990',
    'by 1960',
    'until 2019',
    'until 2024',
    'until 2010',
    'until 1990',
    'before 2019',
    'before 2010',
    'before 1990',
    'before 1970',
    'after 2019',
    'after 2010',
    'after 1990',
    'after 1970',
    'during 2019',
    'during 2010',
    'during 2004',
    'during 1990',
    'during 1970',
    'around 2024',
    'around 2010',
    'around 2004',
    'around 1990',
    'around 1970',
    'as of 2024',
    'as of 2004',
    'as of 2000',
    'as of 1990',
    'as of 1970',
    'back to 2010',
    'back to 2004',
    'back to 2000',
    'back to 1990',
    'back to 1970',
    'prior to 2024',
    'prior to 2019',
    'prior to 2004',
    'prior to 1990',
    'prior to 1970',
    # Embedded in longer sentences (additional variety).
    'the policy has been in place since 2010 and remains active',
    'changes during 2020 affected all departments',
    'completion is expected by 2030 or sooner',
    'established around 1970, the institution has grown',
    'regulations in force before 2004 were superseded',
    'growth after 2000 was particularly strong',
    'the project ran from 2015 through 2020',
    'as of 2024, the framework is considered mature',
    'dating back to 1990, the protocol remains relevant',
    'prior to 2010 no such requirement existed',
])
def test_prose_year_additional_true_positive(text):
    """
    Attack vector: additional preposition + year combinations spanning the full
    valid range, plus sentence-embedded examples for broader coverage.

    Why a parser might fail: the prose-year parser may have been tuned on a limited
    vocabulary of prepositions or a narrow year range. This section systematically
    exercises all prepositions across many different valid years to discover any
    coverage gaps not caught by the primary matrix in section 1.

    What failure reveals: a specific (preposition, year) combination that the parser
    does not handle, enabling targeted regex or pattern expansion.

    Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
    """
    result = extract_explicit_dates(text)
    assert len(result) > 0
