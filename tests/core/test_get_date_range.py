#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for get_date_range function."""

import pytest
from datetime import datetime
from fast_parse_time import get_date_range


class TestGetDateRangeBasic:
    """Tests for basic get_date_range behavior."""

    def test_two_past_references_returns_tuple(self):
        """Two past references should return a (start, end) tuple."""
        result = get_date_range('show data from 7 days ago and 3 days ago')
        assert result is not None
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_two_past_references_ordering(self):
        """Returned tuple should be (earlier, later) regardless of text order."""
        result = get_date_range('show data from 7 days ago and 3 days ago')
        assert result is not None
        start, end = result
        assert start < end

    def test_start_is_datetime(self):
        """Start of range should be a datetime object."""
        result = get_date_range('from 7 days ago to 3 days ago')
        assert result is not None
        start, _ = result
        assert isinstance(start, datetime)

    def test_end_is_datetime(self):
        """End of range should be a datetime object."""
        result = get_date_range('from 7 days ago to 3 days ago')
        assert result is not None
        _, end = result
        assert isinstance(end, datetime)


class TestGetDateRangeNoneReturn:
    """Tests for cases where get_date_range returns None."""

    def test_single_reference_returns_none(self):
        """A single time reference should return None (need exactly 2)."""
        result = get_date_range('5 days ago')
        assert result is None

    def test_no_references_returns_none(self):
        """Text with no temporal references should return None."""
        result = get_date_range('Hello world')
        assert result is None

    def test_empty_string_returns_none(self):
        """Empty string should return None."""
        result = get_date_range('')
        assert result is None


class TestGetDateRangeMixedTense:
    """Tests for mixed tense (past and future) date ranges."""

    def test_past_and_future_returns_tuple(self):
        """One past and one future reference should form a valid range."""
        result = get_date_range('last week and next week')
        assert result is not None
        assert isinstance(result, tuple)

    def test_past_and_future_ordering(self):
        """Past should be the start, future should be the end."""
        result = get_date_range('last week and next week')
        assert result is not None
        start, end = result
        assert start < end


class TestGetDateRangeSentenceContext:
    """Tests for get_date_range within sentence context."""

    def test_in_sentence_with_from_to(self):
        """'from X to Y' pattern in a sentence should work."""
        result = get_date_range('show me activity from 30 days ago to 7 days ago')
        assert result is not None
        start, end = result
        assert start < end

    def test_earlier_reference_is_start(self):
        """The earlier date should always be the start of the range."""
        result = get_date_range('show me activity from 30 days ago to 7 days ago')
        assert result is not None
        start, end = result
        now = datetime.now()
        # Start should be approximately 30 days before now
        # End should be approximately 7 days before now
        assert start < end
        assert start < now
        assert end < now


class TestGetDateRangeHoursBased:
    """Tests for hour-based date ranges."""

    def test_hours_based_range_returns_tuple(self):
        """Two hour-based references should return a (start, end) tuple."""
        result = get_date_range('logs from 2 hours ago and 1 hour ago')
        assert result is not None
        assert isinstance(result, tuple)

    def test_hours_based_range_ordering(self):
        """Earlier hour reference should be the start of the range."""
        result = get_date_range('logs from 2 hours ago and 1 hour ago')
        assert result is not None
        start, end = result
        assert start < end


class TestGetDateRangeMinutesBased:
    """Tests for minute-based date ranges."""

    def test_minutes_based_range_returns_tuple(self):
        """Two minute-based references should return a (start, end) tuple."""
        result = get_date_range('events from 30 minutes ago to 10 minutes ago')
        assert result is not None
        assert isinstance(result, tuple)

    def test_minutes_based_ordering(self):
        """Earlier minute reference should be the start of the range."""
        result = get_date_range('events from 30 minutes ago to 10 minutes ago')
        assert result is not None
        start, end = result
        assert start < end


class TestGetDateRangeMonthBased:
    """Tests for month-based date ranges."""

    def test_month_based_range_returns_tuple(self):
        """Two month-based references should return a (start, end) tuple."""
        result = get_date_range('data from 6 months ago to 1 month ago')
        assert result is not None
        assert isinstance(result, tuple)

    def test_month_based_ordering(self):
        """Earlier month reference should be the start of the range."""
        result = get_date_range('data from 6 months ago to 1 month ago')
        assert result is not None
        start, end = result
        assert start < end


class TestGetDateRangeYearBased:
    """Tests for year-based date ranges."""

    def test_year_based_range_returns_tuple(self):
        """Two year-based references should return a (start, end) tuple."""
        result = get_date_range('history from 2 years ago to last year')
        assert result is not None
        assert isinstance(result, tuple)

    def test_year_based_ordering(self):
        """Earlier year reference should be the start of the range."""
        result = get_date_range('history from 2 years ago to last year')
        assert result is not None
        start, end = result
        assert start < end


class TestSameTenseRange:
    """Tests that two references in the same tense still form a valid range."""

    def test_both_past_forms_valid_range(self):
        """Two past-tense references should still yield a valid ordered range."""
        result = get_date_range('from 10 days ago to 5 days ago')
        assert result is not None
        start, end = result
        assert start < end

    def test_both_past_returns_tuple(self):
        """Two past-tense references should return a tuple."""
        result = get_date_range('between 14 days ago and 7 days ago')
        assert result is not None
        assert isinstance(result, tuple)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
