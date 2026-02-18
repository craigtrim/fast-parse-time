#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for word-to-number conversion in relative time expressions."""

import pytest
from fast_parse_time import parse_time_references


class TestWordNumberConversion:
    """Tests for basic word number patterns."""

    def test_two_days_ago(self):
        """Word number 'two' should convert to 2."""
        result = parse_time_references('two days ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_three_months_ago(self):
        """Word number 'three' should convert to 3."""
        result = parse_time_references('three months ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_five_hours_ago(self):
        """Word number 'five' should convert to 5."""
        result = parse_time_references('five hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_one_week_ago(self):
        """Word number 'one' should convert to 1."""
        result = parse_time_references('one week ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_one_day_ago(self):
        """Word number 'one' should convert to 1."""
        result = parse_time_references('one day ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'


class TestOnePatternVariations:
    """Tests for 'one X ago' pattern variations."""

    def test_one_month_ago(self):
        """'one month ago' should work."""
        result = parse_time_references('one month ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_one_year_ago(self):
        """'one year ago' should work."""
        result = parse_time_references('one year ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_one_hour_ago(self):
        """'one hour ago' should work."""
        result = parse_time_references('one hour ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_one_minute_ago(self):
        """'one minute ago' should work."""
        result = parse_time_references('one minute ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_one_second_ago(self):
        """'one second ago' should work."""
        result = parse_time_references('one second ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'


class TestDigitOnePatterns:
    """Tests for digit '1 X ago' patterns."""

    def test_1_week_ago(self):
        """'1 week ago' should work."""
        result = parse_time_references('1 week ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_1_day_ago(self):
        """'1 day ago' should work."""
        result = parse_time_references('1 day ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_1_month_ago(self):
        """'1 month ago' should work."""
        result = parse_time_references('1 month ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_1_year_ago(self):
        """'1 year ago' should work."""
        result = parse_time_references('1 year ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'


class TestSentenceContext:
    """Tests for word numbers in sentence context."""

    def test_one_week_ago_in_sentence(self):
        """'one week ago' in a sentence should be extracted."""
        result = parse_time_references('I saw this one week ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_one_day_ago_in_sentence(self):
        """'one day ago' in a sentence should be extracted."""
        result = parse_time_references('the event happened one day ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'


class TestCapitalizationVariations:
    """Tests for capitalization variations."""

    def test_one_week_ago_uppercase(self):
        """'ONE WEEK AGO' should work (case-insensitive)."""
        result = parse_time_references('ONE WEEK AGO')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_one_day_ago_mixed_case(self):
        """'One Day Ago' should work (case-insensitive)."""
        result = parse_time_references('One Day Ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'


class TestAdditionalWordNumbers:
    """Tests for additional word number conversions."""

    def test_four_days_ago(self):
        """Word number 'four' should convert to 4."""
        result = parse_time_references('four days ago')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_six_weeks_ago(self):
        """Word number 'six' should convert to 6."""
        result = parse_time_references('six weeks ago')
        assert len(result) == 1
        assert result[0].cardinality == 6
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_seven_months_ago(self):
        """Word number 'seven' should convert to 7."""
        result = parse_time_references('seven months ago')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_eight_hours_ago(self):
        """Word number 'eight' should convert to 8."""
        result = parse_time_references('eight hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 8
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_nine_minutes_ago(self):
        """Word number 'nine' should convert to 9."""
        result = parse_time_references('nine minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 9
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_ten_seconds_ago(self):
        """Word number 'ten' should convert to 10."""
        result = parse_time_references('ten seconds ago')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_twenty_days_ago(self):
        """Word number 'twenty' should convert to 20."""
        result = parse_time_references('twenty days ago')
        assert len(result) == 1
        assert result[0].cardinality == 20
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_thirty_minutes_ago(self):
        """Word number 'thirty' should convert to 30."""
        result = parse_time_references('thirty minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
