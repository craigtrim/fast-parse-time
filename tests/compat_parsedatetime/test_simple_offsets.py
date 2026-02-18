# -*- coding: utf-8 -*-
"""
Test parsing of 'simple' offsets.
Source: https://github.com/bear/parsedatetime/blob/master/tests/TestSimpleOffsets.py
"""
import pytest
from fast_parse_time import parse_time_references

pytestmark = pytest.mark.xfail(strict=False, reason='Compatibility test - implementation gap')


class TestNow:
    """Source: testNow, testRightNow"""

    def test_now(self):
        result = parse_time_references('now')
        assert len(result) == 1
        assert result[0].tense == 'present'
        assert result[0].cardinality == 0

    def test_right_now(self):
        result = parse_time_references('right now')
        assert len(result) == 1
        assert result[0].tense == 'present'
        assert result[0].cardinality == 0


class TestMinutesFromNow:
    """Source: testMinutesFromNow"""

    def test_5_minutes_from_now(self):
        result = parse_time_references('5 minutes from now')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'minute'
        assert result[0].tense == 'future'

    def test_5_min_from_now(self):
        result = parse_time_references('5 min from now')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'minute'
        assert result[0].tense == 'future'

    def test_in_5_minutes(self):
        result = parse_time_references('in 5 minutes')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'minute'
        assert result[0].tense == 'future'

    def test_in_5_min(self):
        result = parse_time_references('in 5 min')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'minute'
        assert result[0].tense == 'future'

    def test_five_minutes_from_now(self):
        result = parse_time_references('five minutes from now')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'minute'
        assert result[0].tense == 'future'

    def test_five_min_from_now(self):
        result = parse_time_references('five min from now')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'minute'
        assert result[0].tense == 'future'

    def test_in_five_minutes(self):
        result = parse_time_references('in five minutes')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'minute'
        assert result[0].tense == 'future'

    def test_in_five_min(self):
        result = parse_time_references('in five min')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'minute'
        assert result[0].tense == 'future'


class TestMinutesBeforeNow:
    """Source: testMinutesBeforeNow"""

    def test_5_minutes_before_now(self):
        result = parse_time_references('5 minutes before now')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_5_min_before_now(self):
        result = parse_time_references('5 min before now')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_5_minutes_ago(self):
        result = parse_time_references('5 minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_five_minutes_before_now(self):
        result = parse_time_references('five minutes before now')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_five_min_before_now(self):
        result = parse_time_references('five min before now')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'


class TestWeekFromNow:
    """Source: testWeekFromNow"""

    def test_in_1_week(self):
        result = parse_time_references('in 1 week')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'future'

    def test_1_week_from_now(self):
        result = parse_time_references('1 week from now')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'future'

    def test_in_one_week(self):
        result = parse_time_references('in one week')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'future'

    def test_one_week_from_now(self):
        result = parse_time_references('one week from now')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'future'

    def test_in_a_week(self):
        result = parse_time_references('in a week')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'future'

    def test_a_week_from_now(self):
        result = parse_time_references('a week from now')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'future'

    def test_in_7_days(self):
        result = parse_time_references('in 7 days')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'day'
        assert result[0].tense == 'future'

    def test_7_days_from_now(self):
        result = parse_time_references('7 days from now')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'day'
        assert result[0].tense == 'future'

    def test_in_seven_days(self):
        result = parse_time_references('in seven days')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'day'
        assert result[0].tense == 'future'

    def test_seven_days_from_now(self):
        result = parse_time_references('seven days from now')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'day'
        assert result[0].tense == 'future'

    def test_next_week(self):
        result = parse_time_references('next week')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'future'


class TestNextWeekDay:
    """Source: testNextWeekDay"""

    def test_next_friday(self):
        result = parse_time_references('next friday')
        assert len(result) == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'future'


class TestWeekBeforeNow:
    """Source: testWeekBeforeNow"""

    def test_1_week_before_now(self):
        result = parse_time_references('1 week before now')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_one_week_before_now(self):
        result = parse_time_references('one week before now')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_a_week_before_now(self):
        result = parse_time_references('a week before now')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_7_days_before_now(self):
        result = parse_time_references('7 days before now')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_seven_days_before_now(self):
        result = parse_time_references('seven days before now')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_1_week_ago(self):
        result = parse_time_references('1 week ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_a_week_ago(self):
        result = parse_time_references('a week ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_last_week(self):
        result = parse_time_references('last week')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'


class TestSpecials:
    """Source: testSpecials in TestSimpleOffsets"""

    def test_tomorrow(self):
        result = parse_time_references('tomorrow')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'future'

    def test_next_day(self):
        result = parse_time_references('next day')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'future'

    def test_yesterday(self):
        result = parse_time_references('yesterday')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_today(self):
        result = parse_time_references('today')
        assert len(result) == 1
        assert result[0].cardinality == 0
        assert result[0].frame == 'day'
        assert result[0].tense == 'present'
