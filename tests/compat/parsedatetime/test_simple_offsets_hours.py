# -*- coding: utf-8 -*-
"""
Test parsing of hour offsets.
Source: https://github.com/bear/parsedatetime/blob/master/tests/TestSimpleOffsetsHours.py
"""
import pytest
from fast_parse_time import parse_time_references

pytestmark = pytest.mark.xfail(strict=False, reason='Compatibility test - implementation gap')


class TestHoursFromNow:
    """Source: testHoursFromNow"""

    def test_5_hours_from_now(self):
        result = parse_time_references('5 hours from now')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'hour'
        assert result[0].tense == 'future'

    def test_5_hour_from_now(self):
        result = parse_time_references('5 hour from now')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'hour'
        assert result[0].tense == 'future'

    def test_5_hr_from_now(self):
        result = parse_time_references('5 hr from now')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'hour'
        assert result[0].tense == 'future'

    def test_in_5_hours(self):
        result = parse_time_references('in 5 hours')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'hour'
        assert result[0].tense == 'future'

    def test_in_5_hour(self):
        result = parse_time_references('in 5 hour')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'hour'
        assert result[0].tense == 'future'

    def test_five_hours_from_now(self):
        result = parse_time_references('five hours from now')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'hour'
        assert result[0].tense == 'future'

    def test_five_hour_from_now(self):
        result = parse_time_references('five hour from now')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'hour'
        assert result[0].tense == 'future'

    def test_in_five_hours(self):
        result = parse_time_references('in five hours')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'hour'
        assert result[0].tense == 'future'

    def test_in_five_hour(self):
        result = parse_time_references('in five hour')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'hour'
        assert result[0].tense == 'future'

    def test_an_hour_from_now(self):
        result = parse_time_references('an hour from now')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'future'

    def test_in_an_hour(self):
        result = parse_time_references('in an hour')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'future'


class TestHoursBeforeNow:
    """Source: testHoursBeforeNow"""

    def test_5_hours_before_now(self):
        result = parse_time_references('5 hours before now')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_5_hr_before_now(self):
        result = parse_time_references('5 hr before now')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_five_hours_before_now(self):
        result = parse_time_references('five hours before now')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_five_hr_before_now(self):
        result = parse_time_references('five hr before now')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_an_hour_before_now(self):
        result = parse_time_references('an hour before now')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_an_hr_before_now(self):
        result = parse_time_references('an hr before now')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'
