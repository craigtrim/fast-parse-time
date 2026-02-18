#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Tests for the stdlib-based date validator that replaces dateparser.

Related GitHub Issue:
    #29 - Remove dateparser dependency: replace with stdlib datetime
    https://github.com/craigtrim/fast-parse-time/issues/29
"""

import unittest
from fast_parse_time.explicit.dmo.stdlib_date_validator import try_parse_date


class TestFullDelimitedSlash(unittest.TestCase):
    """Full 3-component dates using slash delimiter."""

    def test_mdy_standard(self):
        """Standard US format MM/DD/YYYY."""
        self.assertTrue(try_parse_date('04/08/2024'))

    def test_dmy_european(self):
        """European format DD/MM/YYYY."""
        self.assertTrue(try_parse_date('08/04/2024'))

    def test_mdy_single_digit_month(self):
        """Single-digit month."""
        self.assertTrue(try_parse_date('4/08/2024'))

    def test_mdy_single_digit_day(self):
        """Single-digit day."""
        self.assertTrue(try_parse_date('04/8/2024'))

    def test_mdy_single_digit_both(self):
        """Single-digit month and day."""
        self.assertTrue(try_parse_date('4/8/2024'))

    def test_dmy_day_31(self):
        """Day 31 in a 31-day month."""
        self.assertTrue(try_parse_date('31/01/2024'))

    def test_mdy_december(self):
        """December (month 12)."""
        self.assertTrue(try_parse_date('12/25/2024'))

    def test_mdy_leap_day(self):
        """Feb 29 in a leap year."""
        self.assertTrue(try_parse_date('02/29/2024'))

    def test_ymd_slash(self):
        """Year-first with slash: YYYY/MM/DD."""
        self.assertTrue(try_parse_date('2024/04/08'))

    def test_ymd_slash_single_digit(self):
        """Year-first single-digit month and day."""
        self.assertTrue(try_parse_date('2024/4/8'))


class TestFullDelimitedDash(unittest.TestCase):
    """Full 3-component dates using dash delimiter."""

    def test_iso_standard(self):
        """ISO 8601: YYYY-MM-DD."""
        self.assertTrue(try_parse_date('2024-04-08'))

    def test_iso_december(self):
        """ISO 8601 December."""
        self.assertTrue(try_parse_date('2024-12-31'))

    def test_mdy_dashed(self):
        """Dashed MM-DD-YYYY."""
        self.assertTrue(try_parse_date('04-08-2024'))

    def test_dmy_dashed(self):
        """Dashed DD-MM-YYYY."""
        self.assertTrue(try_parse_date('08-04-2024'))

    def test_iso_leap_day(self):
        """ISO leap day."""
        self.assertTrue(try_parse_date('2024-02-29'))

    def test_iso_jan_first(self):
        """ISO January 1st."""
        self.assertTrue(try_parse_date('2024-01-01'))


class TestFullDelimitedDot(unittest.TestCase):
    """Full 3-component dates using dot delimiter."""

    def test_dot_mdy(self):
        """Dot-separated MM.DD.YYYY."""
        self.assertTrue(try_parse_date('04.08.2024'))

    def test_dot_dmy(self):
        """Dot-separated DD.MM.YYYY."""
        self.assertTrue(try_parse_date('08.04.2024'))

    def test_dot_version_number_style(self):
        """Version-number-style date with 2-digit year: 20.04.01."""
        self.assertTrue(try_parse_date('20.04.01'))

    def test_dot_year_month_day_2digit(self):
        """2-digit year first: 24.04.08."""
        self.assertTrue(try_parse_date('24.04.08'))


class TestPartialDatesSlash(unittest.TestCase):
    """Two-component dates (no year) using slash delimiter."""

    def test_month_day_unambiguous(self):
        """Month/Day where month <= 12 and day > 12: clearly MONTH_DAY."""
        self.assertTrue(try_parse_date('3/15'))

    def test_day_month_unambiguous(self):
        """Day/Month where day > 12: clearly DAY_MONTH."""
        self.assertTrue(try_parse_date('31/03'))

    def test_ambiguous_both_small(self):
        """Both components <= 12: ambiguous but structurally valid."""
        self.assertTrue(try_parse_date('4/8'))

    def test_feb_29_partial(self):
        """Feb 29 as partial date (handled via leap year probe)."""
        self.assertTrue(try_parse_date('29/2'))

    def test_feb_29_partial_mdy(self):
        """Feb 29 month-first as partial date."""
        self.assertTrue(try_parse_date('2/29'))

    def test_calendar_impossible_day(self):
        """Feb 30 doesn't exist but structurally looks like DD/MM."""
        self.assertTrue(try_parse_date('30/2'))

    def test_party_date(self):
        """Typical partial date in context: 7/24."""
        self.assertTrue(try_parse_date('7/24'))

    def test_day_31_month_1(self):
        """Jan 31 partial."""
        self.assertTrue(try_parse_date('31/1'))

    def test_single_digit_both(self):
        """Both components single digit."""
        self.assertTrue(try_parse_date('1/1'))

    def test_month_12_day_1(self):
        """December 1st partial."""
        self.assertTrue(try_parse_date('12/1'))


