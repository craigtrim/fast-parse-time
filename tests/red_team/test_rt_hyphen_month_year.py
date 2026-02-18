#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Red Team: Hyphen-Month-Year Patterns
======================================
This module adversarially probes the fast-parse-time parser handling of
date expressions that join a month name or abbreviation to a two-digit or
four-digit year using a hyphen delimiter. The canonical forms targeted are:

  Forward (MONTH_YEAR):   Oct-23, Oct-2023, March-2023
  Reversed (YEAR_MONTH):  23-Oct, 2023-Oct
  Full month names:       January-2023, December-2023

These patterns are prevalent in:
  - Financial reporting headers (Jan-24 P&L, Q3-23 summary)
  - Log file timestamps (Oct-23 audit log)
  - Abbreviated table column headers (Nov-23 | Dec-23 | Jan-24)
  - Database exports and ETL pipeline metadata

The primary adversarial challenge is disambiguation from a large class of
hyphen-joined token pairs that share the same surface structure but carry
no date meaning:
  - Day-of-week prefixes: Sun-23, Mon-23, Tue-23
  - Quarter identifiers: Q1-23, Q2-23, Q3-23, Q4-23
  - Version strings: v1-23, v2-23, v10-23
  - Prefix+year compounds: pre-2023, post-2023, non-2023

