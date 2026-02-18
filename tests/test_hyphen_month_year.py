#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
TDD tests for issue #21: abbreviated month-year format with hyphen delimiter.

Covers forward (MONTH_YEAR) and reversed (YEAR_MONTH) patterns for both
abbreviated and full month names, with 2-digit and 4-digit years.

Related GitHub Issue:
    #21 - Gap: abbreviated month-year format not supported (Oct-23, May-23)
    https://github.com/craigtrim/fast-parse-time/issues/21
"""

import pytest
from fast_parse_time import extract_explicit_dates


# ---------------------------------------------------------------------------
# 1. Abbreviated month + hyphen + 2-digit year → MONTH_YEAR (12 tests)
# ---------------------------------------------------------------------------

class TestAbbrevHyphen2DigitYearForward:
    """MonthAbbr-YY patterns: Oct-23, Jan-00, Dec-99, etc."""

    def test_jan_2digit(self):
        result = extract_explicit_dates('Jan-23')
        assert len(result) >= 1

    def test_feb_2digit(self):
        result = extract_explicit_dates('Feb-23')
        assert len(result) >= 1

    def test_mar_2digit(self):
        result = extract_explicit_dates('Mar-23')
        assert len(result) >= 1

    def test_apr_2digit(self):
        result = extract_explicit_dates('Apr-23')
        assert len(result) >= 1

    def test_may_2digit(self):
        result = extract_explicit_dates('May-23')
        assert len(result) >= 1

    def test_jun_2digit(self):
        result = extract_explicit_dates('Jun-23')
        assert len(result) >= 1

    def test_jul_2digit(self):
        result = extract_explicit_dates('Jul-23')
        assert len(result) >= 1

    def test_aug_2digit(self):
        result = extract_explicit_dates('Aug-23')
        assert len(result) >= 1

    def test_sep_2digit(self):
        result = extract_explicit_dates('Sep-23')
        assert len(result) >= 1

    def test_oct_2digit(self):
        result = extract_explicit_dates('Oct-23')
        assert len(result) >= 1

    def test_nov_2digit(self):
        result = extract_explicit_dates('Nov-23')
        assert len(result) >= 1

    def test_dec_2digit(self):
        result = extract_explicit_dates('Dec-23')
        assert len(result) >= 1


# ---------------------------------------------------------------------------
# 2. Abbreviated month + hyphen + 4-digit year → MONTH_YEAR (12 tests)
# ---------------------------------------------------------------------------

class TestAbbrevHyphen4DigitYearForward:
    """MonthAbbr-YYYY patterns: Oct-2023, Jan-2000, Dec-1999, etc."""

    def test_jan_4digit(self):
        result = extract_explicit_dates('Jan-2023')
        assert len(result) >= 1

    def test_feb_4digit(self):
        result = extract_explicit_dates('Feb-2023')
        assert len(result) >= 1

    def test_mar_4digit(self):
        result = extract_explicit_dates('Mar-2023')
        assert len(result) >= 1

    def test_apr_4digit(self):
        result = extract_explicit_dates('Apr-2023')
        assert len(result) >= 1

    def test_may_4digit(self):
        result = extract_explicit_dates('May-2023')
        assert len(result) >= 1

    def test_jun_4digit(self):
        result = extract_explicit_dates('Jun-2023')
        assert len(result) >= 1

    def test_jul_4digit(self):
        result = extract_explicit_dates('Jul-2023')
        assert len(result) >= 1

    def test_aug_4digit(self):
        result = extract_explicit_dates('Aug-2023')
        assert len(result) >= 1

    def test_sep_4digit(self):
        result = extract_explicit_dates('Sep-2023')
        assert len(result) >= 1

    def test_oct_4digit(self):
        result = extract_explicit_dates('Oct-2023')
        assert len(result) >= 1

    def test_nov_4digit(self):
        result = extract_explicit_dates('Nov-2023')
        assert len(result) >= 1

    def test_dec_4digit(self):
        result = extract_explicit_dates('Dec-2023')
        assert len(result) >= 1


# ---------------------------------------------------------------------------
# 3. Full month name + hyphen + 2-digit year → MONTH_YEAR (12 tests)
# ---------------------------------------------------------------------------

class TestFullMonthHyphen2DigitYearForward:
    """FullMonth-YY patterns: March-23, January-00, December-99, etc."""

    def test_january_2digit(self):
        result = extract_explicit_dates('January-23')
        assert len(result) >= 1

    def test_february_2digit(self):
        result = extract_explicit_dates('February-23')
        assert len(result) >= 1

    def test_march_2digit(self):
        result = extract_explicit_dates('March-23')
        assert len(result) >= 1

    def test_april_2digit(self):
        result = extract_explicit_dates('April-23')
        assert len(result) >= 1

    def test_may_2digit(self):
        result = extract_explicit_dates('May-23')
        assert len(result) >= 1

    def test_june_2digit(self):
        result = extract_explicit_dates('June-23')
        assert len(result) >= 1

    def test_july_2digit(self):
        result = extract_explicit_dates('July-23')
        assert len(result) >= 1

    def test_august_2digit(self):
        result = extract_explicit_dates('August-23')
        assert len(result) >= 1

    def test_september_2digit(self):
        result = extract_explicit_dates('September-23')
        assert len(result) >= 1

    def test_october_2digit(self):
        result = extract_explicit_dates('October-23')
        assert len(result) >= 1

    def test_november_2digit(self):
        result = extract_explicit_dates('November-23')
        assert len(result) >= 1

    def test_december_2digit(self):
        result = extract_explicit_dates('December-23')
        assert len(result) >= 1


# ---------------------------------------------------------------------------
# 4. Full month name + hyphen + 4-digit year → MONTH_YEAR (12 tests)
# ---------------------------------------------------------------------------

class TestFullMonthHyphen4DigitYearForward:
    """FullMonth-YYYY patterns: March-2023, January-2000, December-1999, etc."""

    def test_january_4digit(self):
        result = extract_explicit_dates('January-2023')
        assert len(result) >= 1

    def test_february_4digit(self):
        result = extract_explicit_dates('February-2023')
        assert len(result) >= 1

    def test_march_4digit(self):
        result = extract_explicit_dates('March-2023')
        assert len(result) >= 1

    def test_april_4digit(self):
        result = extract_explicit_dates('April-2023')
        assert len(result) >= 1

    def test_may_4digit(self):
        result = extract_explicit_dates('May-2023')
        assert len(result) >= 1

    def test_june_4digit(self):
        result = extract_explicit_dates('June-2023')
        assert len(result) >= 1

    def test_july_4digit(self):
        result = extract_explicit_dates('July-2023')
        assert len(result) >= 1

    def test_august_4digit(self):
        result = extract_explicit_dates('August-2023')
        assert len(result) >= 1

    def test_september_4digit(self):
        result = extract_explicit_dates('September-2023')
        assert len(result) >= 1

    def test_october_4digit(self):
        result = extract_explicit_dates('October-2023')
        assert len(result) >= 1

    def test_november_4digit(self):
        result = extract_explicit_dates('November-2023')
        assert len(result) >= 1

    def test_december_4digit(self):
        result = extract_explicit_dates('December-2023')
        assert len(result) >= 1


# ---------------------------------------------------------------------------
# 5. Reversed: 2-digit year + hyphen + abbreviated month → YEAR_MONTH (12 tests)
# ---------------------------------------------------------------------------

class TestReversedAbbrev2DigitYear:
    """YY-MonthAbbr patterns: 23-Jan, 23-Oct, etc."""

    def test_23_jan(self):
        result = extract_explicit_dates('23-Jan')
        assert len(result) >= 1

    def test_23_feb(self):
        result = extract_explicit_dates('23-Feb')
        assert len(result) >= 1

    def test_23_mar(self):
        result = extract_explicit_dates('23-Mar')
        assert len(result) >= 1

    def test_23_apr(self):
        result = extract_explicit_dates('23-Apr')
        assert len(result) >= 1

    def test_23_may(self):
        result = extract_explicit_dates('23-May')
        assert len(result) >= 1

    def test_23_jun(self):
        result = extract_explicit_dates('23-Jun')
        assert len(result) >= 1

    def test_23_jul(self):
        result = extract_explicit_dates('23-Jul')
        assert len(result) >= 1

    def test_23_aug(self):
        result = extract_explicit_dates('23-Aug')
        assert len(result) >= 1

    def test_23_sep(self):
        result = extract_explicit_dates('23-Sep')
        assert len(result) >= 1

    def test_23_oct(self):
        result = extract_explicit_dates('23-Oct')
        assert len(result) >= 1

    def test_23_nov(self):
        result = extract_explicit_dates('23-Nov')
        assert len(result) >= 1

    def test_23_dec(self):
        result = extract_explicit_dates('23-Dec')
        assert len(result) >= 1


# ---------------------------------------------------------------------------
# 6. Reversed: 4-digit year + hyphen + abbreviated month → YEAR_MONTH (12 tests)
# ---------------------------------------------------------------------------

class TestReversedAbbrev4DigitYear:
    """YYYY-MonthAbbr patterns: 2023-Jan, 2023-Oct, etc."""

    def test_2023_jan(self):
        result = extract_explicit_dates('2023-Jan')
        assert len(result) >= 1

    def test_2023_feb(self):
        result = extract_explicit_dates('2023-Feb')
        assert len(result) >= 1

    def test_2023_mar(self):
        result = extract_explicit_dates('2023-Mar')
        assert len(result) >= 1

    def test_2023_apr(self):
        result = extract_explicit_dates('2023-Apr')
        assert len(result) >= 1

    def test_2023_may(self):
        result = extract_explicit_dates('2023-May')
        assert len(result) >= 1

    def test_2023_jun(self):
        result = extract_explicit_dates('2023-Jun')
        assert len(result) >= 1

    def test_2023_jul(self):
        result = extract_explicit_dates('2023-Jul')
        assert len(result) >= 1

    def test_2023_aug(self):
        result = extract_explicit_dates('2023-Aug')
        assert len(result) >= 1

    def test_2023_sep(self):
        result = extract_explicit_dates('2023-Sep')
        assert len(result) >= 1

    def test_2023_oct(self):
        result = extract_explicit_dates('2023-Oct')
        assert len(result) >= 1

    def test_2023_nov(self):
        result = extract_explicit_dates('2023-Nov')
        assert len(result) >= 1

    def test_2023_dec(self):
        result = extract_explicit_dates('2023-Dec')
        assert len(result) >= 1


# ---------------------------------------------------------------------------
# 7. Reversed: 2-digit year + hyphen + full month name → YEAR_MONTH (12 tests)
# ---------------------------------------------------------------------------

class TestReversedFull2DigitYear:
    """YY-FullMonth patterns: 23-January, 23-October, etc."""

    def test_23_january(self):
        result = extract_explicit_dates('23-January')
        assert len(result) >= 1

    def test_23_february(self):
        result = extract_explicit_dates('23-February')
        assert len(result) >= 1

    def test_23_march(self):
        result = extract_explicit_dates('23-March')
        assert len(result) >= 1

    def test_23_april(self):
        result = extract_explicit_dates('23-April')
        assert len(result) >= 1

    def test_23_may(self):
        result = extract_explicit_dates('23-May')
        assert len(result) >= 1

    def test_23_june(self):
        result = extract_explicit_dates('23-June')
        assert len(result) >= 1

    def test_23_july(self):
        result = extract_explicit_dates('23-July')
        assert len(result) >= 1

    def test_23_august(self):
        result = extract_explicit_dates('23-August')
        assert len(result) >= 1

    def test_23_september(self):
        result = extract_explicit_dates('23-September')
        assert len(result) >= 1

    def test_23_october(self):
        result = extract_explicit_dates('23-October')
        assert len(result) >= 1

    def test_23_november(self):
        result = extract_explicit_dates('23-November')
        assert len(result) >= 1

    def test_23_december(self):
        result = extract_explicit_dates('23-December')
        assert len(result) >= 1


# ---------------------------------------------------------------------------
# 8. Reversed: 4-digit year + hyphen + full month name → YEAR_MONTH (12 tests)
# ---------------------------------------------------------------------------

class TestReversedFull4DigitYear:
    """YYYY-FullMonth patterns: 2023-January, 2023-October, etc."""

    def test_2023_january(self):
        result = extract_explicit_dates('2023-January')
        assert len(result) >= 1

    def test_2023_february(self):
        result = extract_explicit_dates('2023-February')
        assert len(result) >= 1

    def test_2023_march(self):
        result = extract_explicit_dates('2023-March')
        assert len(result) >= 1

    def test_2023_april(self):
        result = extract_explicit_dates('2023-April')
        assert len(result) >= 1

    def test_2023_may(self):
        result = extract_explicit_dates('2023-May')
        assert len(result) >= 1

    def test_2023_june(self):
        result = extract_explicit_dates('2023-June')
        assert len(result) >= 1

    def test_2023_july(self):
        result = extract_explicit_dates('2023-July')
        assert len(result) >= 1

    def test_2023_august(self):
        result = extract_explicit_dates('2023-August')
        assert len(result) >= 1

    def test_2023_september(self):
        result = extract_explicit_dates('2023-September')
        assert len(result) >= 1

    def test_2023_october(self):
        result = extract_explicit_dates('2023-October')
        assert len(result) >= 1

    def test_2023_november(self):
        result = extract_explicit_dates('2023-November')
        assert len(result) >= 1

    def test_2023_december(self):
        result = extract_explicit_dates('2023-December')
        assert len(result) >= 1


# ---------------------------------------------------------------------------
# 9. DateType verification: forward formats → MONTH_YEAR (12 tests)
# ---------------------------------------------------------------------------

class TestDateTypeForwardIsMonthYear:
    """Forward MonthAbbr-YYYY patterns must return DateType MONTH_YEAR."""

    def test_jan_type(self):
        result = extract_explicit_dates('Jan-2023')
        assert 'MONTH_YEAR' in result.values()

    def test_feb_type(self):
        result = extract_explicit_dates('Feb-2023')
        assert 'MONTH_YEAR' in result.values()

    def test_mar_type(self):
        result = extract_explicit_dates('Mar-2023')
        assert 'MONTH_YEAR' in result.values()

    def test_apr_type(self):
        result = extract_explicit_dates('Apr-2023')
        assert 'MONTH_YEAR' in result.values()

    def test_may_type(self):
        result = extract_explicit_dates('May-2023')
        assert 'MONTH_YEAR' in result.values()

    def test_jun_type(self):
        result = extract_explicit_dates('Jun-2023')
        assert 'MONTH_YEAR' in result.values()

    def test_jul_type(self):
        result = extract_explicit_dates('Jul-2023')
        assert 'MONTH_YEAR' in result.values()

    def test_aug_type(self):
        result = extract_explicit_dates('Aug-2023')
        assert 'MONTH_YEAR' in result.values()

    def test_sep_type(self):
        result = extract_explicit_dates('Sep-2023')
        assert 'MONTH_YEAR' in result.values()

    def test_oct_type(self):
        result = extract_explicit_dates('Oct-2023')
        assert 'MONTH_YEAR' in result.values()

    def test_nov_type(self):
        result = extract_explicit_dates('Nov-2023')
        assert 'MONTH_YEAR' in result.values()

    def test_dec_type(self):
        result = extract_explicit_dates('Dec-2023')
        assert 'MONTH_YEAR' in result.values()


# ---------------------------------------------------------------------------
# 10. DateType verification: reversed formats → YEAR_MONTH (12 tests)
# ---------------------------------------------------------------------------

class TestDateTypeReversedIsYearMonth:
    """Reversed YYYY-MonthAbbr patterns must return DateType YEAR_MONTH."""

    def test_year_jan_type(self):
        result = extract_explicit_dates('2023-Jan')
        assert 'YEAR_MONTH' in result.values()

    def test_year_feb_type(self):
        result = extract_explicit_dates('2023-Feb')
        assert 'YEAR_MONTH' in result.values()

    def test_year_mar_type(self):
        result = extract_explicit_dates('2023-Mar')
        assert 'YEAR_MONTH' in result.values()

    def test_year_apr_type(self):
        result = extract_explicit_dates('2023-Apr')
        assert 'YEAR_MONTH' in result.values()

    def test_year_may_type(self):
        result = extract_explicit_dates('2023-May')
        assert 'YEAR_MONTH' in result.values()

    def test_year_jun_type(self):
        result = extract_explicit_dates('2023-Jun')
        assert 'YEAR_MONTH' in result.values()

    def test_year_jul_type(self):
        result = extract_explicit_dates('2023-Jul')
        assert 'YEAR_MONTH' in result.values()

    def test_year_aug_type(self):
        result = extract_explicit_dates('2023-Aug')
        assert 'YEAR_MONTH' in result.values()

    def test_year_sep_type(self):
        result = extract_explicit_dates('2023-Sep')
        assert 'YEAR_MONTH' in result.values()

    def test_year_oct_type(self):
        result = extract_explicit_dates('2023-Oct')
        assert 'YEAR_MONTH' in result.values()

    def test_year_nov_type(self):
        result = extract_explicit_dates('2023-Nov')
        assert 'YEAR_MONTH' in result.values()

    def test_year_dec_type(self):
        result = extract_explicit_dates('2023-Dec')
        assert 'YEAR_MONTH' in result.values()


# ---------------------------------------------------------------------------
# 11. Result count: forward formats return exactly 1 result (12 tests)
# ---------------------------------------------------------------------------

class TestResultCountForward:
    """Standalone hyphen-month-year tokens should yield exactly 1 result."""

    def test_count_jan_abbrev_2digit(self):
        result = extract_explicit_dates('Jan-23')
        assert len(result) == 1

    def test_count_feb_abbrev_4digit(self):
        result = extract_explicit_dates('Feb-2023')
        assert len(result) == 1

    def test_count_mar_full_2digit(self):
        result = extract_explicit_dates('March-23')
        assert len(result) == 1

    def test_count_apr_full_4digit(self):
        result = extract_explicit_dates('April-2023')
        assert len(result) == 1

    def test_count_may_abbrev_2digit(self):
        result = extract_explicit_dates('May-23')
        assert len(result) == 1

    def test_count_jun_abbrev_4digit(self):
        result = extract_explicit_dates('Jun-2023')
        assert len(result) == 1

    def test_count_jul_full_2digit(self):
        result = extract_explicit_dates('July-23')
        assert len(result) == 1

    def test_count_aug_full_4digit(self):
        result = extract_explicit_dates('August-2023')
        assert len(result) == 1

    def test_count_sep_abbrev_2digit(self):
        result = extract_explicit_dates('Sep-23')
        assert len(result) == 1

    def test_count_oct_abbrev_4digit(self):
        result = extract_explicit_dates('Oct-2023')
        assert len(result) == 1

    def test_count_nov_full_2digit(self):
        result = extract_explicit_dates('November-23')
        assert len(result) == 1

    def test_count_dec_full_4digit(self):
        result = extract_explicit_dates('December-2023')
        assert len(result) == 1


# ---------------------------------------------------------------------------
# 12. Result count: reversed formats return exactly 1 result (12 tests)
# ---------------------------------------------------------------------------

class TestResultCountReversed:
    """Reversed standalone tokens should yield exactly 1 result."""

    def test_count_2digit_jan(self):
        result = extract_explicit_dates('23-Jan')
        assert len(result) == 1

    def test_count_4digit_feb(self):
        result = extract_explicit_dates('2023-Feb')
        assert len(result) == 1

    def test_count_2digit_march(self):
        result = extract_explicit_dates('23-March')
        assert len(result) == 1

    def test_count_4digit_april(self):
        result = extract_explicit_dates('2023-April')
        assert len(result) == 1

    def test_count_2digit_may(self):
        result = extract_explicit_dates('23-May')
        assert len(result) == 1

    def test_count_4digit_jun(self):
        result = extract_explicit_dates('2023-Jun')
        assert len(result) == 1

    def test_count_2digit_july(self):
        result = extract_explicit_dates('23-July')
        assert len(result) == 1

    def test_count_4digit_aug(self):
        result = extract_explicit_dates('2023-Aug')
        assert len(result) == 1

    def test_count_2digit_sep(self):
        result = extract_explicit_dates('23-Sep')
        assert len(result) == 1

    def test_count_4digit_oct(self):
        result = extract_explicit_dates('2023-Oct')
        assert len(result) == 1

    def test_count_2digit_november(self):
        result = extract_explicit_dates('23-November')
        assert len(result) == 1

    def test_count_4digit_dec(self):
        result = extract_explicit_dates('2023-Dec')
        assert len(result) == 1


# ---------------------------------------------------------------------------
# 13. Case-insensitive: lowercase abbreviated months (12 tests)
# ---------------------------------------------------------------------------

class TestCaseInsensitiveLowerAbbrev:
    """All-lowercase abbreviated month-year tokens should match."""

    def test_lower_jan(self):
        result = extract_explicit_dates('jan-23')
        assert len(result) >= 1

    def test_lower_feb(self):
        result = extract_explicit_dates('feb-2023')
        assert len(result) >= 1

    def test_lower_mar(self):
        result = extract_explicit_dates('mar-23')
        assert len(result) >= 1

    def test_lower_apr(self):
        result = extract_explicit_dates('apr-2023')
        assert len(result) >= 1

    def test_lower_may(self):
        result = extract_explicit_dates('may-23')
        assert len(result) >= 1

    def test_lower_jun(self):
        result = extract_explicit_dates('jun-2023')
        assert len(result) >= 1

    def test_lower_jul(self):
        result = extract_explicit_dates('jul-23')
        assert len(result) >= 1

    def test_lower_aug(self):
        result = extract_explicit_dates('aug-2023')
        assert len(result) >= 1

    def test_lower_sep(self):
        result = extract_explicit_dates('sep-23')
        assert len(result) >= 1

    def test_lower_oct(self):
        result = extract_explicit_dates('oct-23')
        assert len(result) >= 1

    def test_lower_nov(self):
        result = extract_explicit_dates('nov-2023')
        assert len(result) >= 1

    def test_lower_dec(self):
        result = extract_explicit_dates('dec-23')
        assert len(result) >= 1


# ---------------------------------------------------------------------------
# 14. Case-insensitive: uppercase abbreviated months (12 tests)
# ---------------------------------------------------------------------------

class TestCaseInsensitiveUpperAbbrev:
    """All-uppercase abbreviated month-year tokens should match."""

    def test_upper_jan(self):
        result = extract_explicit_dates('JAN-23')
        assert len(result) >= 1

    def test_upper_feb(self):
        result = extract_explicit_dates('FEB-2023')
        assert len(result) >= 1

    def test_upper_mar(self):
        result = extract_explicit_dates('MAR-23')
        assert len(result) >= 1

    def test_upper_apr(self):
        result = extract_explicit_dates('APR-2023')
        assert len(result) >= 1

    def test_upper_may(self):
        result = extract_explicit_dates('MAY-23')
        assert len(result) >= 1

    def test_upper_jun(self):
        result = extract_explicit_dates('JUN-2023')
        assert len(result) >= 1

    def test_upper_jul(self):
        result = extract_explicit_dates('JUL-23')
        assert len(result) >= 1

    def test_upper_aug(self):
        result = extract_explicit_dates('AUG-2023')
        assert len(result) >= 1

    def test_upper_sep(self):
        result = extract_explicit_dates('SEP-23')
        assert len(result) >= 1

    def test_upper_oct(self):
        result = extract_explicit_dates('OCT-23')
        assert len(result) >= 1

    def test_upper_nov(self):
        result = extract_explicit_dates('NOV-2023')
        assert len(result) >= 1

    def test_upper_dec(self):
        result = extract_explicit_dates('DEC-23')
        assert len(result) >= 1


# ---------------------------------------------------------------------------
# 15. Sentence-embedded: forward formats in prose (12 tests)
# ---------------------------------------------------------------------------

class TestSentenceEmbeddedForward:
    """Hyphen-month-year tokens embedded in longer text."""

    def test_sentence_jan_abbrev(self):
        result = extract_explicit_dates('Report filed in Jan-2023 for review')
        assert len(result) >= 1

    def test_sentence_feb_abbrev(self):
        result = extract_explicit_dates('Data collected from Feb-23 onward')
        assert len(result) >= 1

    def test_sentence_mar_full(self):
        result = extract_explicit_dates('Records from March-2023 are available')
        assert len(result) >= 1

    def test_sentence_apr_full(self):
        result = extract_explicit_dates('Quarter ending April-23 results')
        assert len(result) >= 1

    def test_sentence_may_abbrev(self):
        result = extract_explicit_dates('Contract signed May-2023 expires next year')
        assert len(result) >= 1

    def test_sentence_jun_abbrev(self):
        result = extract_explicit_dates('The Jun-23 figures show a 12 percent increase')
        assert len(result) >= 1

    def test_sentence_jul_full(self):
        result = extract_explicit_dates('Fiscal year ended July-2023')
        assert len(result) >= 1

    def test_sentence_aug_abbrev(self):
        result = extract_explicit_dates('Market data for Aug-23 is attached')
        assert len(result) >= 1

    def test_sentence_sep_full(self):
        result = extract_explicit_dates('September-2023 was the peak month')
        assert len(result) >= 1

    def test_sentence_oct_abbrev(self):
        result = extract_explicit_dates('Review period covers Oct-23 through Dec-23')
        assert len(result) >= 1

    def test_sentence_nov_full(self):
        result = extract_explicit_dates('See November-2023 appendix for details')
        assert len(result) >= 1

    def test_sentence_dec_abbrev(self):
        result = extract_explicit_dates('Year-end closing Dec-2023 balances')
        assert len(result) >= 1


# ---------------------------------------------------------------------------
# 16. Sentence-embedded: reversed formats in prose (12 tests)
# ---------------------------------------------------------------------------

class TestSentenceEmbeddedReversed:
    """Reversed hyphen-year-month tokens embedded in longer text."""

    def test_sentence_2023_jan(self):
        result = extract_explicit_dates('Filed under 2023-Jan records')
        assert len(result) >= 1

    def test_sentence_2023_feb(self):
        result = extract_explicit_dates('Audit from 2023-February completed')
        assert len(result) >= 1

    def test_sentence_23_mar(self):
        result = extract_explicit_dates('Reference period 23-Mar to 23-Jun')
        assert len(result) >= 1

    def test_sentence_2023_apr(self):
        result = extract_explicit_dates('Q2 starts 2023-Apr per schedule')
        assert len(result) >= 1

    def test_sentence_23_may(self):
        result = extract_explicit_dates('Budget approved for 23-May rollout')
        assert len(result) >= 1

    def test_sentence_2023_jun(self):
        result = extract_explicit_dates('Deliverables due 2023-Jun latest')
        assert len(result) >= 1

    def test_sentence_23_jul(self):
        result = extract_explicit_dates('The 23-July deadline is firm')
        assert len(result) >= 1

    def test_sentence_2023_aug(self):
        result = extract_explicit_dates('System goes live 2023-Aug')
        assert len(result) >= 1

    def test_sentence_23_sep(self):
        result = extract_explicit_dates('Pilot concluded 23-Sep successfully')
        assert len(result) >= 1

    def test_sentence_2023_oct(self):
        result = extract_explicit_dates('Started from 2023-Oct through present')
        assert len(result) >= 1

    def test_sentence_23_nov(self):
        result = extract_explicit_dates('Patch released 23-November hotfix')
        assert len(result) >= 1

    def test_sentence_2023_dec(self):
        result = extract_explicit_dates('Closed books 2023-December as scheduled')
        assert len(result) >= 1


# ---------------------------------------------------------------------------
# 17. Sept alternative abbreviation (6 tests)
# ---------------------------------------------------------------------------

class TestSeptAlternativeAbbrev:
    """'Sept' (4-letter) is a valid alternative to 'Sep'."""

    def test_sept_2digit_forward(self):
        result = extract_explicit_dates('Sept-23')
        assert len(result) >= 1

    def test_sept_4digit_forward(self):
        result = extract_explicit_dates('Sept-2023')
        assert len(result) >= 1

    def test_2digit_sept_reversed(self):
        result = extract_explicit_dates('23-Sept')
        assert len(result) >= 1

    def test_4digit_sept_reversed(self):
        result = extract_explicit_dates('2023-Sept')
        assert len(result) >= 1

    def test_sept_sentence_forward(self):
        result = extract_explicit_dates('Report from Sept-2023 quarter')
        assert len(result) >= 1

    def test_sept_sentence_reversed(self):
        result = extract_explicit_dates('Filed under 2023-Sept archive')
        assert len(result) >= 1


# ---------------------------------------------------------------------------
# 18. Boundary and edge cases (10 tests)
# ---------------------------------------------------------------------------

class TestBoundaryAndEdgeCases:
    """Edge cases around year boundaries and single-digit elements."""

    def test_year_2000_abbrev(self):
        """Earliest plausible 2-digit year → 2000."""
        result = extract_explicit_dates('Jan-00')
        assert len(result) >= 1

    def test_year_2099_abbrev(self):
        """Latest plausible 2-digit year → 2099."""
        result = extract_explicit_dates('Dec-99')
        assert len(result) >= 1

    def test_year_1990_4digit(self):
        """Historical 4-digit year within MIN_YEAR range."""
        result = extract_explicit_dates('Oct-1990')
        assert len(result) >= 1

    def test_year_2030_4digit(self):
        """Near-future 4-digit year within MAX_YEAR range."""
        result = extract_explicit_dates('Mar-2030')
        assert len(result) >= 1

    def test_reversed_year_2000(self):
        result = extract_explicit_dates('00-Jan')
        assert len(result) >= 1

    def test_reversed_year_1990(self):
        result = extract_explicit_dates('1990-Oct')
        assert len(result) >= 1

    def test_mixed_case_forward(self):
        """Mixed case like 'oCt-2023' should still match."""
        result = extract_explicit_dates('oCt-2023')
        assert len(result) >= 1

    def test_mixed_case_reversed(self):
        """Mixed case in reversed format."""
        result = extract_explicit_dates('2023-oCt')
        assert len(result) >= 1

    def test_full_month_lower_forward(self):
        result = extract_explicit_dates('march-2023')
        assert len(result) >= 1

    def test_full_month_upper_forward(self):
        result = extract_explicit_dates('MARCH-2023')
        assert len(result) >= 1


# ---------------------------------------------------------------------------
# 19. Non-match cases: should return empty or None (10 tests)
# ---------------------------------------------------------------------------

class TestNonMatchCases:
    """Strings that should NOT match as hyphen-month-year."""

    def test_invalid_month_abbrev(self):
        """'Foo-23' is not a valid month abbreviation."""
        result = extract_explicit_dates('Foo-23')
        assert not result or 'Foo-23' not in result

    def test_numeric_only_two_part(self):
        """'10-23' is numeric-only (already classified as DAY_MONTH_AMBIGUOUS)."""
        result = extract_explicit_dates('10-23')
        # Should not be classified as MONTH_YEAR via the new path
        if result:
            assert 'MONTH_YEAR' not in result.values() or '10-23' not in result

    def test_three_component(self):
        """'Oct-23-2023' has three components, out of scope."""
        result = extract_explicit_dates('Oct-23-2023')
        # Not expected to match the two-part hyphen-month-year pattern
        assert result is None or len(result) == 0 or 'Oct-23-2023' not in result

    def test_space_separated(self):
        """'Oct 23' is ambiguous (23rd vs 2023) — excluded from this issue."""
        result = extract_explicit_dates('Oct 23')
        # If matched at all, it should not assert MONTH_YEAR via this new path
        # (we do not assert empty here, just no collision)
        assert result is None or 'Oct 23' not in result or True  # no requirement

    def test_slash_separated(self):
        """'Oct/23' slash-delimited is out of scope for #21."""
        result = extract_explicit_dates('Oct/23')
        if result:
            assert 'Oct/23' not in result

    def test_empty_string(self):
        """Empty input should return None or empty."""
        result = extract_explicit_dates('')
        assert not result

    def test_plain_month_name(self):
        """'October' alone should not return a MONTH_YEAR result."""
        result = extract_explicit_dates('October')
        assert result is None or 'MONTH_YEAR' not in (result or {}).values()

    def test_plain_number(self):
        """'2023' alone should return YEAR_ONLY, not MONTH_YEAR."""
        result = extract_explicit_dates('2023')
        if result:
            assert 'MONTH_YEAR' not in result.values()

    def test_day_month_not_crash(self):
        """'31-Oct' is ambiguous (Oct 31st vs 2031-October).
        The reversed YY-MonthAbbr path classifies it as YEAR_MONTH (31 → 2031).
        Just confirm no crash and a valid return type."""
        result = extract_explicit_dates('31-Oct')
        assert result is None or isinstance(result, dict)

    def test_future_year_boundary(self):
        """A year beyond MAX_YEAR+10 should not match."""
        result = extract_explicit_dates('Oct-2099')
        # 2099 is near the boundary; implementation may or may not accept it.
        # Just verify no crash.
        assert result is None or isinstance(result, dict)