class TestPartialDatesDash(unittest.TestCase):
    """Two-component dates (no year) using dash delimiter."""

    def test_month_day_dashed(self):
        """MM-DD partial."""
        self.assertTrue(try_parse_date('3-15'))

    def test_day_month_dashed(self):
        """DD-MM partial."""
        self.assertTrue(try_parse_date('31-03'))

    def test_ambiguous_dashed(self):
        """Ambiguous partial with dash."""
        self.assertTrue(try_parse_date('4-8'))

    def test_feb_29_dash(self):
        """Feb 29 partial with dash."""
        self.assertTrue(try_parse_date('29-2'))


class TestPartialDatesDot(unittest.TestCase):
    """Two-component dates (no year) using dot delimiter."""

    def test_month_day_dot(self):
        """MM.DD partial."""
        self.assertTrue(try_parse_date('3.15'))

    def test_day_month_dot(self):
        """DD.MM partial."""
        self.assertTrue(try_parse_date('31.03'))

    def test_ambiguous_dot(self):
        """Ambiguous partial with dot."""
        self.assertTrue(try_parse_date('4.8'))


class TestYearMonthOnly(unittest.TestCase):
    """Two-component year+month dates (no day)."""

    def test_year_month_slash(self):
        """YYYY/MM format."""
        self.assertTrue(try_parse_date('2023/01'))

    def test_year_month_dash(self):
        """YYYY-MM format."""
        self.assertTrue(try_parse_date('2023-01'))

    def test_year_december_slash(self):
        """YYYY/12 format."""
        self.assertTrue(try_parse_date('2024/12'))

    def test_year_december_dash(self):
        """YYYY-12 format."""
        self.assertTrue(try_parse_date('2024-12'))


class TestWrittenMonthWithComma(unittest.TestCase):
    """Written month dates with comma separator (English prose style)."""

    def test_march_comma(self):
        """March 15, 2024."""
        self.assertTrue(try_parse_date('March 15, 2024'))

    def test_abbreviated_mar_comma(self):
        """Mar 15, 2024."""
        self.assertTrue(try_parse_date('Mar 15, 2024'))

    def test_january_comma(self):
        """January 1, 2024."""
        self.assertTrue(try_parse_date('January 1, 2024'))

    def test_december_comma(self):
        """December 31, 2024."""
        self.assertTrue(try_parse_date('December 31, 2024'))

    def test_feb_comma_leap(self):
        """February 29, 2024 — leap year."""
        self.assertTrue(try_parse_date('February 29, 2024'))

    def test_june_comma(self):
        """June 15, 2024."""
        self.assertTrue(try_parse_date('June 15, 2024'))

    def test_sep_abbreviated_comma(self):
        """Sep 15, 2024 (standard 3-letter)."""
        self.assertTrue(try_parse_date('Sep 15, 2024'))

    def test_oct_abbreviated_comma(self):
        """Oct 1, 2024."""
        self.assertTrue(try_parse_date('Oct 1, 2024'))


