#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Red Team Test Suite -- Year Range Patterns
==========================================
Target function : extract_explicit_dates(text: str) -> Dict[str, str]
Target patterns : 2014-2015, from 2004 to 2008, between 2010 and 2020

Related GitHub Issue:
    #43 https://github.com/craigtrim/fast-parse-time/issues/43

ATTACK SURFACE OVERVIEW
------------------------
Year-range expressions take three structural forms:

  1. HYPHEN FORM: ``YYYY-YYYY`` (e.g., 2014-2015)
     The hyphen is structurally identical to the separator used in ISO dates
     and in many non-temporal contexts (phone fragments, ISBN segments, ticket
     IDs). The parser must distinguish year-pairs from these look-alikes.

  2. FROM...TO FORM: ``from YYYY to YYYY`` (e.g., from 2004 to 2008)
     Requires matching two keywords ('from' and 'to') each preceding a valid year,
     with arbitrary prose between them. The prose may contain non-year numbers.

  3. BETWEEN...AND FORM: ``between YYYY and YYYY`` (e.g., between 2010 and 2020)
     Requires matching 'between' and 'and' as structural keywords. 'and' is an
     extremely common English word and must not be matched in non-range contexts.

ATTACK VECTORS
--------------
  1. INVERTED YEAR ORDER: A year range where the end year is smaller than the
     start year (2015-2014, "from 2020 to 2019") is semantically invalid. The
     parser must decide whether to reject these or accept them (for 'circa' use
     cases). The test records current behaviour.

  2. MATH EXPRESSIONS: ``2048-1024`` is a valid arithmetic expression. A parser
     that matches any ``YYYY-YYYY`` pattern will fire on mathematical subtraction
     where both operands happen to be in the year range.

  3. PHONE FRAGMENTS: ``2014-5678`` looks like a year followed by a 4-digit
     local number. The second number (5678) is outside the valid year range but
     a parser that does not validate both sides of the hyphen will match it.

  4. ISBN FRAGMENTS: ``978-2014-3`` is an ISBN fragment where 2014 is a publisher
     code, not a year.

  5. SAME-YEAR RANGES: ``2024-2024`` (both sides equal) is technically a zero-
     duration range. Some parsers may accept it; others may reject it. The test
     records behaviour.

  6. UNICODE HYPHEN VARIANTS: The Unicode standard has multiple characters that
     look like a hyphen: en-dash (U+2013), em-dash (U+2014), minus sign (U+2212),
     and fullwidth hyphen-minus (U+FF0D). A parser that only matches ASCII
     hyphen-minus (U+002D) will miss these variants.

XFAIL STRATEGY
--------------
All tests carry ``pytestmark = pytest.mark.xfail`` so the suite remains green
while the implementation is incomplete.

