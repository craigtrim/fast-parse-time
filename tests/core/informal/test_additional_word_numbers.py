#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for word-to-number conversion in relative time expressions."""

import pytest
from fast_parse_time import parse_time_references

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
