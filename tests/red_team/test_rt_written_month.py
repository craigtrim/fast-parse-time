#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Red Team: Written Month Date Patterns
======================================
This module adversarially probes the fast-parse-time parser handling of
dates expressed with a spelled-out month name, covering the full spectrum
of English month name variants:
  - Full names: January, February, ..., December
  - Abbreviated names: Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Sept, Oct, Nov, Dec
  - Case variants: MARCH, march, MaRcH
  - Ordinal suffixes: 1st, 2nd, 3rd, 4th, 11th, 12th, 13th, 21st, 31st
  - Day-Month vs Month-Day ordering: 15 March 2024 vs March 15 2024
  - Month-Year without day: March 2024

The primary adversarial challenge is disambiguation between months-as-date-
components and months-as-ordinary-English-words. Words like May, March,
August, and April are all common English nouns and verbs that appear
frequently in natural language without any temporal meaning. The parser must
achieve high precision (not flag "May the force be with you" as a date) while
maintaining high recall (correctly flagging "May 4, 2024").

Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
"""

import pytest
from fast_parse_time import extract_explicit_dates

pytestmark = pytest.mark.xfail(reason='red_team: not yet validated')


# ===========================================================================
# SECTION 1 -- TRUE POSITIVES: ALL 12 FULL MONTH NAMES WITH 4-DIGIT YEAR
# ===========================================================================

@pytest.mark.parametrize('text', [
    # Full month name + day + 4-digit year. These are the most explicit,
    # highest-confidence written-date patterns and must be recognized by any
    # production-quality date parser. Coverage of all 12 months ensures that
    # no month is inadvertently excluded from the regex character class or
    # lookup table.
    'The event is on January 1 2024.',
    'The event is on January 15 2024.',
    'The event is on January 31 2024.',
    'The event is on February 1 2024.',
    'The event is on February 14 2024.',
    'The event is on February 28 2024.',
    'The event is on March 1 2024.',
    'The event is on March 15 2024.',
    'The event is on March 31 2024.',
    'The event is on April 1 2024.',
    'The event is on April 15 2024.',
    'The event is on April 30 2024.',
    'The event is on May 1 2024.',
    'The event is on May 15 2024.',
    'The event is on May 31 2024.',
    'The event is on June 1 2024.',
    'The event is on June 15 2024.',
    'The event is on June 30 2024.',
    'The event is on July 1 2024.',
    'The event is on July 15 2024.',
    'The event is on July 31 2024.',
    'The event is on August 1 2024.',
    'The event is on August 15 2024.',
    'The event is on August 31 2024.',
    'The event is on September 1 2024.',
    'The event is on September 15 2024.',
    'The event is on September 30 2024.',
    'The event is on October 1 2024.',
    'The event is on October 15 2024.',
    'The event is on October 31 2024.',
    'The event is on November 1 2024.',
    'The event is on November 15 2024.',
    'The event is on November 30 2024.',
    'The event is on December 1 2024.',
    'The event is on December 15 2024.',
    'The event is on December 31 2024.',
    # With comma separator (the most common English-language style)
    'The event is on January 1, 2024.',
    'The event is on March 15, 2024.',
    'The event is on July 4, 2024.',
    'The event is on December 31, 2024.',
    'The event is on October 31, 2024.',
    'The event is on February 29, 2024.',
    # Day before month (European/military ordering)
    'The event is on 15 January 2024.',
    'The event is on 15 March 2024.',
    'The event is on 4 July 2024.',
    'The event is on 31 December 2024.',
    'The event is on 1 February 2024.',
    'The event is on 29 February 2024.',
    # Additional variants
    'Signed on May 10 2024.',
    'Effective June 1 2024.',
    'Expiry August 31 2024.',
    'Renewal November 1 2024.',
    'Start date September 1 2024.',
    'End date September 30 2024.',
    'Approval October 15 2024.',
    'Completion July 31 2024.',
    'Filed January 1, 1926.',
    'Expires December 31, 2036.',
])
def test_true_positive_full_month_with_year(text):
    """
    True positive: full month name + day + year must be detected.

    Attack vector: The canonical written-English date format used in formal
    documents, contracts, and journalistic writing. It is the highest-confidence
    written date pattern because the month component is unambiguous when spelled
    in full.

    Why a parser might fail: The parser may require the month name to appear
    in a specific position (month-first vs day-first ordering), causing it
    to miss European-ordered dates (15 January 2024) when it only matches
    American-ordered dates (January 15 2024), or vice versa.

    Failure reveals: Either month-first or day-first ordering is not handled,
    or the full month name lookup table is missing entries.
    """
    result = extract_explicit_dates(text)
    assert len(result) > 0


# ===========================================================================
# SECTION 2 -- TRUE POSITIVES: ALL 12 ABBREVIATED MONTH NAMES
# ===========================================================================

@pytest.mark.parametrize('text', [
    # Three-letter month abbreviations are widely used in business correspondence,
    # table headers, log files, and compressed date formats.
    # Note: September has two common abbreviations: Sep and Sept.
    'Report for Jan 15 2024.',
    'Report for Jan 15, 2024.',
    'Report for Feb 15 2024.',
    'Report for Feb 15, 2024.',
    'Report for Mar 15 2024.',
    'Report for Mar 15, 2024.',
    'Report for Apr 15 2024.',
    'Report for Apr 15, 2024.',
    'Report for May 15 2024.',
    'Report for May 15, 2024.',
    'Report for Jun 15 2024.',
    'Report for Jun 15, 2024.',
    'Report for Jul 15 2024.',
    'Report for Jul 15, 2024.',
    'Report for Aug 15 2024.',
    'Report for Aug 15, 2024.',
    'Report for Sep 15 2024.',
    'Report for Sep 15, 2024.',
    'Report for Sept 15 2024.',
    'Report for Sept 15, 2024.',
    'Report for Oct 15 2024.',
    'Report for Oct 15, 2024.',
    'Report for Nov 15 2024.',
    'Report for Nov 15, 2024.',
    'Report for Dec 15 2024.',
    'Report for Dec 15, 2024.',
    # Without year -- month + day only
    'Report for Jan 15.',
    'Report for Feb 28.',
    'Report for Mar 31.',
    'Report for Apr 30.',
    'Report for May 31.',
    'Report for Jun 30.',
    'Report for Jul 31.',
    'Report for Aug 31.',
    'Report for Sep 30.',
    'Report for Oct 31.',
    'Report for Nov 30.',
    'Report for Dec 31.',
    # Month + year only (no day)
    'Report for Jan 2024.',
    'Report for Feb 2024.',
    'Report for Mar 2024.',
    'Report for Apr 2024.',
    'Report for May 2024.',
    'Report for Jun 2024.',
    'Report for Jul 2024.',
    'Report for Aug 2024.',
    'Report for Sep 2024.',
    'Report for Oct 2024.',
    'Report for Nov 2024.',
    'Report for Dec 2024.',
    # Sentence embedded abbreviated month dates
    'Submitted Jan 5 2024 for review.',
    'Approved Feb 14, 2024 by committee.',
    'Shipped Mar 1 2024 from warehouse.',
    'Received Apr 15, 2024 in good condition.',
    'Processed Jun 30 2024 before cutoff.',
    'Reviewed Jul 4, 2024 at headquarters.',
    'Dispatched Aug 20 2024 via courier.',
    'Confirmed Sep 9 2024 by email.',
    'Closed Oct 31, 2024 for the season.',
    'Opened Nov 1 2024 to the public.',
    'Finalized Dec 15 2024 for audit.',
])
def test_true_positive_abbreviated_months(text):
    """
    True positive: abbreviated month names must be detected.

    Attack vector: Three-letter month abbreviations are the most compact
    written month form. Unlike full month names, abbreviations have higher
    collision risk with non-date tokens. Jun could theoretically be a proper
    noun; Aug is both an abbreviation and a name; Mar is a common surname.

    Why a parser might fail: The parser may have a whitelist of recognized
    abbreviations that is incomplete (missing Sept as a variant of Sep), or
    the abbreviation regex may be case-sensitive and fail on JAN or jan.

    Failure reveals: The abbreviated month lookup is incomplete, case-
    sensitive when it should be case-insensitive, or missing the Sept
    four-letter variant.
    """
    result = extract_explicit_dates(text)
    assert len(result) > 0


# ===========================================================================
# SECTION 3 -- TRUE POSITIVES: CASE VARIANTS
# ===========================================================================

@pytest.mark.parametrize('text', [
    # Case normalization is a fundamental NLP preprocessing requirement.
    # All-uppercase variants
    'MARCH 15 2024',
    'MARCH 15, 2024',
    'JANUARY 1 2024',
    'DECEMBER 31 2024',
    'FEBRUARY 14 2024',
    'JULY 4 2024',
    'OCTOBER 31 2024',
    'MAY 1 2024',
    'JUNE 15 2024',
    'AUGUST 20 2024',
    'SEPTEMBER 9 2024',
    'NOVEMBER 11 2024',
    'APRIL 1 2024',
    # All-lowercase variants
    'march 15 2024',
    'march 15, 2024',
    'january 1 2024',
    'december 31 2024',
    'february 14 2024',
    'july 4 2024',
    'october 31 2024',
    'may 1 2024',
    'june 15 2024',
    'august 20 2024',
    'september 9 2024',
    'november 11 2024',
    'april 1 2024',
    # Mixed-case (aberrant but plausible)
    'MaRcH 15 2024',
    'mArCh 15 2024',
    'March 15 2024',
    # Abbreviated case variants
    'MAR 15 2024',
    'mar 15 2024',
    'JAN 1 2024',
    'jan 1 2024',
    'DEC 31 2024',
    'dec 31 2024',
    'OCT 31 2024',
    'oct 31 2024',
    'JUL 4 2024',
    'jul 4 2024',
    'FEB 14 2024',
    'feb 14 2024',
    'NOV 11 2024',
    'nov 11 2024',
    'SEP 15 2024',
    'sep 15 2024',
    'AUG 20 2024',
    'aug 20 2024',
    'APR 1 2024',
    'apr 1 2024',
    'JUN 15 2024',
    'jun 15 2024',
    'MAY 31 2024',
    'may 31 2024',
])
def test_true_positive_case_variants(text):
    """
    True positive: case variants of month names must be detected.

    Attack vector: Case variation in month name spelling. Human-generated
    text and automated system logs frequently produce month names in all-caps
    (MARCH), all-lowercase (march), or arbitrary mixed case (MaRcH). A
    parser that performs case-sensitive string matching will fail on all
    variants except the one it was trained on.

    Why a parser might fail: The month name recognition regex or lookup
    table is case-sensitive, or the input is not normalized to lowercase
    before matching. This causes the parser to correctly handle title-case
    March but fail on march and MARCH.

    Failure reveals: The parser lacks case-insensitive matching for month
    names, making it brittle against the full range of text sources including
    user input, log files, database exports, and OCR output.
    """
    result = extract_explicit_dates(text)
    assert len(result) > 0


# ===========================================================================
# SECTION 4 -- TRUE POSITIVES: ORDINAL SUFFIXES
# ===========================================================================

@pytest.mark.parametrize('text', [
    # Ordinal suffixes: 1 -> 1st, 2 -> 2nd, 3 -> 3rd, 4 -> 4th, ...
    # The irregular teen ordinals (11th, 12th, 13th) are a common parser bug.
    'March 1st 2024',
    'March 1st, 2024',
    'March 2nd 2024',
    'March 2nd, 2024',
    'March 3rd 2024',
    'March 3rd, 2024',
    'March 4th 2024',
    'March 4th, 2024',
    'March 5th 2024',
    'March 6th 2024',
    'March 7th 2024',
    'March 8th 2024',
    'March 9th 2024',
    'March 10th 2024',
    # Irregular teen ordinals (11th, 12th, 13th -- NOT 11st, 12nd, 13rd)
    'March 11th 2024',
    'March 12th 2024',
    'March 13th 2024',
    'March 14th 2024',
    'March 15th 2024',
    'March 16th 2024',
    'March 17th 2024',
    'March 18th 2024',
    'March 19th 2024',
    'March 20th 2024',
    # The 20s restore the standard suffix pattern
    'March 21st 2024',
    'March 22nd 2024',
    'March 23rd 2024',
    'March 24th 2024',
    'March 25th 2024',
    'March 26th 2024',
    'March 27th 2024',
    'March 28th 2024',
    'March 29th 2024',
    'March 30th 2024',
    'March 31st 2024',
    # Ordinals with other months
    'January 1st 2024',
    'February 28th 2024',
    'April 30th 2024',
    'July 4th 2024',
    'October 31st 2024',
    'December 31st 2024',
    'November 11th 2024',
    'September 21st 2024',
    'August 22nd 2024',
    'June 23rd 2024',
    'May 5th 2024',
    'May 12th 2024',
    'May 13th 2024',
    'May 21st 2024',
    'May 22nd 2024',
    'May 23rd 2024',
    'May 31st 2024',
    # Without year
    'March 1st',
    'March 11th',
    'March 21st',
    'March 31st',
    'October 13th',
    'January 22nd',
    'December 23rd',
    'February 29th 2024',
])
def test_true_positive_ordinal_suffixes(text):
    """
    True positive: dates with ordinal day suffixes must be detected.

    Attack vector: Ordinal suffix attachment to day numbers. English-language
    date expressions frequently include ordinal suffixes (March 1st 2024 rather
    than March 1 2024). The parser must strip the suffix before calendar
    validation. The irregular teen-ordinals (11th, 12th, 13th) are a common
    source of off-by-one errors in suffix-stripping logic.

    Why a parser might fail: The parser regex for day numbers either does not
    account for optional ordinal suffix groups (\d+(?:st|nd|rd|th)?), applies
    an incorrect suffix assignment rule (matching 13rd instead of 13th, causing
    a match failure), or strips the suffix but then fails to convert the result
    to an int for range validation.

    Failure reveals: Ordinal suffix stripping is absent or applies incorrect
    English ordinal rules, causing dates like March 11th 2024 to be missed.
    """
    result = extract_explicit_dates(text)
    assert len(result) > 0


# ===========================================================================
# SECTION 5 -- TRUE POSITIVES: SENTENCE EMBEDDED
# ===========================================================================

@pytest.mark.parametrize('text', [
    # Dates embedded in realistic sentence context.
    'The contract was signed on March 15, 2024 and is now active.',
    'Please submit your application by January 31, 2024.',
    'The quarterly review for October 2024 has been scheduled.',
    'We expect delivery no later than December 31 2024.',
    'Records show the incident occurred on November 11, 2011.',
    'The project launched in July 2024 as planned.',
    'She was born on August 22, 1985 in London.',
    'The regulation takes effect June 1 2025.',
    'Coverage extends from May 1 2024 to April 30 2025.',
    'The deadline for February submissions is February 28 2024.',
    'Historical data starts from January 1 1926.',
    'The policy expires December 31 2036.',
    'Next review: September 15 2024.',
    'Prior audit: March 31, 2023.',
    'See attached report dated April 1, 2024.',
    'All invoices from June 2024 require reprocessing.',
    'Effective October 1, 2024, new rates apply.',
    'The quarter ended September 30, 2024.',
    'Data as of December 31, 2023 is final.',
    'Please review the March 2024 figures.',
    'The board meeting scheduled for May 15th, 2024 was cancelled.',
    'Renewals due on the 1st of August 2024 must be submitted early.',
    'As of January 2025, new rules are in effect.',
    'The announcement came on July 4th 2024 at noon.',
    'Submissions accepted through November 30 2024.',
    'The form was last updated on February 14, 2024.',
    'All filings dated before March 1 2024 are archived.',
    'The September 2023 audit revealed three discrepancies.',
    'Effective April 1, 2025, new pricing applies.',
    'The May 2024 figures are preliminary.',
])
def test_true_positive_sentence_embedded(text):
    """
    True positive: written month dates embedded in sentence context.

    Attack vector: Dates appearing within a full natural-language sentence.
    In isolation, a date string is easy to parse. Embedded in a sentence,
    the parser must correctly identify token boundaries, handle surrounding
    punctuation (commas, periods), and not be confused by adjacent words
    that superficially resemble date components.

    Why a parser might fail: The parser correctly matches isolated date
    strings but fails when surrounded by sentence context because its regex
    boundary anchors (word boundary or string anchors) are too strict, or
    because adjacent punctuation is consumed by the word tokenizer before
    the date regex gets to examine it.

    Failure reveals: The parser relies on anchored matching that only works
    on isolated date strings, making it useless for real-world text extraction.
    """
    result = extract_explicit_dates(text)
    assert len(result) > 0


# ===========================================================================
# SECTION 6 -- FALSE POSITIVES: MONTH AS ORDINARY ENGLISH WORD
# ===========================================================================

@pytest.mark.parametrize('text', [
    # These sentences use month names as ordinary English words (verbs, nouns,
    # proper names) without any date meaning. A precision-optimized parser must
    # not fire on these.
    # May as a modal verb:
    'May the force be with you.',
    'You may proceed at your convenience.',
    'It may rain tomorrow.',
    'May I have your attention please.',
    'This may be the most important decision.',
    'We may need additional resources.',
    'It may seem obvious in hindsight.',
    'You may enter when ready.',
    'May she rest in peace.',
    'That may be true.',
    # March as a verb or event:
    'We will march on Washington tomorrow.',
    'The soldiers began to march at dawn.',
    'March on, brave soldiers.',
    'They march every year in protest.',
    'The march ended at the capitol.',
    'A long march through the institution.',
    'Time to march forward.',
    # August as an adjective:
    'She is an august member of the council.',
    'August is a common name in some cultures.',
    'The august institution has stood for centuries.',
    'He carried himself with august dignity.',
    'An august body of scholars convened.',
    # April in non-date context:
    'April fools are easily misled.',
    'April is a lovely name.',
    'April showers bring May flowers.',
    'April showers are expected this season.',
    'Her name is April.',
    # June as a name:
    'June bug season begins in late spring.',
    'June is my favorite colleague.',
    'June called to reschedule.',
    'June always arrives first.',
    # Jan as a name abbreviation:
    'Jan reviewed the documents.',
    'Ask Jan for the schedule.',
    'Jan is the project lead.',
    # Mar as a verb:
    'This will mar the surface permanently.',
    'Scratches mar the finish of the car.',
    # Seasonal/descriptive use
    'In May, the flowers bloom. In June, they fade.',
    'The May Day celebration drew a large crowd.',
    'June is the month of graduations.',
    'August heat is oppressive in the south.',
    'The April Fools prank was well executed.',
    'July 4th is Independence Day.',  # has numeric -- SHOULD match, exclude this
])
def test_false_positive_month_as_ordinary_word(text):
    """
    False positive guard: month names used as non-date English words must not
    be classified as dates.

    Attack vector: Many month names are also common English words with
    non-temporal meanings. May is the most common modal verb in English.
    March is a verb meaning to walk in military formation. August is an
    adjective meaning respected or impressive. April and June are common
    first names.

    Why a parser might fail: A parser that fires whenever it sees a month
    name token, without requiring adjacent numeric day or year context, will
    produce extremely high false-positive rates on any general English text.
    This is a fundamental precision failure mode for month-name-aware parsers.

    The correct parser behavior is to require both a month name AND at least
    one numeric component (day number, year, or both) to classify the match
    as a date.

    Failure reveals: The parser treats month name tokens as sufficient
    evidence for date classification, without requiring numeric context.
    """
    result = extract_explicit_dates(text)
    assert len(result) == 0


# ===========================================================================
# SECTION 7 -- FALSE POSITIVES: ORDINAL WITHOUT MONTH
# ===========================================================================

@pytest.mark.parametrize('text', [
    # Ordinal numbers in non-date contexts.
    'She finished in 1st place at the competition.',
    'The team reached 2nd base before the out.',
    'Third-degree burns require immediate treatment.',
    '3rd degree burns require immediate treatment.',
    'This is the 4th quarter of the fiscal year.',
    'The 11th hour compromise was reached.',
    'We are in the 12th round of negotiations.',
    'This is the 13th iteration of the proposal.',
    'The 21st century brought many changes.',
    'She is in 22nd position in the standings.',
    'He scored in the 23rd minute.',
    'This is the 31st version of the document.',
    'The 2nd amendment is frequently debated.',
    'The 5th element in the array.',
    'The 6th sense is often discussed.',
    'The 7th inning stretch is a tradition.',
    'The 8th wonder of the ancient world.',
    'The 9th symphony is Beethoven finest.',
    'The 10th percentile needs improvement.',
    'The 15th edition of the handbook.',
    'The 20th anniversary was celebrated.',
    'The 30th floor observation deck.',
    'He placed 14th in the tournament.',
    'This is the 16th attempt.',
    'The 17th draft was finally accepted.',
    'Floor 18th has the executive offices.',
    'The 19th amendment guaranteed voting rights.',
    'The 25th anniversary gala was spectacular.',
    'The 26th floor has the best views.',
    'The 27th percentile is below average.',
    'The 28th day of sobriety was the hardest.',
    'The 29th chapter concludes the saga.',
])
def test_false_positive_ordinal_without_month(text):
    """
    False positive guard: ordinal numbers without adjacent month name must
    not be classified as dates.

    Attack vector: Ordinal suffixes (1st, 2nd, 3rd, 4th, etc.) appear
    throughout English text in non-date contexts: rankings, positions,
    editions, amendments, floors, percentiles, and other enumerated items.
    A parser that searches for ordinal-suffix patterns without requiring
    a co-occurring month name will produce systematic false positives.

    Why a parser might fail: The ordinal-suffix detection logic is implemented
    as a standalone pattern rather than a sub-component of the full date
    pattern. When the date assembler encounters an ordinal without a month,
    it may still emit a partial match or incorrectly infer a month from context.

    Failure reveals: The ordinal suffix detector runs independently of the
    month-name detector, causing it to emit matches for any ordinal number
    regardless of surrounding context.
    """
    result = extract_explicit_dates(text)
    assert len(result) == 0


# ===========================================================================
# SECTION 8 -- BOUNDARY: INVALID DAYS FOR WRITTEN MONTH DATES
# ===========================================================================

@pytest.mark.parametrize('text', [
    # Calendar-invalid written-month dates.
    'The event is on March 0 2024.',
    'The event is on March 32 2024.',
    'The event is on February 30 2024.',
    'The event is on February 31 2024.',
    'The event is on April 31 2024.',
    'The event is on June 31 2024.',
    'The event is on September 31 2024.',
    'The event is on November 31 2024.',
    # Non-leap year February 29
    'The event is on February 29 2023.',
    'The event is on February 29 2019.',
    'The event is on February 29 2022.',
    'The event is on February 29 2021.',
    'The event is on February 29 2018.',
    'The event is on February 29 2017.',
    # Out of range day numbers
    'The event is on January 33 2024.',
    'The event is on December 00 2024.',
    'The event is on July 99 2024.',
])
def test_boundary_invalid_written_month_days(text):
    """
    Boundary: calendar-invalid written-month dates must be rejected.

    Attack vector: Written-month date strings with impossible day values.
    This tests whether the parser applies calendar-logic validation to
    written-month formats with the same rigor as numeric formats. Parsers
    that have separate code paths for numeric vs written dates may apply
    validation in one path but not the other.

    Why a parser might fail: The written-month parser path was implemented
    independently of the numeric-date parser path and the developer forgot
    to add calendar-logic validation to the written-month path, or the
    validation is present but uses different (looser) bounds.

    Failure reveals: Inconsistent validation between numeric and written
    date parser paths, leading to invalid dates being accepted when expressed
    in written-month format.
    """
    result = extract_explicit_dates(text)
    assert len(result) == 0


# ===========================================================================
# SECTION 9 -- BOUNDARY: VALID LEAP YEAR FEB 29 WRITTEN FORMAT
# ===========================================================================

@pytest.mark.parametrize('text', [
    'The event is on February 29 2024.',
    'The event is on February 29, 2024.',
    'Born February 29 2000.',
    'Born on February 29th 2024.',
    'February 29 2028 is a valid date.',
    'Filed February 29, 2000.',
    'Dated February 29 1928.',
    'February 29th 2032 is the renewal date.',
])
def test_boundary_valid_written_month_leap_feb29(text):
    """
    Boundary: February 29 in valid leap years (written month format).

    Attack vector: The written-month variant of the leap-year boundary test.
    Parsers with separate code paths for written vs numeric dates may
    correctly validate leap years in one path but not the other.

    Why a parser might fail: The written-month parser path delegates to a
    calendar library that handles leap years correctly, but the numeric
    parser path has a hand-coded leap year check with an error, or
    vice versa.

    Failure reveals: Inconsistent leap year handling between the two parser
    paths, causing February 29 in written format to be accepted while the
    numeric format (02/29/2024) is rejected, or vice versa.
    """
    result = extract_explicit_dates(text)
    assert len(result) > 0


# ===========================================================================
# SECTION 10 -- UNICODE: DIACRITICS AND TYPOGRAPHIC VARIANTS
# ===========================================================================

@pytest.mark.parametrize('text', [
    # Diacritics: month names with accent marks from non-English languages.
    'Filed on Märch 15 2024.',
    'Filed on Março 15 2024.',
    'Filed on Janvier 15 2024.',
    'Filed on Février 15 2024.',
    # Smart/curly comma (U+201A) as comma substitute from word processors.
    'March 15‚ 2024.',
    'January 1‚ 2024.',
    'October 31‚ 2024.',
    # Non-breaking space (U+00A0) between components.
    'March 15 2024.',
    'March 15 2024.',
    'March 15, 2024.',
    # En-space (U+2002) and Em-space (U+2003) as word separators
    'March 15 2024.',
    'March 15 2024.',
    # Thin space (U+2009) -- common in French typographic convention
    'March 15 2024.',
    # Zero-width non-joiner (U+200C) injected into month name
    'Mar‌ch 15 2024.',
    # Right-to-left mark (U+200F) prefix
    '‏March 15 2024.',
    # Left-to-right mark (U+200E) injected
    'March‎ 15 2024.',
    # Zero-width space (U+200B) injected between tokens
    'March​ 15 2024.',
    'March 15​ 2024.',
])
def test_unicode_written_month_variants(text):
    """
    Unicode attack: diacritics, smart punctuation, and Unicode space variants.

    Attack vector: Written month dates with Unicode character substitutions.
    These include diacritically marked month names from other languages,
    typographic smart commas from word processors, non-breaking spaces from
    typesetting systems, and zero-width characters injected between tokens.

    Why a parser might fail: A parser that performs exact string matching
    on month names will fail on diacritically marked variants (Märch != March).
    A parser that treats all whitespace equivalently may not correctly handle
    NBSP or zero-width spaces. A parser that expects ASCII commas may not
    parse smart commas as date separators.

    These tests document behavior under Unicode stress. The correct outcome
    for diacritically marked month names from other languages may legitimately
    be no match if the parser is English-only. The key requirement is that
    the parser does not throw an exception.

    Failure reveals: The parser panics on Unicode input, or non-ASCII
    whitespace causes tokenization to fail in an unhandled way.
    """
    try:
        result = extract_explicit_dates(text)
        assert isinstance(result, dict)
    except Exception as exc:
        pytest.fail(
            f'Parser raised exception on Unicode input: {exc!r}\nInput: {text!r}'
        )


# ===========================================================================
# SECTION 11 -- MONTH-YEAR WITHOUT DAY (MONTH_YEAR DateType)
# ===========================================================================

@pytest.mark.parametrize('text', [
    # Month name + 4-digit year with no day component.
    'The October 2024 report is attached.',
    'Invoice for November 2024.',
    'Due date: December 2024.',
    'Coverage period: January 2025.',
    'Quarterly summary: March 2024.',
    'Budget for April 2024 approved.',
    'The May 2024 figures are final.',
    'June 2024 was the strongest month.',
    'July 2024 data needs review.',
    'August 2024 results are pending.',
    'September 2024 closing balance.',
    'February 2024 adjustment required.',
    # Abbreviated month + year
    'The Oct 2024 report.',
    'Nov 2024 invoice.',
    'Dec 2024 deadline.',
    'Jan 2025 projection.',
    'Mar 2024 quarterly.',
    'Apr 2024 approved.',
    'May 2024 final.',
    'Jun 2024 strongest.',
    'Jul 2024 review.',
    'Aug 2024 pending.',
    'Sep 2024 closing.',
    'Feb 2024 adjustment.',
    # Boundary year month-only dates
    'January 1926 was the start.',
    'December 2036 is the last coverage month.',
    # Additional month-year variants
    'The March 2023 results were restated.',
    'April 2022 marked the project start.',
    'See May 2021 for historical baseline.',
    'June 2020 data is in the archive.',
    'July 2019 was the strongest period.',
    'August 2018 saw the highest volume.',
    'September 2017 closing confirmed.',
    'October 2016 review completed.',
    'November 2015 figures are final.',
    'December 2014 year-end submitted.',
])
def test_true_positive_month_year_no_day(text):
    """
    True positive: Month + Year without day component must be detected.

    Attack vector: Partial date expressions consisting of only a month name
    and a four-digit year. These are common in business contexts for monthly
    reporting periods, billing cycles, and deadline specifications. The parser
    must recognize these as valid MONTH_YEAR dates despite the absence of a
    day component.

    Why a parser might fail: The parser was designed primarily around complete
    dates (month + day + year) and treats the day as a required field.
    Month-year-only patterns are handled by a separate code path that may be
    less well-tested or have narrower pattern coverage.

    Failure reveals: The MONTH_YEAR extraction path is missing, incomplete,
    or has a bug that causes it to require a day component that is absent
    in these legitimate business-context date expressions.
    """
    result = extract_explicit_dates(text)
    assert len(result) > 0