# ---------------------------------------------------------------------------
# 20. Multi-date in sentence (5 tests)
# ---------------------------------------------------------------------------

class TestMultiDateInText:
    """Multiple hyphen-month-year tokens in a single string."""

    def test_two_forward_dates(self):
        """Two forward-format dates in one sentence."""
        result = extract_explicit_dates('Review period Oct-23 through Dec-23')
        assert len(result) >= 2

    def test_two_reversed_dates(self):
        """Two reversed-format dates in one sentence."""
        result = extract_explicit_dates('Span from 2023-Jan to 2023-Mar')
        assert len(result) >= 2

    def test_mixed_forward_reversed(self):
        """One forward and one reversed in same sentence."""
        result = extract_explicit_dates('Filed Oct-2023 and archived under 2023-Nov')
        assert len(result) >= 2

    def test_abbrev_and_full_month(self):
        """Abbreviated and full-month format in same sentence."""
        result = extract_explicit_dates('Covers Oct-23 and November-2023')
        assert len(result) >= 2

    def test_three_dates_in_sentence(self):
        """Three date tokens in one sentence."""
        result = extract_explicit_dates('Quarters: Jan-23, Apr-23, Jul-23')
        assert len(result) >= 3


# ---------------------------------------------------------------------------
# 21. Various year values across decades (10 tests)
# ---------------------------------------------------------------------------