class TestWrittenMonthNoComma(unittest.TestCase):
    """Written month dates without comma."""

    def test_march_no_comma(self):
        """March 15 2024."""
        self.assertTrue(try_parse_date('March 15 2024'))

    def test_mar_no_comma(self):
        """Mar 15 2024."""
        self.assertTrue(try_parse_date('Mar 15 2024'))

    def test_day_month_year_european(self):
        """15 March 2024 (European order)."""
        self.assertTrue(try_parse_date('15 March 2024'))

    def test_day_abbreviated_month_year(self):
        """15 Mar 2024 (European abbreviated)."""
        self.assertTrue(try_parse_date('15 Mar 2024'))

    def test_january_no_comma(self):
        """January 1 2024."""
        self.assertTrue(try_parse_date('January 1 2024'))

    def test_december_no_comma(self):
        """December 31 2024."""
        self.assertTrue(try_parse_date('December 31 2024'))

    def test_all_months_jan(self):
        self.assertTrue(try_parse_date('January 15 2024'))

    def test_all_months_feb(self):
        self.assertTrue(try_parse_date('February 15 2024'))

    def test_all_months_apr(self):
        self.assertTrue(try_parse_date('April 15 2024'))

    def test_all_months_may(self):
        self.assertTrue(try_parse_date('May 15 2024'))

    def test_all_months_jun(self):
        self.assertTrue(try_parse_date('June 15 2024'))

    def test_all_months_jul(self):
        self.assertTrue(try_parse_date('July 15 2024'))

    def test_all_months_aug(self):
        self.assertTrue(try_parse_date('August 15 2024'))

    def test_all_months_sep(self):
        self.assertTrue(try_parse_date('September 15 2024'))

    def test_all_months_oct(self):
        self.assertTrue(try_parse_date('October 15 2024'))

    def test_all_months_nov(self):
        self.assertTrue(try_parse_date('November 15 2024'))

    def test_all_months_dec(self):
        self.assertTrue(try_parse_date('December 15 2024'))


class TestWrittenMonthYearOnly(unittest.TestCase):
    """Month + year only (no day component)."""

    def test_march_year(self):
        """March 2024."""
        self.assertTrue(try_parse_date('March 2024'))

    def test_mar_year(self):
        """Mar 2024."""
        self.assertTrue(try_parse_date('Mar 2024'))

    def test_january_year(self):
        """January 2024."""
        self.assertTrue(try_parse_date('January 2024'))

    def test_december_year(self):
        """December 2024."""
        self.assertTrue(try_parse_date('December 2024'))

    def test_feb_year(self):
        """Feb 2024."""
        self.assertTrue(try_parse_date('Feb 2024'))

    def test_sep_year(self):
        """Sep 2024."""
        self.assertTrue(try_parse_date('Sep 2024'))


class TestNonStandardAbbreviations(unittest.TestCase):
    """Non-standard month abbreviations that need alias normalisation."""

    def test_sept_with_comma(self):
        """'Sept 15, 2024' — 4-letter Sept variant."""
        self.assertTrue(try_parse_date('Sept 15, 2024'))

    def test_sept_no_comma(self):
        """'Sept 15 2024' without comma."""
        self.assertTrue(try_parse_date('Sept 15 2024'))

    def test_sept_year_only(self):
        """'Sept 2024' — month+year with Sept."""
        self.assertTrue(try_parse_date('Sept 2024'))

    def test_sept_lowercase(self):
        """'sept 15, 2024' — all lowercase."""
        self.assertTrue(try_parse_date('sept 15, 2024'))


class TestShortYearFormats(unittest.TestCase):
    """Dates with 2-digit years (version-number style, etc.)."""

    def test_dot_dmy_short_year(self):
        """DD.MM.YY format."""
        self.assertTrue(try_parse_date('20.04.01'))

    def test_slash_mdy_short_year(self):
        """MM/DD/YY format."""
        self.assertTrue(try_parse_date('04/08/24'))

    def test_slash_dmy_short_year(self):
        """DD/MM/YY format."""
        self.assertTrue(try_parse_date('08/04/24'))


class TestWhitespaceHandling(unittest.TestCase):
    """Whitespace edge cases."""

    def test_leading_spaces(self):
        """Leading whitespace is stripped."""
        self.assertTrue(try_parse_date('   04/08/2024'))

    def test_trailing_spaces(self):
        """Trailing whitespace is stripped."""
        self.assertTrue(try_parse_date('04/08/2024   '))

    def test_both_sides(self):
        """Whitespace on both sides."""
        self.assertTrue(try_parse_date('  04/08/2024  '))

    def test_written_month_with_whitespace(self):
        """Written month with surrounding whitespace."""
        self.assertTrue(try_parse_date('  March 15, 2024  '))

    def test_whitespace_only(self):
        """Whitespace-only string returns False."""
        self.assertFalse(try_parse_date('   '))


