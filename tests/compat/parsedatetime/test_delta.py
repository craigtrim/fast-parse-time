# -*- coding: utf-8 -*-
"""
Test time delta parsing (integer and float values).
Source: https://github.com/bear/parsedatetime/blob/master/tests/TestDelta.py
"""
import pytest
from fast_parse_time import parse_time_references

pytestmark = pytest.mark.xfail(strict=False, reason='Compatibility test - implementation gap')


class TestIntegerDeltas:
    """Source: testInteger -- integer cardinality values"""

    def test_5_minutes_ago(self):
        result = parse_time_references('5 minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_34_hours_ago(self):
        result = parse_time_references('34 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 34
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_2_days_ago(self):
        result = parse_time_references('2 days ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'


class TestFloatDeltas:
    """
    Source: testFloat -- float cardinality values.
    parsedatetime supports fractional quantities like '7.2 days ago'.
    """

    def test_7_point_2_days_ago(self):
        result = parse_time_references('7.2 days ago')
        assert len(result) == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_8_point_3_hours_ago(self):
        result = parse_time_references('8.3 hours ago')
        assert len(result) == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_1_point_4_months_ago(self):
        result = parse_time_references('1.4 months ago')
        assert len(result) == 1
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_4_point_8_months_ago(self):
        result = parse_time_references('4.8 months ago')
        assert len(result) == 1
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_5_point_11_years_ago(self):
        result = parse_time_references('5.11553 years ago')
        assert len(result) == 1
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'