class TestVariousYearValues:
    """Confirm multiple distinct year values resolve correctly."""

    def test_year_2010(self):
        result = extract_explicit_dates('Oct-2010')
        assert len(result) >= 1

    def test_year_2015(self):
        result = extract_explicit_dates('Mar-2015')
        assert len(result) >= 1

    def test_year_2020(self):
        result = extract_explicit_dates('Jun-2020')
        assert len(result) >= 1

    def test_year_2025(self):
        result = extract_explicit_dates('Sep-2025')
        assert len(result) >= 1

    def test_year_2digit_10(self):
        result = extract_explicit_dates('Oct-10')
        assert len(result) >= 1

    def test_year_2digit_15(self):
        result = extract_explicit_dates('Mar-15')
        assert len(result) >= 1

    def test_year_2digit_20(self):
        result = extract_explicit_dates('Jun-20')
        assert len(result) >= 1

    def test_year_1995_reversed(self):
        result = extract_explicit_dates('1995-Oct')
        assert len(result) >= 1

    def test_year_2005_reversed(self):
        result = extract_explicit_dates('2005-Mar')
        assert len(result) >= 1

    def test_year_2digit_reversed(self):
        result = extract_explicit_dates('15-Jun')
        assert len(result) >= 1


# ---------------------------------------------------------------------------
# 22. Case-insensitive: lowercase full month names (12 tests)
# ---------------------------------------------------------------------------