class TestInvalidInputs(unittest.TestCase):
    """Inputs that must return False."""

    def test_none(self):
        """None returns False without raising."""
        self.assertFalse(try_parse_date(None))

    def test_empty_string(self):
        """Empty string returns False."""
        self.assertFalse(try_parse_date(''))

    def test_plain_text(self):
        """Non-date text returns False."""
        self.assertFalse(try_parse_date('hello world'))

    def test_single_word(self):
        """Single non-date word returns False."""
        self.assertFalse(try_parse_date('meeting'))

    def test_number_only(self):
        """A standalone number (not a year-month) returns False."""
        self.assertFalse(try_parse_date('42'))

    def test_iso_invalid_month_zero(self):
        """Month 00 in ISO position is invalid."""
        self.assertFalse(try_parse_date('2024-00-01'))

    def test_iso_invalid_month_13(self):
        """Month 13 in ISO position is invalid."""
        self.assertFalse(try_parse_date('2024-13-01'))

    def test_slash_invalid_month_zero(self):
        """Month 00 in slash format is invalid."""
        self.assertFalse(try_parse_date('00/08/2024'))

    def test_slash_invalid_day_zero(self):
        """Day 00 in slash format is invalid."""
        self.assertFalse(try_parse_date('04/00/2024'))

    def test_all_nines(self):
        """99/99/9999 is not a date."""
        self.assertFalse(try_parse_date('99/99/9999'))

    def test_iso_feb_29_nonleap(self):
        """Feb 29 in a non-leap year (2023) is invalid."""
        self.assertFalse(try_parse_date('2023-02-29'))

    def test_iso_feb_30(self):
        """Feb 30 in ISO format is always invalid."""
        self.assertFalse(try_parse_date('2024-02-30'))

    def test_iso_jan_32(self):
        """Day 32 in ISO format is always invalid."""
        self.assertFalse(try_parse_date('2024-01-32'))

    def test_too_many_components(self):
        """Four slash-separated components are not a date."""
        self.assertFalse(try_parse_date('04/08/2024/extra'))

    def test_partial_both_components_zero(self):
        """0/0 both zero — outside plausible range (1-31)."""
        self.assertFalse(try_parse_date('0/0'))

    def test_partial_first_component_zero(self):
        """0/8 first zero — outside plausible range."""
        self.assertFalse(try_parse_date('0/8'))

    def test_partial_second_component_zero(self):
        """4/0 second zero — outside plausible range."""
        self.assertFalse(try_parse_date('4/0'))

    def test_partial_both_over_31(self):
        """32/40 — both over 31, not plausible date components."""
        self.assertFalse(try_parse_date('32/40'))

    def test_text_with_numbers_not_date(self):
        """Text containing numbers but not a date."""
        self.assertFalse(try_parse_date('version 3 released'))

    def test_decimal_number(self):
        """Pi to 3 decimal places — second component exceeds 31, not a date."""
        self.assertFalse(try_parse_date('3.141'))

    def test_url_like(self):
        """URL-like string is not a date."""
        self.assertFalse(try_parse_date('http://example.com'))


class TestBoundaryDates(unittest.TestCase):
    """Boundary values: first/last days, end of months, etc."""

    def test_jan_1(self):
        """January 1st."""
        self.assertTrue(try_parse_date('01/01/2024'))

    def test_dec_31(self):
        """December 31st."""
        self.assertTrue(try_parse_date('12/31/2024'))

    def test_leap_day_2000(self):
        """Leap day in year 2000 (divisible by 400)."""
        self.assertTrue(try_parse_date('02/29/2000'))

    def test_non_leap_year_1900(self):
        """1900 is NOT a leap year (divisible by 100 but not 400)."""
        self.assertFalse(try_parse_date('02/29/1900'))

    def test_century_year_2100(self):
        """2100 is NOT a leap year."""
        self.assertFalse(try_parse_date('02/29/2100'))

    def test_apr_30(self):
        """April 30 — valid last day of April."""
        self.assertTrue(try_parse_date('04/30/2024'))

    def test_apr_31_invalid(self):
        """April 31 — April has only 30 days."""
        self.assertFalse(try_parse_date('2024-04-31'))

    def test_nov_30(self):
        """November 30 — valid."""
        self.assertTrue(try_parse_date('11/30/2024'))

    def test_jun_31_invalid(self):
        """June 31 — June has only 30 days."""
        self.assertFalse(try_parse_date('2024-06-31'))


if __name__ == '__main__':
    unittest.main()