A secondary challenge is the Unicode hyphen family: the ASCII hyphen-minus
(U+002D) is the intended delimiter, but typographers frequently substitute
non-breaking hyphen (U+2011), en-dash (U+2013), em-dash (U+2014), or the
invisible soft hyphen (U+00AD).

Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
"""

import pytest
from fast_parse_time import extract_explicit_dates

pytestmark = pytest.mark.xfail(reason='red_team: not yet validated')


# ===========================================================================
# SECTION 1 -- TRUE POSITIVES: ALL 12 ABBREVIATED MONTHS FORWARD (Abbrev-YY)
# ===========================================================================

@pytest.mark.parametrize('text', [
    # Abbreviated month + hyphen + 2-digit year. This is the most compact
    # MONTH_YEAR format and appears extensively in financial reporting,
    # spreadsheet column headers, and time-series data.
    'Jan-23',
    'Feb-23',
    'Mar-23',
    'Apr-23',
    'May-23',
    'Jun-23',
    'Jul-23',
    'Aug-23',
    'Sep-23',
    'Sept-23',
    'Oct-23',
    'Nov-23',
    'Dec-23',
    # Additional 2-digit year variants
    'Jan-00',
    'Jan-99',
    'Jan-24',
    'Feb-24',
    'Mar-24',
    'Apr-24',
    'May-24',
    'Jun-24',
    'Jul-24',
    'Aug-24',
    'Sep-24',
    'Oct-24',
    'Nov-24',
    'Dec-24',
    # In sentence context
    'The report for Jan-23 is attached.',
    'Review the Feb-23 figures.',
    'Submit by Mar-23 deadline.',
    'Data from Apr-23 needs review.',
    'The May-23 audit is complete.',
    'June invoices: Jun-23.',
    'Quarterly: Jul-23.',
    'See Aug-23 summary.',
    'Filed Sep-23.',
    'Submitted Oct-23.',
    'Balance for Nov-23.',
    'Year-end Dec-23 report.',
    # Additional year variants
    'Jan-26',
    'Dec-36',
    'Oct-22',
    'Mar-19',
    'Jul-15',
    'Nov-10',
    'Feb-05',
    'Apr-00',
    'Jun-98',
    'Aug-95',
    'Sep-90',
    'May-85',
])
def test_true_positive_abbrev_months_forward_2digit(text):
    """
    True positive: abbreviated month + hyphen + 2-digit year (forward order).

    Attack vector: The Abbrev-YY format is the most compact written MONTH_YEAR
    date expression. It is extremely common in financial tables, audit trails,
    and report headers. The 2-digit year introduces ambiguity about the century
    (Jan-23 = January 2023 vs January 1923), but within the supported year
    range [1926, 2036], the century assignment can be inferred by convention.

    Why a parser might fail: The parser may require a 4-digit year and reject
    2-digit years entirely. Alternatively, the 2-digit year pattern may be
    matched by a less specific rule that does not validate the month component,
    or the month abbreviation lookup may be incomplete.

    Failure reveals: The 2-digit year variant of the MONTH_YEAR extractor is
    absent, or the month abbreviation table is missing entries.
    """
    result = extract_explicit_dates(text)
    assert len(result) > 0


# ===========================================================================
# SECTION 2 -- TRUE POSITIVES: ALL 12 ABBREVIATED MONTHS WITH 4-DIGIT YEAR
# ===========================================================================

@pytest.mark.parametrize('text', [
    # Abbreviated month + hyphen + 4-digit year. The 4-digit year removes
    # century ambiguity and is the more explicit variant of the format.
    'Jan-2023',
    'Feb-2023',
    'Mar-2023',
    'Apr-2023',
    'May-2023',
    'Jun-2023',
    'Jul-2023',
    'Aug-2023',
    'Sep-2023',
    'Sept-2023',
    'Oct-2023',
    'Nov-2023',
    'Dec-2023',
    # Different years across the valid range
    'Jan-1926',
    'Dec-2036',
    'Oct-2024',
    'Mar-2025',
    'Jul-2030',
    'Nov-1980',
    'Feb-2000',
    'Apr-1999',
    'Jun-2010',
    'Aug-2015',
    'Sep-2018',
    'May-2019',
    # Additional variants
    'Jan-2024',
    'Feb-2024',
    'Mar-2024',
    'Apr-2024',
    'May-2024',
    'Jun-2024',
    'Jul-2024',
    'Aug-2024',
    'Sep-2024',
    'Oct-2024',
    'Nov-2024',
    'Dec-2024',
    # Sentence embedded
    'The Jan-2023 report is final.',
    'See Feb-2023 for prior period.',
    'The Mar-2023 quarter is closed.',
    'Apr-2023 data has been reconciled.',
    'May-2023 invoices are archived.',
    'Jun-2023 closing balance confirmed.',
    'Jul-2023 was the peak month.',
    'Aug-2023 showed a decline.',
    'Sep-2023 recovered strongly.',
    'Oct-2023 is the reference period.',
    'Nov-2023 figures are preliminary.',
    'Dec-2023 year-end data is final.',
])
def test_true_positive_abbrev_months_forward_4digit(text):
    """
    True positive: abbreviated month + hyphen + 4-digit year (forward order).

    Attack vector: The Abbrev-YYYY format resolves the century ambiguity of
    the 2-digit year variant. It is used where precision is required: formal
    financial statements, database schemas, API date fields. The 4-digit year
    is also more easily distinguishable from non-date hyphened tokens because
    few non-date identifiers use 4-digit numeric components.

    Why a parser might fail: The parser handles the 2-digit year case but
    applies a different (or absent) pattern for the 4-digit year case, or
    the pattern for 4-digit years incorrectly requires the month to come
    after the year (YYYY-Abbrev format), causing Abbrev-YYYY to be missed.

    Failure reveals: The 4-digit year variant of the forward-order
    Abbrev-YYYY pattern is not recognized by the extractor.
    """
    result = extract_explicit_dates(text)
    assert len(result) > 0


# ===========================================================================
# SECTION 3 -- TRUE POSITIVES: ALL 12 ABBREVIATED MONTHS REVERSED (YY-Abbrev)
# ===========================================================================

@pytest.mark.parametrize('text', [
    # Year-first (reversed) format: YY-Abbrev or YYYY-Abbrev. This layout is
    # common in ISO-influenced date systems and data exports from European systems.
    '23-Jan',
    '23-Feb',
    '23-Mar',
    '23-Apr',
    '23-May',
    '23-Jun',
    '23-Jul',
    '23-Aug',
    '23-Sep',
    '23-Oct',
    '23-Nov',
    '23-Dec',
    # 4-digit year reversed variants
    '2023-Jan',
    '2023-Feb',
    '2023-Mar',
    '2023-Apr',
    '2023-May',
    '2023-Jun',
    '2023-Jul',
    '2023-Aug',
    '2023-Sep',
    '2023-Oct',
    '2023-Nov',
    '2023-Dec',
    # Sentence embedded reversed
    'Data as of 23-Oct is attached.',
    'Report for 23-Nov is ready.',
    'Period 2023-Oct closes Friday.',
    'The 2023-Dec figures are final.',
    'Audit for 24-Jan completed.',
    'See 2024-Mar for updated data.',
    'Baseline: 23-Sep.',
    'Reference: 2023-Jun.',
    # Additional reversed variants
    '24-Jan',
    '24-Feb',
    '24-Mar',
    '24-Apr',
    '24-May',
    '24-Jun',
    '24-Jul',
    '24-Aug',
    '24-Sep',
    '24-Oct',
    '24-Nov',
    '24-Dec',
    '2024-Jan',
    '2024-Feb',
    '2024-Mar',
    '2024-Apr',
    '2024-May',
    '2024-Jun',
    '2024-Jul',
    '2024-Aug',
    '2024-Sep',
    '2024-Oct',
    '2024-Nov',
    '2024-Dec',
])
def test_true_positive_abbrev_months_reversed(text):
    """
    True positive: year + hyphen + abbreviated month (reversed order).

    Attack vector: The reversed YY-Abbrev and YYYY-Abbrev formats. These are
    used in contexts where lexicographic sorting of date strings should produce
    chronological order (ISO 8601 motivation). The year-first ordering is
    standard in database fields, file naming conventions, and European data
    exports.

    Why a parser might fail: The parser was designed around the forward-order
    (Abbrev-Year) convention common in English business language and does not
    have a corresponding reversed-order pattern, or the reversed-order pattern
    is present but uses different (or absent) year-range validation logic.

    Failure reveals: The YEAR_MONTH extractor path is absent or incomplete,
    causing all year-first date expressions to be missed.
    """
    result = extract_explicit_dates(text)
    assert len(result) > 0


# ===========================================================================
# SECTION 4 -- TRUE POSITIVES: ALL 12 FULL MONTH NAMES HYPHENATED
# ===========================================================================

@pytest.mark.parametrize('text', [
    # Full month name + hyphen + 4-digit year.
    'January-2023',
    'February-2023',
    'March-2023',
    'April-2023',
    'May-2023',
    'June-2023',
    'July-2023',
    'August-2023',
    'September-2023',
    'October-2023',
    'November-2023',
    'December-2023',
    # Additional year variants
    'January-2024',
    'February-2024',
    'March-2024',
    'April-2024',
    'May-2024',
    'June-2024',
    'July-2024',
    'August-2024',
    'September-2024',
    'October-2024',
    'November-2024',
    'December-2024',
    # Sentence embedded
    'The March-2023 report was submitted.',
    'See October-2024 for current data.',
    'Coverage period: January-2024 to December-2024.',
    'The September-2023 audit found no issues.',
    'July-2024 is the target completion.',
    'Filed under November-2023.',
    'The February-2024 adjustment is pending.',
    'Effective August-2024 new rates apply.',
    'June-2023 was the baseline period.',
    'December-2023 is year-end.',
    'April-2024 budget was approved.',
    'May-2023 marked the project start.',
    # Boundary years
    'January-1926',
    'December-2036',
    'March-1980',
    'October-2000',
])
def test_true_positive_full_month_hyphenated(text):
    """
    True positive: full month name + hyphen + 4-digit year.

    Attack vector: The full-name hyphenated MONTH-YEAR format. While less
    common than the abbreviated form, this pattern appears in formal contexts
    where abbreviations are discouraged. The parser must recognize full month
    names (not just abbreviations) in the hyphenated MONTH_YEAR extractor.

    Why a parser might fail: The hyphenated month-year extractor was built
    primarily for abbreviated month names and does not include full month names
    in its pattern set, or the full-name pattern is a lower-priority branch
    that is pre-empted by a more general pattern match.

    Failure reveals: The MONTH_YEAR extractor only handles abbreviated month
    names and silently rejects spelled-out month names in hyphenated format.
    """
    result = extract_explicit_dates(text)
    assert len(result) > 0


# ===========================================================================
# SECTION 5 -- TRUE POSITIVES: CASE VARIANTS
# ===========================================================================

@pytest.mark.parametrize('text', [
    # Case variation in the abbreviated month component.
    'OCT-23',
    'oct-23',
    'OcT-23',
    'OCT-2023',
    'oct-2023',
    'OcT-2023',
    'JAN-23',
    'jan-23',
    'JaN-23',
    'DEC-23',
    'dec-23',
    'DeC-23',
    'MAR-2024',
    'mar-2024',
    'MaR-2024',
    'JUL-2024',
    'jul-2024',
    'JuL-2024',
    'NOV-2023',
    'nov-2023',
    'NoV-2023',
    'FEB-23',
    'feb-23',
    'FeB-23',
    'APR-2024',
    'apr-2024',
    'ApR-2024',
    'SEP-23',
    'sep-23',
    'SeP-23',
    'AUG-2024',
    'aug-2024',
    'AuG-2024',
    'JUN-23',
    'jun-23',
    'JuN-23',
    'MAY-23',
    'may-23',
    'MaY-23',
    # Full month name case variants
    'OCTOBER-2023',
    'october-2023',
    'JANUARY-2024',
    'january-2024',
    'MARCH-2023',
    'march-2023',
    'DECEMBER-2024',
    'december-2024',
])
def test_true_positive_case_variants(text):
    """
    True positive: case variants of hyphenated month-year expressions.

    Attack vector: Case variation in month abbreviation spelling. System logs,
    database exports, and automated report headers frequently produce month
    abbreviations in all-caps (OCT), all-lowercase (oct), or mixed case (OcT).
    A parser using case-sensitive string matching will fail on all but the
    casing it was designed for.

    Why a parser might fail: The month abbreviation lookup table or regex is
    case-sensitive. This is a particularly common bug when month names are
    stored as title-cased constants (Oct, Jan, Dec) and compared using ==
    rather than case-insensitive matching.

    Failure reveals: The hyphenated MONTH_YEAR extractor uses case-sensitive
    comparison for month name lookup, making it fragile against real-world
    data sources that normalize to uppercase or lowercase.
    """
    result = extract_explicit_dates(text)
    assert len(result) > 0


# ===========================================================================
# SECTION 6 -- TRUE POSITIVES: SENTENCE EMBEDDED
# ===========================================================================

@pytest.mark.parametrize('text', [
    'The report for Oct-23 is ready for review.',
    'As of 2023-Oct, the project is complete.',
    'All data from Jan-2024 must be reprocessed.',
    'Please review the Dec-23 closing figures.',
    'Coverage period runs from Jan-23 to Dec-23.',
    'The Nov-2023 audit revealed three discrepancies.',
    'Submit your Mar-24 expense report by the 5th.',
    'The Jul-2024 projection has been updated.',
    'Historical baseline set at Sep-22.',
    'The 2024-Feb data has been reconciled.',
    'Effective 2024-Jan new pricing applies.',
    'See the attached May-2024 summary.',
    'Period ending Jun-24 shows 12% growth.',
    'The Aug-2023 figures were restated.',
    'From Feb-2024 to August-2024 revenue grew.',
    'The October-2024 draft is under review.',
    'Q3 results: Jul-24, Aug-24, Sep-24.',
    'Invoices dated Oct-2023 require resubmission.',
    'All June-2024 transactions are reconciled.',
    'The March-2024 and April-2024 reports are merged.',
    'For period ending 2024-Jun please review.',
    'Compare 2023-Nov to 2024-Nov performance.',
    'The 23-Jan report is late.',
    'Data for 24-Dec is under embargo.',
    'Reference period: 2023-Mar to 2024-Mar.',
])
def test_true_positive_sentence_embedded(text):
    """
    True positive: hyphenated month-year expressions in sentence context.

    Attack vector: Hyphenated month-year tokens appearing within a full
    natural-language sentence. The surrounding sentence context introduces
    additional hyphens (from compound adjectives, hyphenated words, etc.)
    that may confuse a parser looking for hyphens as date delimiters.

    Why a parser might fail: The parser uses lookahead or lookbehind
    assertions anchored to whitespace that do not correctly handle cases
    where the date token is followed by a comma, period, or other
    punctuation rather than whitespace.

    Failure reveals: The boundary detection logic is sensitive to
    punctuation that immediately follows the date token, causing the
    parser to miss dates at the end of a clause.
    """
    result = extract_explicit_dates(text)
    assert len(result) > 0


# ===========================================================================
# SECTION 7 -- FALSE POSITIVES: NON-DATE HYPHENATED TOKENS
# ===========================================================================

@pytest.mark.parametrize('text', [
    # Day-of-week abbreviations followed by a 2-digit number.
    'Sun-23 is not a date.',
    'Mon-23 is a day label.',
    'Tue-23 label.',
    'Wed-23 identifier.',
    'Thu-23 marker.',
    'Fri-23 tag.',
    'Sat-23 prefix.',
    'Sun-2023 day label.',
    'Mon-2024 identifier.',
    'Tue-2024 tag.',
    # Quarter identifiers: Q1-23, Q2-23, Q3-23, Q4-23.
    'Q1-23 results are attached.',
    'Q2-23 revenue grew 5%.',
    'Q3-23 data is under review.',
    'Q4-23 was the strongest quarter.',
    'Q1-2023 earnings report.',
    'Q2-2024 projections.',
    'Q3-2024 actual vs budget.',
    'Q4-2024 forecast.',
    # Version identifiers with letter prefix: v1-23, v2-23.
    'v1-23 of the spec.',
    'v2-23 fixes the bug.',
    'v10-23 is the LTS release.',
    'v1-2023 is deprecated.',
    # Prefix+year compounds.
    'The pre-2023 policy applies.',
    'Post-2023 regulations are stricter.',
    'Non-2023 data is archived.',
    'Anti-2023 measures were repealed.',
    'Re-2023 filing is required.',
    'Mid-2023 saw the peak.',
    'Late-2023 data is available.',
    'Early-2023 baseline established.',
    'Pre-2024 contracts are grandfathered.',
    'Post-2024 invoices use new rates.',
    # Month abbreviations used as word stems
    'Mar-ket analysis is attached.',
    'Jun-ction of routes is at mile 42.',
    'Aug-mented reality demo scheduled.',
    'Oct-ane rating is 91.',
    'Dec-imal precision matters.',
    'Nov-el approach tried.',
    'Feb-rile response noted.',
    # Generic hyphenated numeric identifiers
    'ID-23 was assigned.',
    'REF-23 must be quoted.',
    'CODE-2023 is invalid.',
    'TAG-23 applied.',
    # Same string on both sides of hyphen
    'Oct-Oct is not a date.',
    'Jan-Jan makes no sense.',
    # Year-year ranges (not month-year)
    'The 2023-2024 fiscal year budget.',
    'Revenue for 2022-2023 was flat.',
    # Non-month word prefixes with year
    'feature-2023 branch merged.',
    'hotfix-2024 deployed.',
    'PROJ-2023 ticket resolved.',
    'BUG-2024 is critical.',
    'update-2023 patch applied.',
    'release-2024 notes attached.',
])
def test_false_positive_non_date_hyphenated_tokens(text):
    """
    False positive guard: non-date hyphenated tokens must not be classified
    as dates.

    Attack vector: A large variety of hyphen-joined token pairs share the
    surface structure of hyphenated month-year expressions:
      - Day-of-week abbreviations (Sun, Mon, Tue, ...) followed by a year
      - Quarter labels (Q1, Q2, Q3, Q4) followed by a year
      - Version prefixes (v1, v2, v10) followed by a year
      - Common English word prefixes (pre-, post-, non-, mid-, late-, early-)
        followed by a year
      - Month abbreviations used as word stems (Mar-ket, Jun-ction)

    The parser must use a whitelist of valid month abbreviations (Jan, Feb,
    Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec) as the discriminating
    criterion. Any left-side token that is NOT in this whitelist should not
    trigger a MONTH_YEAR match.

    Why a parser might fail: The parser applies a too-broad pattern that
    matches any 2-3 letter alphabetic prefix followed by a hyphen and a
    2-4 digit number, without restricting the prefix to the month name
    whitelist.

    Failure reveals: The month-name whitelist is either absent (pure shape
    matching) or has a logic bug that allows non-month prefixes to match.
    """
    result = extract_explicit_dates(text)
    assert len(result) == 0


# ===========================================================================
# SECTION 8 -- BOUNDARY: YEAR RANGE FOR HYPHENATED MONTH-YEAR
# ===========================================================================

@pytest.mark.parametrize('text, expect_match', [
    # The hyphenated month-year extractor must apply the same year-range
    # constraint [1926, 2036] as all other date extractors.
    ('Jan-1926', True),
    ('Dec-2036', True),
    ('Oct-2024', True),
    ('Mar-1980', True),
    ('Jan-1925', False),
    ('Dec-2037', False),
    ('Oct-1800', False),
    ('Mar-2100', False),
    # 2-digit boundary tests
    ('Jan-26', True),
    ('Dec-36', True),
    ('Oct-24', True),
    # Degenerate cases
    ('Oct-Oct', False),
    ('2023-2024', False),
    ('Jan-Jan', False),
    # Additional boundary probes
    ('Feb-1926', True),
    ('Nov-2036', True),
    ('Jul-1927', True),
    ('Aug-2035', True),
    ('Sep-1924', False),
    ('Oct-2038', False),
])
def test_boundary_year_range_hyphenated(text, expect_match):
    """
    Boundary: year range enforcement for hyphenated month-year expressions.

    Attack vector: Hyphenated month-year expressions with year values at or
    beyond the documented supported range [1926, 2036]. The extractor must
    apply the same range constraint as all other date extractors. Also tests
    degenerate cases where the right-side operand is not a numeric year.

    Why a parser might fail: The hyphenated month-year extractor was
    implemented independently of the numeric date extractor and does not
    share the year-range validation logic. As a result, it may accept year
    values that all other extractors would reject (e.g., Jan-1800 or
    Oct-2100), leading to inconsistent parser behavior.

    Failure reveals: The year-range guard is absent or incorrectly applied
    in the hyphenated month-year extractor, causing range violations to
    propagate to the output.
    """
    result = extract_explicit_dates(text)
    if expect_match:
        assert len(result) > 0, f'Expected match for: {text!r}'
    else:
        assert len(result) == 0, f'Expected no match for: {text!r}'


# ===========================================================================
# SECTION 9 -- UNICODE: NON-ASCII HYPHEN VARIANTS
# ===========================================================================

@pytest.mark.parametrize('text', [
    # Non-breaking hyphen (U+2011): visually identical to regular hyphen.
    # Inserted by word processors to prevent line breaks at hyphens.
    'Oct‑23',
    'Oct‑2023',
    '2023‑Oct',
    'Jan‑24',
    'Mar‑2024',
    # En-dash (U+2013): slightly wider than hyphen, common in typography.
    'Oct–23',
    'Oct–2023',
    '2023–Oct',
    'Jan–24',
    'Mar–2024',
    # Em-dash (U+2014): significantly wider, used for parenthetical phrases.
    'Oct—23',
    'Oct—2023',
    '2023—Oct',
    'Jan—24',
    # Soft hyphen (U+00AD): invisible in rendering, typesetting line-break hint.
    'Oct­23',
    'Oct­2023',
    '2023­Oct',
    'Jan­24',
    # Figure dash (U+2012): similar in width to en-dash.
    'Oct‒23',
    'Oct‒2023',
    # Horizontal bar (U+2015): longer than em-dash.
    'Oct―23',
    'Oct―2023',
])
def test_unicode_hyphen_variants(text):
    """
    Unicode attack: non-ASCII hyphen substitutions in hyphenated month-year
    expressions.

    Attack vector: The Unicode standard includes multiple characters that
    are visually indistinguishable from or resemble the ASCII hyphen-minus
    (U+002D):
      - Non-breaking hyphen (U+2011): identical appearance, prevents line break
      - En-dash (U+2013): slightly wider, common word processor substitution
      - Em-dash (U+2014): significantly wider, parenthetical use
      - Soft hyphen (U+00AD): invisible, typesetting line-break hint
      - Figure dash (U+2012): financial use, width of a digit
      - Horizontal bar (U+2015): linguistic use

    These substitutions can appear in word processor output, PDF extraction
    artifacts, HTML entity encoding, and adversarial inputs.

    Why a parser might fail: The parser regex is anchored to the ASCII
    hyphen-minus character class ([-]) and does not include Unicode hyphen
    variants. Text normalized from word processor or PDF sources will
    silently fail to match.

    Failure reveals: The parser raises an unhandled exception on Unicode
    input, or the parser silently hangs on Unicode hyphen injection.
    """
    try:
        result = extract_explicit_dates(text)
        assert isinstance(result, dict)
    except Exception as exc:
        pytest.fail(
            f'Parser raised exception on Unicode hyphen input: {exc!r}\nInput: {text!r}'
        )


# ===========================================================================
# SECTION 10 -- COMPREHENSIVE: ALL MONTHS ACROSS ALL VALID YEARS (SWEEP)
# ===========================================================================

@pytest.mark.parametrize('month_abbrev', [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
])
@pytest.mark.parametrize('year', [1926, 1950, 1980, 2000, 2010, 2020, 2024, 2036])
def test_true_positive_all_months_all_valid_years(month_abbrev, year):
    """
    True positive: comprehensive sweep of all month abbreviations across
    representative valid years.

    Attack vector: Combinatorial coverage of the month-year matrix. Bugs in
    the hyphenated MONTH_YEAR extractor may be month-specific (e.g., May
    conflicting with the modal-verb suppression rule) or year-specific (e.g.,
    boundary years at the edge of the valid range).

    This parametrized test generates 12 months x 8 years = 96 test cases,
    ensuring that no month-year combination within the valid range is missed
    by the extractor.

    Why a parser might fail: A month-specific suppression rule (e.g., May
    is suppressed because it appears frequently as a modal verb) may be
    applied even in hyphenated context where May-2024 is unambiguous.
    Alternatively, a year-range boundary check with an off-by-one error may
    incorrectly reject the boundary years (1926, 2036).

    Failure reveals: Either a month-specific suppression is overly broad
    (catching May-2024 in addition to bare May as a modal verb), or the
    year-range check has an off-by-one at the boundary values.
    """
    text = f'The {month_abbrev}-{year} report is ready.'
    result = extract_explicit_dates(text)
    assert len(result) > 0, (
        f'Expected match for {month_abbrev}-{year} in: {text!r}'
    )


# ===========================================================================
# SECTION 11 -- ADJACENT CONTEXT: MULTIPLE DATES IN ONE STRING
# ===========================================================================

@pytest.mark.parametrize('text', [
    'Compare Jan-23 to Jan-24.',
    'From Feb-2023 to Feb-2024.',
    'Q1 covers Jan-24, Feb-24, Mar-24.',
    'Period: Oct-23 through Dec-23.',
    'The trend from 2023-Jan to 2023-Dec is positive.',
    'See both Jun-2023 and Jun-2024 for comparison.',
    'Monthly data: Jan-24, Feb-24, Mar-24, Apr-24.',
    'H1 2024: Jan-2024 through Jun-2024.',
    'H2 2023: Jul-2023 through Dec-2023.',
    'YoY comparison: Oct-2023 vs Oct-2024.',
    'Compare Q1: Jan-24, Feb-24, Mar-24 with prior.',
    'Period: 2023-Jan through 2023-Dec inclusive.',
])
def test_true_positive_multiple_dates_in_string(text):
    """
    True positive: multiple hyphenated month-year dates in a single string.

    Attack vector: A string containing multiple date references. The parser
    must extract all occurrences without the first match consuming the entire
    string or without state contamination between matches.

    Why a parser might fail: The parser uses a non-overlapping single-pass
    regex that returns only the first match, or the parser consumes whitespace
    greedily after the first match, preventing subsequent matches.

    Failure reveals: The multi-match iteration logic is absent or incorrectly
    implemented, causing only the first date to be returned.
    """
    result = extract_explicit_dates(text)
    assert len(result) >= 2, f'Expected at least 2 date matches in: {text!r}'


# ===========================================================================
# SECTION 12 -- FALSE POSITIVES: ADDITIONAL EDGE CASES
# ===========================================================================

@pytest.mark.parametrize('text', [
    # Git branch names with year fragments
    'Branch feature-2023 was merged.',
    'Hotfix hotfix-2024 deployed.',
    # JIRA-style ticket IDs
    'Ticket PROJ-2023 is resolved.',
    'Issue BUG-2024 is critical.',
    # Hyphenated year ranges
    'The 2023-2024 fiscal year budget.',
    'Revenue for 2022-2023 was flat.',
    # Generic word-year compounds
    'The update-2023 patch was applied.',
    'The release-2024 notes are attached.',
    'See doc-2023 for background.',
    'File backup-2024 is stored.',
    # Numbers on both sides of hyphen (no alphabetic month component)
    'Record 01-23 was processed.',
    'ID 99-23 is expired.',
    'Code 12-23 is active.',
    # Three-component sequences that look like date fragments
    'Ref 23-45-67 is incorrect.',
    'Code A23-B45 is a product ID.',
    # Year as left operand with non-month right operand
    '2023-Q1 financial data.',
    '2024-H2 is our target.',
    '2023-YTD performance.',
    '2024-FY results.',
])
def test_false_positive_additional_non_date_constructs(text):
    """
    False positive guard: additional non-date hyphenated constructs.

    Attack vector: Additional categories of hyphen-joined strings that appear
    frequently in technical and business text without date meaning:
      - Source control branch names (feature-2023, hotfix-2024)
      - Issue tracker IDs (PROJ-2023, BUG-2024)
      - Fiscal year ranges (2023-2024)
      - Generic word-year compounds (update-2023, backup-2024)
      - Pure numeric pairs (01-23, 99-23)
      - Business period labels (2023-Q1, 2024-H2, 2023-YTD)

    Why a parser might fail: The parser left-operand whitelist may be
    applied only to alphabetic tokens and may inadvertently match numeric
    tokens on the left side (01-23 could be misread as day-year if the
    month whitelist lookup falls back to a numeric interpretation).

    Failure reveals: The left-side discriminator is either absent, not
    anchored to word boundaries, or falls back to a numeric interpretation
    when no month name is recognized.
    """
    result = extract_explicit_dates(text)
    assert len(result) == 0