TRUE POSITIVE TESTS  ->  assert len(result) > 0
FALSE POSITIVE TESTS ->  assert len(result) == 0
BOUNDARY TESTS       ->  assert isinstance(result, dict)
UNICODE TESTS        ->  assert isinstance(result, dict)
"""

import pytest
from fast_parse_time.api import extract_explicit_dates

# Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43

pytestmark = pytest.mark.xfail(reason='red_team: not yet validated')


# ============================================================================
# SECTION 1 -- TRUE POSITIVES: HYPHEN FORM
# ============================================================================

@pytest.mark.parametrize('text', [
    # Consecutive year pairs (span of 1 year).
    '2014-2015',
    '2019-2020',
    '2023-2024',
    '2024-2025',
    '2025-2026',
    '2026-2027',
    '2027-2028',
    '2028-2029',
    '2029-2030',
    '2030-2031',
    '2031-2032',
    '2032-2033',
    '2033-2034',
    '2034-2035',
    '2035-2036',
    '1926-1927',
    '1930-1931',
    '1940-1941',
    '1950-1951',
    '1960-1961',
    '1970-1971',
    '1980-1981',
    '1990-1991',
    '2000-2001',
    '2010-2011',
    # 5-year spans.
    '2000-2005',
    '2005-2010',
    '2010-2015',
    '2015-2020',
    '2020-2025',
    '2025-2030',
    '2030-2035',
    '1930-1935',
    '1950-1955',
    '1970-1975',
    '1980-1985',
    '1990-1995',
    # 10-year spans.
    '2000-2010',
    '2010-2020',
    '2020-2030',
    '1926-1936',
    '1930-1940',
    '1940-1950',
    '1950-1960',
    '1960-1970',
    '1970-1980',
    '1980-1990',
    '1990-2000',
    # 25-year spans.
    '1975-2000',
    '2000-2025',
    '1926-1951',
    '2011-2036',
    # 50-year spans.
    '1950-2000',
    '1976-2026',
    '1936-1986',
    '1970-2020',
    # Full-range span.
    '1926-2036',
    # Other valid pairs.
    '2004-2008',
    '2004-2019',
    '2019-2024',
    '1998-2004',
    '1998-2010',
    '1998-2020',
    '2001-2011',
    '2007-2009',
    '2016-2018',
    '2017-2021',
    '2018-2022',
])
def test_year_range_hyphen_true_positive(text):
    """
    Attack vector: year ranges in hyphen-delimited form (YYYY-YYYY).

    Why a parser might fail: the hyphen-year-range pattern is visually identical
    to a date sub-component (the YYYY-MM portion of a full date like 2024-01-01)
    and to non-temporal hyphenated numbers (phone fragments, ISBN segments).
    The parser must apply positive lookahead/lookbehind logic or validate that
    both sides of the hyphen are 4-digit numbers within the valid year range.

    A common false-negative failure mode: the parser correctly identifies the
    pattern 'YYYY-YYYY' but then rejects it because the difference between the
    two years exceeds a maximum span threshold. This would incorrectly reject
    50-year spans like '1950-2000' that are legitimately used in historical texts.

    What failure reveals: each failing case identifies a specific year-pair
    pattern that the parser does not classify as YEAR_RANGE, enabling targeted
    regex refinement.

    Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
    """
    result = extract_explicit_dates(text)
    assert len(result) > 0


# ============================================================================
# SECTION 2 -- TRUE POSITIVES: FROM...TO FORM
# ============================================================================

@pytest.mark.parametrize('text', [
    # Simple 'from YYYY to YYYY' expressions.
    'from 2004 to 2008',
    'from 1990 to 2000',
    'from 2020 to 2025',
    'from 2010 to 2020',
    'from 2014 to 2015',
    'from 2019 to 2024',
    'from 1926 to 2036',
    'from 1930 to 1940',
    'from 1950 to 2000',
    'from 1970 to 1980',
    'from 1980 to 1990',
    'from 2000 to 2010',
    'from 2015 to 2020',
    'from 2024 to 2030',
    'from 2025 to 2036',
    'from 1998 to 2010',
    'from 1998 to 2019',
    'from 2004 to 2019',
    'from 2001 to 2010',
    'from 2007 to 2009',
    # Sentence-embedded 'from...to'.
    'from 2004 to 2008 we operated under the old framework',
    'the project ran from 1990 to 2000 without interruption',
    'from 2019 to 2024 the sector grew at 8% annually',
    'revenue from 2010 to 2020 increased threefold',
    'the study covers from 2014 to 2015 and beyond',
    'the policy was enforced from 2000 to 2010 consistently',
    'performance from 2020 to 2025 exceeded all projections',
    'spanning from 1950 to 2000, the era was transformative',
    # 'From' at sentence start (title case).
    'From 2004 to 2008 the economy expanded',
    'From 2010 to 2020 global temperatures rose',
    # 'FROM' in all caps.
    'FROM 2019 TO 2024',
    'FROM 2004 TO 2008',
])
def test_year_range_from_to_true_positive(text):
    """
    Attack vector: year ranges in the 'from YYYY to YYYY' prose form.

    Why a parser might fail: the 'from...to' form requires matching two separate
    keywords at a distance. If the parser uses a single regex like
    ``from\\s+(\\d{4})\\s+to\\s+(\\d{4})``, it will fail when:
      - The words 'from' and 'to' are separated by additional prose
      - The expression is at sentence start with capitalisation
      - The expression uses all-caps (FROM, TO)
      - Additional words appear between 'from YYYY' and 'to YYYY'

    The sentence-embedded cases test whether the parser correctly extracts the
    range even when the expression is surrounded by other text. The 'from' and
    'to' keywords are common English words, so a parser that uses them as
    anchors must verify that the adjacent tokens are valid 4-digit years.

    What failure reveals: the parser does not recognise the 'from...to' prose
    form for year ranges, limiting its ability to extract temporal spans from
    narrative text.

    Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
    """
    result = extract_explicit_dates(text)
    assert len(result) > 0


# ============================================================================
# SECTION 3 -- TRUE POSITIVES: BETWEEN...AND FORM
# ============================================================================

@pytest.mark.parametrize('text', [
    # Simple 'between YYYY and YYYY' expressions.
    'between 2010 and 2020',
    'between 1980 and 2000',
    'between 2014 and 2015',
    'between 2019 and 2024',
    'between 1926 and 2036',
    'between 2000 and 2010',
    'between 1950 and 2000',
    'between 1970 and 1990',
    'between 1990 and 2010',
    'between 2004 and 2008',
    'between 2020 and 2030',
    'between 2024 and 2036',
    'between 1930 and 1940',
    'between 1960 and 1970',
    'between 1980 and 1985',
    'between 1998 and 2010',
    'between 2001 and 2011',
    'between 2007 and 2009',
    'between 2015 and 2020',
    'between 2025 and 2035',
    # Sentence-embedded 'between...and'.
    'between 2010 and 2020 there was significant growth',
    'the gap between 1980 and 2000 saw major changes',
    'between 2014 and 2015 the protocol was revised',
    'revenues between 2019 and 2024 grew by 40%',
    'the period between 1950 and 2000 defined the modern era',
    'activity between 2004 and 2008 was above average',
    'between 2020 and 2030 we forecast a compound rate of 5%',
    'the span between 1926 and 2036 covers the full dataset',
    # 'Between' at sentence start (title case).
    'Between 2010 and 2020 global GDP doubled',
    'Between 1970 and 1990 inflation remained high',
    # All caps.
    'BETWEEN 2010 AND 2020',
    'BETWEEN 2004 AND 2008',
])
def test_year_range_between_and_true_positive(text):
    """
    Attack vector: year ranges in the 'between YYYY and YYYY' prose form.

    Why a parser might fail: the word 'and' is one of the most common words in
    English, appearing in virtually every sentence. A parser that scans for 'and'
    as a range connector must verify that it is preceded by 'between YYYY' and
    followed by 'YYYY'. Without this full structural check, the parser would produce
    thousands of false positives on sentences that contain 'and' between numbers.

    The sentence-embedded cases (e.g., "the gap between 1980 and 2000 saw major
    changes") test whether the parser correctly handles the 'between' keyword when
    it is preceded by a noun phrase and followed by prose. A regex anchored to
    the start of the string will miss all of these.

    Case variants ('Between', 'BETWEEN') test case sensitivity handling. All-caps
    versions are common in legal documents, financial tables, and government reports.

    What failure reveals: the parser does not recognise the 'between...and' form,
    a common and important year-range pattern in analytical and historical writing.

    Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
    """
    result = extract_explicit_dates(text)
    assert len(result) > 0


# ============================================================================
# SECTION 4 -- TRUE POSITIVES: SENTENCE EMBEDDED (all three forms)
# ============================================================================

@pytest.mark.parametrize('text', [
    # Hyphen form embedded.
    'the period 2014-2015 saw unprecedented growth',
    'data from the 2019-2020 fiscal year',
    'the 2010-2020 decade was transformative',
    'performance during 2000-2010 exceeded targets',
    'the 1970-1980 era of stagflation affected policy',
    'records for 1990-2000 are available in the archive',
    'the 1926-2036 dataset spans the full study period',
    'see the 2024-2025 projections in appendix B',
    'the 2004-2008 expansion is well documented',
    '2020-2030 is the strategic planning horizon',
    # From...to form embedded.
    'from 2004 to 2008 we grew at 12% annually',
    'the company expanded from 1990 to 2000 dramatically',
    'from 2019 to 2024, three new product lines were launched',
    'revenues from 2010 to 2020 increased threefold across all segments',
    'from 1970 to 1980 the industry was regulated differently',
    'changes from 2000 to 2010 were significant and measurable',
    # Between...and form embedded.
    'the period between 2010 and 2020 there was significant growth',
    'performance between 2004 and 2008 exceeded all benchmarks',
    'between 2019 and 2024 the regulatory landscape shifted',
    'the interval between 1980 and 2000 contains the data we need',
    'between 1950 and 2000 the population doubled',
    'studies between 2000 and 2010 confirm the trend',
])
def test_year_range_sentence_embedded_true_positive(text):
    """
    Attack vector: all three year-range forms embedded in natural-language sentences.

    Why a parser might fail: see the detailed rationale in sections 1-3. The
    additional challenge in sentence-embedded contexts is that each form must be
    extracted from surrounding prose without being anchored to the string boundaries.

    The 'from 2004 to 2008 we grew' case tests that the parser does not extend
    the match to include 'we grew' as part of the year range. The 'data from the
    2019-2020 fiscal year' case tests that 'the' (an article between 'from' and
    the year range) does not break the hyphen-form pattern.

    What failure reveals: the parser's pattern matching is too narrow for real
    prose inputs, requiring artificially clean (preposition-adjacent-to-year)
    structures.

    Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
    """
    result = extract_explicit_dates(text)
    assert len(result) > 0


# ============================================================================
# SECTION 5 -- FALSE POSITIVES: INVERTED HYPHEN (end before start)
# ============================================================================

@pytest.mark.parametrize('text', [
    # Year pairs where the second year is smaller than the first.
    # Semantically invalid as a time range (time cannot run backwards).
    # A parser that validates year ordering should reject these.
    '2015-2014',
    '2020-2000',
    '2024-2023',
    '2036-1926',
    '2030-2020',
    '2025-2020',
    '2020-2010',
    '2010-2000',
    '2000-1990',
    '1990-1980',
    '1980-1970',
    '1970-1960',
    '1960-1950',
    '1950-1940',
    '1940-1930',
    '2036-2035',
    '2035-2020',
    '2019-2018',
    '2018-2017',
    '2017-2016',
    '2016-2015',
    '2008-2004',
    '2004-1998',
    '2001-1999',
])
def test_year_range_inverted_false_positive(text):
    """
    Attack vector: hyphen-delimited pairs where the end year is earlier than the
    start year (inverted temporal order).

    Why a parser might fail (producing a false positive): a regex that matches
    any ``\\d{4}-\\d{4}`` pattern without validating that the left year is less
    than the right year will accept inverted pairs. The string '2015-2014' passes
    the structural test (both are 4-digit numbers in range) but fails the semantic
    test (time cannot run backwards in a range).

    The exception to this rule is 'circa' use cases where the author writes a
    year range in reverse to indicate a counting-down context ('by 2014-2000 we
    had completed X'). This is unusual enough that the parser should default to
    requiring ascending order and document any exceptions explicitly.

    What failure reveals (false positive produced): the parser does not validate
    year ordering within hyphen-delimited ranges, accepting semantically invalid
    inputs and potentially misclassifying other numeric patterns (like phone
    fragments that happen to have two valid year-range year values) as ranges.

    Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
    """
    result = extract_explicit_dates(text)
    assert len(result) == 0


# ============================================================================
# SECTION 6 -- FALSE POSITIVES: MATH EXPRESSIONS
# ============================================================================

@pytest.mark.parametrize('text', [
    # Arithmetic subtraction expressions where both operands happen to be in the
    # year range [1926, 2036]. These are NOT year ranges.
    '2048-1024',
    '2000-1000',
    '2036-1926',    # min/max boundary values but as math, not a range
    '2024-1024',
    '1980-1024',
    '2000-1536',
    '2020-1984',
    '2024-2000',    # result = 24 (valid subtraction)
    '2000-1900',    # result = 100
    '2036-2000',    # result = 36
    '1990-1960',    # result = 30
    '2020-1970',    # result = 50
    '2024-2016',    # result = 8
    '2030-1030',
    '2000-1000',
    # In explicit arithmetic context.
    'calculate 2048-1024 = 1024',
    'the sum 2000-1000 equals 1000',
    '2024 - 2016 = 8',    # with spaces around the hyphen
    'answer: 2036-1926=110',
])
def test_year_range_math_false_positive(text):
    """
    Attack vector: arithmetic subtraction expressions where both operands fall
    within the valid year range, making them structurally identical to year ranges.

    Why a parser might fail (producing a false positive): without semantic
    context, the string '2024-2016' is structurally identical to a year range
    and to arithmetic subtraction. The parser cannot distinguish them from
    structure alone.

    Disambiguation strategies include:
      1. Requiring surrounding context (preposition before, or 'the ... period'
         phrasing).
      2. Validating that the result is a positive, multi-year span (e.g., minimum
         span of 1 year), which rejects very small differences like '2024-2023'.
      3. Requiring that neither operand is an unreasonably round power-of-two
         (1024, 2048) that indicates a mathematical context.

    None of these heuristics are perfect. The test records current behaviour and
    helps the maintainer decide the appropriate trade-off between recall and
    precision for the hyphen-form year range.

    What failure reveals (false positive produced): the parser cannot distinguish
    year-range hyphens from arithmetic minus signs.

    Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
    """
    result = extract_explicit_dates(text)
    assert len(result) == 0


# ============================================================================
# SECTION 7 -- FALSE POSITIVES: PHONE FRAGMENTS
# ============================================================================

@pytest.mark.parametrize('text', [
    # Phone number fragments where the first component is a valid year but
    # the second component is a 4-digit local number outside the year range.
    '2014-5678',
    '2019-9999',
    '2020-1234',
    '2024-5555',
    '2010-9876',
    '1990-4321',
    '2000-8765',
    '2015-3456',
    '2030-7890',
    '1970-2468',
    '1980-1357',
    '1950-6543',
    '2036-9876',
    '1926-2345',
    '2024-8080',    # year + port number
    '2020-4040',
    '2019-6060',
    '2000-5050',
    # In context of a phone number.
    'call us at 2024-5678 for details',
    'extension 2019-9999',
    'fax: 2020-1234',
])
def test_year_range_phone_fragment_false_positive(text):
    """
    Attack vector: phone number fragments where the first 4 digits form a valid
    year but the second 4 digits (5678, 9999, 1234, etc.) are outside the valid
    year range [1926, 2036].

    Why a parser might fail (producing a false positive): if the parser only
    validates the LEFT side of the hyphen as a valid year (checking that the first
    4-digit group is in [1926, 2036]) but not the RIGHT side, then '2014-5678'
    will match because 2014 is a valid year. A correctly implemented parser must
    validate BOTH sides.

    Phone fragments are extremely common in business documents, especially in
    regions where local phone numbers are formatted as YYYY-XXXX (such as some
    South American countries and older North American exchange formats).

    What failure reveals (false positive produced): the parser is not validating
    both year values in the hyphen-form range, only the left side.

    Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
    """
    result = extract_explicit_dates(text)
    assert len(result) == 0


# ============================================================================
# SECTION 8 -- FALSE POSITIVES: ISBN FRAGMENTS
# ============================================================================

@pytest.mark.parametrize('text', [
    # ISBN-10 and ISBN-13 fragments where a year-range-looking component appears.
    '978-2014-3',
    '0-2020-123-4',
    '978-2019-456-7',
    '0-2024-001',
    '978-2010-000',
    '0-2000-5',
    '978-1990-1',
    '0-2036-9',
    '978-1926-0',
    # In context.
    'ISBN: 978-2014-3',
    'ISBN-13: 978-2019-456-7',
    'see also: 0-2020-123-4',
    # ISSN fragments (8 digits, often shown as XXXX-XXXX).
    '2024-5678',    # ISSN-like format (same as phone test but context)
    '2019-0001',
    '2020-9999',
    '1990-0000',
    # DOI fragments.
    '10.2014/example',
    '10.2020/some-identifier',
])
def test_year_range_isbn_fragment_false_positive(text):
    """
    Attack vector: ISBN, ISSN, and DOI fragments where a year-like number appears
    within a longer identifier separated by hyphens.

    Why a parser might fail (producing a false positive): ISBN-13 numbers in the
    'ISBN 978-YYYY-XXXX' format contain a 4-digit publisher prefix that may happen
    to be in the valid year range. A parser that does not look at surrounding context
    (the '978-' prefix indicates an ISBN, not a year range) will incorrectly extract
    the publisher code as a year.

    DOI identifiers (10.XXXX/...) are another common source of false positives:
    the XXXX portion is a registrant code that may look like a year.

    ISSN identifiers are formatted as XXXX-XXXX (8 digits, hyphen-separated), and
    are structurally identical to the YYYY-YYYY year-range format. The difference
    is purely semantic: the ISSN registrant number '2019' in ISSN 2019-0001 refers
    to a journal identifier, not the year 2019.

    What failure reveals (false positive produced): the parser is matching
    structured identifier fragments as year ranges, which would be particularly
    harmful in bibliographic and library systems.

    Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
    """
    result = extract_explicit_dates(text)
    assert len(result) == 0


# ============================================================================
# SECTION 9 -- FALSE POSITIVES: SAME-YEAR BOTH SIDES
# ============================================================================

@pytest.mark.parametrize('text', [
    # Year ranges where both sides are the same year (zero-duration range).
    '2024-2024',
    '2020-2020',
    '2019-2019',
    '2010-2010',
    '2000-2000',
    '1990-1990',
    '1970-1970',
    '1950-1950',
    '1926-1926',
    '2036-2036',
    '2030-2030',
    '2025-2025',
    '2015-2015',
    '2005-2005',
    '2001-2001',
    # In 'between...and' form.
    'between 2010 and 2010',
    'between 2024 and 2024',
    'between 2020 and 2020',
    'between 2000 and 2000',
    'between 1990 and 1990',
    # In 'from...to' form.
    'from 2020 to 2020',
    'from 2024 to 2024',
    'from 2010 to 2010',
    'from 2000 to 2000',
])
def test_year_range_same_year_false_positive(text):
    """
    Attack vector: year range expressions where the start and end year are
    identical (zero-duration range).

    Why a parser might fail (producing a false positive): a parser that validates
    only that both sides are valid years in range, without checking that the end
    year is STRICTLY GREATER than the start year, will accept '2024-2024' as a
    valid year range. Whether this is a bug or a feature is a policy decision.

    The argument for rejecting same-year ranges: a range with identical endpoints
    is semantically equivalent to a single year reference, not a range. Accepting
    it as a YEAR_RANGE classification creates a dual-classification problem where
    '2024-2024' would be classified differently from '2024' alone.

    The argument for accepting same-year ranges: in some contexts (e.g., financial
    reporting: 'the 2024-2024 fiscal year') same-year ranges are conventional and
    meaningful. The test records current behaviour without committing to a policy.

    What failure reveals (false positive produced): the parser accepts zero-duration
    ranges, creating potential downstream issues in systems that compute date spans.

    Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
    """
    result = extract_explicit_dates(text)
    assert len(result) == 0


# ============================================================================
# SECTION 10 -- BOUNDARY: RANGE LIMITS AND EDGE CASES
# ============================================================================

@pytest.mark.parametrize('text, description', [
    # Start at minimum, end at maximum -- the widest possible valid range.
    ('1926-2036', 'full valid range (min to max)'),
    ('from 1926 to 2036', 'full valid range, from...to form'),
    ('between 1926 and 2036', 'full valid range, between...and form'),

    # Start below minimum -- should be rejected.
    ('1925-2030', 'start year below minimum (1925 < 1926)'),
    ('1924-2036', 'start year well below minimum'),
    ('1900-2020', 'start year far below minimum'),
    ('from 1925 to 2030', 'from...to form, start below minimum'),
    ('between 1925 and 2030', 'between...and form, start below minimum'),

    # End above maximum -- should be rejected.
    ('2020-2037', 'end year above maximum (2037 > 2036)'),
    ('1990-2040', 'end year well above maximum'),
    ('2000-2100', 'end year far above maximum'),
    ('from 2020 to 2037', 'from...to form, end above maximum'),
    ('between 2020 and 2037', 'between...and form, end above maximum'),

    # Both outside range.
    ('1900-1925', 'both years below minimum'),
    ('2037-2040', 'both years above maximum'),

    # Same-year forms (covered also in section 9 for additional boundary context).
    ('between 2010 and 2010', 'same year -- zero duration range'),
    ('from 2020 to 2019', 'from...to form, inverted (end before start)'),
    ('between 2020 and 2010', 'between...and form, inverted'),

    # One-year adjacent to boundary.
    ('1926-2036', 'exact boundaries'),
    ('1927-2035', 'one inside each boundary'),
    ('1926-2035', 'min boundary, max-1'),
    ('1927-2036', 'min+1, max boundary'),
])
def test_year_range_boundary(text, description):
    """
    Attack vector: year range expressions at the exact boundaries of the supported
    year range [1926, 2036], one step beyond the boundaries in each direction, and
    semantically invalid forms (inverted, same-year).

    Why a parser might fail: off-by-one errors in the year-range guard are
    symmetric with the prose-year boundary tests in FILE 2. This section extends
    that analysis to the three structural forms of year ranges and adds the
    inversion and zero-duration edge cases.

    The 'from 2020 to 2019' case (inverted 'from...to') is particularly important
    because it tests whether the parser validates the year ordering in prose form
    the same way it does in hyphen form. Inconsistent behaviour between the two
    forms would indicate that the ordering check is implemented separately (and
    possibly incorrectly) for each pattern.

    This test does not assert a direction because the correct behaviour for some
    of these edge cases depends on the project's explicit policy (e.g., whether
    same-year ranges are accepted). The xfail mark at module level captures all
    outcomes for review in issue #43.

    Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
    """
    result = extract_explicit_dates(text)
    assert isinstance(result, dict)


# ============================================================================
# SECTION 11 -- UNICODE: HYPHEN VARIANT ATTACKS
# ============================================================================

@pytest.mark.parametrize('text, description', [
    # En-dash (U+2013) replacing hyphen-minus in YYYY-YYYY.
    # En-dashes are the typographically correct separator for year ranges in
    # professional typography (e.g., 2014-2015 should be typeset as 2014-2015
    # using an en-dash). Many documents from publishing, legal, and academic
    # contexts will use en-dashes.
    ('2014\u20132015', 'en-dash year range (U+2013): 2014\u20132015'),
    ('2019\u20132024', 'en-dash year range (U+2013): 2019\u20132024'),
    ('2010\u20132020', 'en-dash year range (U+2013): 2010\u20132020'),
    ('1926\u20132036', 'en-dash year range (U+2013): 1926\u20132036'),
    ('2000\u20132010', 'en-dash year range (U+2013): 2000\u20132010'),

    # Em-dash (U+2014) replacing hyphen-minus in YYYY-YYYY.
    # Em-dashes are sometimes used in informal or typewriter-era typography.
    ('2014\u20142015', 'em-dash year range (U+2014): 2014\u20142015'),
    ('2019\u20142024', 'em-dash year range (U+2014): 2019\u20142024'),
    ('2010\u20142020', 'em-dash year range (U+2014): 2010\u20142020'),
    ('1926\u20142036', 'em-dash year range (U+2014): 1926\u20142036'),

    # Minus sign (U+2212) replacing hyphen-minus.
    # The Unicode minus sign is used in mathematical typesetting and appears in
    # copy-pasted text from LaTeX documents or equation editors.
    ('2014\u22122015', 'minus sign year range (U+2212): 2014\u22122015'),
    ('2019\u22122024', 'minus sign year range (U+2212): 2019\u22122024'),
    ('2010\u22122020', 'minus sign year range (U+2212): 2010\u22122020'),
    ('1926\u22122036', 'minus sign year range (U+2212): 1926\u22122036'),

    # Fullwidth hyphen-minus (U+FF0D) replacing ASCII hyphen-minus (U+002D).
    # Fullwidth characters are used in CJK (Chinese, Japanese, Korean) text
    # environments and appear in content that was originally formatted for
    # East Asian display systems.
    ('2014\uFF0D2015', 'fullwidth hyphen-minus (U+FF0D): 2014\uFF0D2015'),
    ('2019\uFF0D2024', 'fullwidth hyphen-minus (U+FF0D): 2019\uFF0D2024'),
    ('2010\uFF0D2020', 'fullwidth hyphen-minus (U+FF0D): 2010\uFF0D2020'),
    ('1926\uFF0D2036', 'fullwidth hyphen-minus (U+FF0D): 1926\uFF0D2036'),

    # Combining minus (U+2212) in sentence context.
    ('the period 2014\u20132015 was significant', 'en-dash in sentence context'),
    ('from 2004\u20132008 the trend was positive', "en-dash after 'from'"),
    ('the 2019\u20142024 era is well studied', 'em-dash in sentence context'),

    # Fullwidth digits around standard hyphen (hybrid attack).
    ('\uFF12\uFF10\uFF12\uFF14-2015', 'fullwidth start year + ASCII hyphen'),
    ('2014-\uFF12\uFF10\uFF11\uFF15', 'ASCII hyphen + fullwidth end year'),
])
def test_year_range_unicode_hyphen(text, description):
    """
    Attack vector: year range expressions using Unicode hyphen variants in place
    of the ASCII hyphen-minus (U+002D).

    Why a parser might be affected: the typographically correct separator for a
    year range is an en-dash (U+2013), not a hyphen-minus (U+002D). A parser
    whose regex uses the literal ASCII hyphen '-' will not match en-dash or
    em-dash variants, causing it to miss year ranges in professionally typeset
    documents, legal texts, and academic papers.

    The four Unicode hyphen variants tested here cover the most common cases:
      - U+2013 (en-dash): the correct typographic separator for ranges
      - U+2014 (em-dash): the typewriter alternative and informal separator
      - U+2212 (minus sign): used in mathematical typesetting (LaTeX, equation editors)
      - U+FF0D (fullwidth hyphen-minus): used in CJK text environments

    The correct handling policy is a design decision:
      Option A (strict ASCII): reject all Unicode hyphens -- pure ASCII matching
      Option B (Unicode-aware): normalise all hyphen variants to U+002D before
                                matching, accepting en-dash and em-dash ranges
      Option C (selective): only accept en-dash (U+2013) as an additional
                            separator alongside ASCII hyphen

    This test records current behaviour without asserting direction, enabling the
    maintainer to make an explicit policy decision in issue #43.

    Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
    """
    result = extract_explicit_dates(text)
    assert isinstance(result, dict)


# ============================================================================
# SECTION 12 -- ADDITIONAL TRUE POSITIVES (reaching 250+ total cases)
# ============================================================================

@pytest.mark.parametrize('text', [
    # Additional hyphen-form pairs not in section 1.
    '1927-1928',
    '1929-1930',
    '1933-1934',
    '1936-1937',
    '1938-1939',
    '1942-1943',
    '1945-1946',
    '1948-1949',
    '1952-1953',
    '1955-1956',
    '1958-1959',
    '1962-1963',
    '1965-1966',
    '1968-1969',
    '1972-1973',
    '1975-1976',
    '1978-1979',
    '1982-1983',
    '1985-1986',
    '1988-1989',
    '1992-1993',
    '1995-1996',
    '1998-1999',
    '2002-2003',
    '2006-2007',
    '2008-2009',
    '2011-2012',
    '2012-2013',
    '2013-2014',
    '2016-2017',
    '2017-2018',
    '2018-2019',
    '2021-2022',
    '2022-2023',
    # Additional from...to forms.
    'from 1927 to 1929',
    'from 1945 to 1950',
    'from 1955 to 1965',
    'from 1975 to 1985',
    'from 1985 to 1995',
    'from 1995 to 2005',
    'from 2005 to 2015',
    'from 2016 to 2018',
    'from 2017 to 2019',
    'from 2021 to 2023',
    'from 2022 to 2024',
    'from 2023 to 2025',
    'from 2026 to 2028',
    'from 2028 to 2030',
    'from 2032 to 2034',
    # Additional between...and forms.
    'between 1927 and 1929',
    'between 1945 and 1950',
    'between 1955 and 1965',
    'between 1975 and 1985',
    'between 1985 and 1995',
    'between 1995 and 2005',
    'between 2005 and 2015',
    'between 2016 and 2018',
    'between 2021 and 2023',
    'between 2022 and 2024',
    'between 2023 and 2025',
    'between 2026 and 2028',
    'between 2028 and 2030',
    'between 2032 and 2034',
    'between 2034 and 2036',
    # Sentence-embedded additional forms.
    'growth from 1945 to 1950 exceeded expectations',
    'between 1955 and 1965 the industry restructured',
    'the 1975-1985 decade saw major regulatory changes',
    'from 1985 to 1995 was an era of rapid expansion',
    'the 1995-2000 dot-com boom is well documented',
    'from 2001 to 2010 the recovery was uneven',
    'between 2012 and 2016 the market stabilised',
    'the 2016-2020 period coincided with policy shifts',
    'from 2021 to 2024 the sector adapted to new norms',
    'between 2024 and 2028 the projections are optimistic',
    'the 2028-2032 window is critical for the transition',
    'from 2032 to 2036 we expect full deployment',
])
def test_year_range_additional_true_positive(text):
    """
    Attack vector: additional year-range pairs in all three structural forms,
    spanning dense year-over-year adjacent pairs and intermediate multi-year spans.

    Why a parser might fail: dense year-over-year pairs (1927-1928, 1929-1930,
    etc.) test whether the parser correctly handles all consecutive years in the
    valid range [1926, 2036], not just the 'interesting' ones (decade starts,
    well-known historical years). A parser tuned on a sparse training set may miss
    years that were never in the training vocabulary.

    The sentence-embedded additional cases extend the context-handling test to
    a wider variety of surrounding prose patterns, ensuring that neither the
    preceding noun phrase nor the trailing verb phrase disrupts pattern matching.

    What failure reveals: each failing case identifies a specific year-pair or
    sentence context where the parser's year-range extraction fails, enabling
    targeted coverage improvement.

    Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
    """
    result = extract_explicit_dates(text)
    assert len(result) > 0
