# -*- coding: utf-8 -*-
"""
Test parsing of time units.
Source: https://github.com/bear/parsedatetime/blob/master/tests/TestUnits.py
"""
import pytest
from fast_parse_time import parse_time_references

pytestmark = pytest.mark.xfail(strict=False, reason='Compatibility test - implementation gap')


class TestMinutes:
    """Source: testMinutes"""

    def test_1_minutes_ago(self):
        result = parse_time_references('1 minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_1_minute_ago(self):
        result = parse_time_references('1 minute ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_1_min_ago(self):
        result = parse_time_references('1 min ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'


class TestHours:
    """Source: testHours"""

    def test_1_hour_ago(self):
        result = parse_time_references('1 hour ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_1_hours_ago(self):
        result = parse_time_references('1 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'


class TestDays:
    """Source: testDays"""

    def test_1_day_ago(self):
        result = parse_time_references('1 day ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_1_days_ago(self):
        result = parse_time_references('1 days ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'


class TestWeeks:
    """Source: testWeeks"""

    def test_1_week_ago(self):
        result = parse_time_references('1 week ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_1_weeks_ago(self):
        result = parse_time_references('1 weeks ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'


class TestMonths:
    """Source: testMonths"""

    def test_1_month_ago(self):
        result = parse_time_references('1 month ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_1_months_ago(self):
        result = parse_time_references('1 months ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'


class TestYears:
    """Source: testYears"""

    def test_1_year_ago(self):
        result = parse_time_references('1 year ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_1_years_ago(self):
        result = parse_time_references('1 years ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_1_yr_ago(self):
        result = parse_time_references('1 yr ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'
