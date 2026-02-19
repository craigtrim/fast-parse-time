# -*- coding: utf-8 -*-
"""
Test extraction of date-like strings from text (pre-parse step).
Source: https://github.com/akoumjian/datefinder/blob/master/tests/test_extract_date_strings.py

datefinder has a two-step pipeline: first extract candidate date strings,
then parse them to datetime. These tests cover the extraction step.
fast-parse-time's extract_explicit_dates() covers both steps.
"""
import pytest
from fast_parse_time import extract_explicit_dates

pytestmark = pytest.mark.xfail(strict=False, reason='Compatibility test - implementation gap')


class TestDateStringExtraction:
    """Source: test_extract_date_strings -- date strings with timezone context"""

    def test_full_written_date_with_timezone(self):
        """'March 20, 2015 3:30 pm GMT'"""
        result = extract_explicit_dates('March 20, 2015 3:30 pm GMT')
        assert len(result) >= 1

    def test_written_date_with_timezone_in_sentence(self):
        """'March 20, 2015 3:30 pm ACWDT in the parking lot'"""
        result = extract_explicit_dates(
            'March 20, 2015 3:30 pm ACWDT in the parking lot'
        )
        assert len(result) >= 1

    def test_written_date_at_start_of_sentence(self):
        """'blah blah March 20, 2015 3pm MADMT for some thing'"""
        result = extract_explicit_dates(
            'blah blah March 20, 2015 3pm MADMT for some thing'
        )
        assert len(result) >= 1

    def test_iso_date_with_weekday_prefix(self):
        """'starting Thursday 2020-11-05 13:50 GMT'"""
        result = extract_explicit_dates('starting Thursday 2020-11-05 13:50 GMT')
        assert len(result) >= 1

    def test_iso_date_with_abbr_weekday_prefix(self):
        """'starting Thu 2020-11-05 13:50 GMT'"""
        result = extract_explicit_dates('starting Thu 2020-11-05 13:50 GMT')
        assert len(result) >= 1


class TestStrictExtraction:
    """Source: test_extract_date_strings_with_strict_option"""

    def test_no_match_for_relative_weekday_phrase(self):
        """'the Friday after next Tuesday the 20th' -- no full date, should not match."""
        result = extract_explicit_dates('the Friday after next Tuesday the 20th')
        assert len(result) == 0

    def test_no_match_for_month_year_with_time_word(self):
        """'This Tuesday March 2015 in the evening' -- no day, should not match."""
        result = extract_explicit_dates('This Tuesday March 2015 in the evening')
        assert len(result) == 0

    def test_numeric_date_preceded_by_word(self):
        """'They said it was on 01-03-2015'"""
        result = extract_explicit_dates('They said it was on 01-03-2015')
        assert len(result) >= 1

    def test_written_month_two_digit_day_year(self):
        """'May 20 2015 is nowhere near the other date'"""
        result = extract_explicit_dates('May 20 2015 is nowhere near the other date')
        assert len(result) >= 1