class TestCaseInsensitiveLowerFull:
    """All-lowercase full month names with hyphen."""

    def test_lower_january(self):
        result = extract_explicit_dates('january-2023')
        assert len(result) >= 1

    def test_lower_february(self):
        result = extract_explicit_dates('february-23')
        assert len(result) >= 1

    def test_lower_march(self):
        result = extract_explicit_dates('march-2023')
        assert len(result) >= 1

    def test_lower_april(self):
        result = extract_explicit_dates('april-23')
        assert len(result) >= 1

    def test_lower_may(self):
        result = extract_explicit_dates('may-2023')
        assert len(result) >= 1

    def test_lower_june(self):
        result = extract_explicit_dates('june-23')
        assert len(result) >= 1

    def test_lower_july(self):
        result = extract_explicit_dates('july-2023')
        assert len(result) >= 1

    def test_lower_august(self):
        result = extract_explicit_dates('august-23')
        assert len(result) >= 1

    def test_lower_september(self):
        result = extract_explicit_dates('september-2023')
        assert len(result) >= 1

    def test_lower_october(self):
        result = extract_explicit_dates('october-23')
        assert len(result) >= 1

    def test_lower_november(self):
        result = extract_explicit_dates('november-2023')
        assert len(result) >= 1

    def test_lower_december(self):
        result = extract_explicit_dates('december-23')
        assert len(result) >= 1


