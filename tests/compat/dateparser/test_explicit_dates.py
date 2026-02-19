# -*- coding: utf-8 -*-
"""
Test explicit date extraction from text.
Source: https://github.com/scrapinghub/dateparser/blob/master/tests/test_clean_api.py
        https://github.com/scrapinghub/dateparser/blob/master/tests/test_search.py
English-language cases only.
"""
import pytest
from fast_parse_time import extract_explicit_dates

pytestmark = pytest.mark.xfail(strict=False, reason='Compatibility test - implementation gap')


class TestAbsoluteDateStrings:
    """
    Source: test_clean_api.py -- absolute date strings.
    dateparser.parse() resolves these to datetime objects.
    fast-parse-time classifies them by type.
    """

    def test_january_25_2014(self):
        result = extract_explicit_dates('January 25, 2014')
        assert len(result) == 1
        assert 'January 25, 2014' in result

    def test_may_5_2000_with_time(self):
        """Date with time component -- extract the date portion."""
        result = extract_explicit_dates('May 5, 2000 13:00')
        assert len(result) >= 1

    def test_august_8_2018_with_am_pm(self):
        result = extract_explicit_dates('August 8, 2018 5 PM')
        assert len(result) >= 1

    def test_february_26_1981(self):
        result = extract_explicit_dates('February 26, 1981 5 am UTC')
        assert len(result) >= 1

    def test_oct_23_month_year(self):
        """
        'Oct-23' is a month-year format.
        dateparser interprets this as October 2023.
        fast-parse-time should extract it as a date token.
        """
        result = extract_explicit_dates('Oct-23')
        assert len(result) >= 1

    def test_may_23_month_year(self):
        result = extract_explicit_dates('May-23')
        assert len(result) >= 1


class TestDateSearchInText:
    """
    Source: test_search.py -- dates embedded in free-form text.
    dateparser.search.search_dates() finds all dates within a string.
    fast-parse-time extract_explicit_dates() does the same for its supported formats.
    """

    def test_sep_03_2014(self):
        result = extract_explicit_dates('Sep 03 2014')
        assert len(result) >= 1

    def test_full_written_date_in_sentence(self):
        """'friday, 03 september 2014' -- date embedded with weekday prefix."""
        result = extract_explicit_dates('friday, 03 september 2014')
        assert len(result) >= 1

    def test_aug_06_2018_with_time_and_timezone(self):
        """Date with time and timezone abbreviation."""
        result = extract_explicit_dates('Aug 06, 2018 05:05 PM CDT')
        assert len(result) >= 1

    def test_numeric_date_in_sentence(self):
        result = extract_explicit_dates('the meeting is on 04/08/2024')
        assert '04/08/2024' in result

    def test_iso_date_in_sentence(self):
        result = extract_explicit_dates('report filed 2023-09-15 by the team')
        assert '2023-09-15' in result

    def test_multiple_dates_in_text(self):
        """Multiple dates in one string -- all should be found."""
        result = extract_explicit_dates(
            'between 01/15/2024 and 03/20/2024'
        )
        assert len(result) == 2

    def test_date_range_sentence(self):
        result = extract_explicit_dates('from March 15, 2024 to April 1, 2024')
        assert len(result) >= 1