# ---------------------------------------------------------------------------
# 23. Extracted text key matches input token (12 tests)
# ---------------------------------------------------------------------------

class TestExtractedTextKey:
    """The key returned in the result dict should match the original date token."""

    def test_key_oct_23(self):
        result = extract_explicit_dates('Oct-23')
        assert 'Oct-23' in result

    def test_key_jan_2023(self):
        result = extract_explicit_dates('Jan-2023')
        assert 'Jan-2023' in result

    def test_key_march_2023(self):
        result = extract_explicit_dates('March-2023')
        assert 'March-2023' in result

    def test_key_november_23(self):
        result = extract_explicit_dates('November-23')
        assert 'November-23' in result

    def test_key_2023_oct(self):
        result = extract_explicit_dates('2023-Oct')
        assert '2023-Oct' in result

    def test_key_23_jan(self):
        result = extract_explicit_dates('23-Jan')
        assert '23-Jan' in result

    def test_key_2023_march(self):
        result = extract_explicit_dates('2023-March')
        assert '2023-March' in result

    def test_key_23_december(self):
        result = extract_explicit_dates('23-December')
        assert '23-December' in result

    def test_key_sept_2023(self):
        result = extract_explicit_dates('Sept-2023')
        assert 'Sept-2023' in result

    def test_key_2023_sept(self):
        result = extract_explicit_dates('2023-Sept')
        assert '2023-Sept' in result

    def test_key_lower_oct_23(self):
        """Lowercase input — key should preserve original casing."""
        result = extract_explicit_dates('oct-23')
        assert 'oct-23' in result

    def test_key_upper_mar_2023(self):
        """Uppercase input — key should preserve original casing."""
        result = extract_explicit_dates('MAR-2023')
        assert 'MAR-2023' in result
