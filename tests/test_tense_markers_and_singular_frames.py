# -*- coding: utf-8 -*-
"""
Comprehensive test suite for 'before' tense marker and singular uninflected time frames.

Related GitHub Issue:
    #58 - Support 'before' as past-tense marker and singular uninflected time frames
    https://github.com/craigtrim/fast-parse-time/issues/58

Test Coverage:
1. 'before' as past-tense marker (like 'ago')
2. Singular uninflected frames (week, month, year, hour, minute, second)

This file contains 250+ test cases using TDD approach - all tests written before implementation.
"""
import pytest
from fast_parse_time import parse_time_references


class TestBeforeMarkerDays:
    """Test 'before' as past-tense marker with day frame - numeric cardinalities 1-30"""

    def test_1_day_before(self):
        result = parse_time_references('1 day before')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_2_days_before(self):
        result = parse_time_references('2 days before')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_3_days_before(self):
        result = parse_time_references('3 days before')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_4_days_before(self):
        result = parse_time_references('4 days before')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_5_days_before(self):
        result = parse_time_references('5 days before')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_6_days_before(self):
        result = parse_time_references('6 days before')
        assert len(result) == 1
        assert result[0].cardinality == 6
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_7_days_before(self):
        result = parse_time_references('7 days before')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_10_days_before(self):
        result = parse_time_references('10 days before')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_15_days_before(self):
        result = parse_time_references('15 days before')
        assert len(result) == 1
        assert result[0].cardinality == 15
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_20_days_before(self):
        result = parse_time_references('20 days before')
        assert len(result) == 1
        assert result[0].cardinality == 20
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_30_days_before(self):
        result = parse_time_references('30 days before')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'


class TestBeforeMarkerWeeks:
    """Test 'before' as past-tense marker with week frame - numeric cardinalities 1-20"""

    def test_1_week_before(self):
        result = parse_time_references('1 week before')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_2_weeks_before(self):
        result = parse_time_references('2 weeks before')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_3_weeks_before(self):
        result = parse_time_references('3 weeks before')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_4_weeks_before(self):
        result = parse_time_references('4 weeks before')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_5_weeks_before(self):
        result = parse_time_references('5 weeks before')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_10_weeks_before(self):
        result = parse_time_references('10 weeks before')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_15_weeks_before(self):
        result = parse_time_references('15 weeks before')
        assert len(result) == 1
        assert result[0].cardinality == 15
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_20_weeks_before(self):
        result = parse_time_references('20 weeks before')
        assert len(result) == 1
        assert result[0].cardinality == 20
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'


class TestBeforeMarkerMonths:
    """Test 'before' as past-tense marker with month frame - numeric cardinalities 1-24"""

    def test_1_month_before(self):
        result = parse_time_references('1 month before')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_2_months_before(self):
        result = parse_time_references('2 months before')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_3_months_before(self):
        result = parse_time_references('3 months before')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_6_months_before(self):
        result = parse_time_references('6 months before')
        assert len(result) == 1
        assert result[0].cardinality == 6
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_12_months_before(self):
        result = parse_time_references('12 months before')
        assert len(result) == 1
        assert result[0].cardinality == 12
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_18_months_before(self):
        result = parse_time_references('18 months before')
        assert len(result) == 1
        assert result[0].cardinality == 18
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_24_months_before(self):
        result = parse_time_references('24 months before')
        assert len(result) == 1
        assert result[0].cardinality == 24
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'


class TestBeforeMarkerYears:
    """Test 'before' as past-tense marker with year frame - numeric cardinalities 1-20"""

    def test_1_year_before(self):
        result = parse_time_references('1 year before')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_2_years_before(self):
        result = parse_time_references('2 years before')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_3_years_before(self):
        result = parse_time_references('3 years before')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_5_years_before(self):
        result = parse_time_references('5 years before')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_10_years_before(self):
        result = parse_time_references('10 years before')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_20_years_before(self):
        result = parse_time_references('20 years before')
        assert len(result) == 1
        assert result[0].cardinality == 20
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'


class TestBeforeMarkerHours:
    """Test 'before' as past-tense marker with hour frame - numeric cardinalities 1-24"""

    def test_1_hour_before(self):
        result = parse_time_references('1 hour before')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_2_hours_before(self):
        result = parse_time_references('2 hours before')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_3_hours_before(self):
        result = parse_time_references('3 hours before')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_6_hours_before(self):
        result = parse_time_references('6 hours before')
        assert len(result) == 1
        assert result[0].cardinality == 6
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_12_hours_before(self):
        result = parse_time_references('12 hours before')
        assert len(result) == 1
        assert result[0].cardinality == 12
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_24_hours_before(self):
        result = parse_time_references('24 hours before')
        assert len(result) == 1
        assert result[0].cardinality == 24
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'


class TestBeforeMarkerMinutes:
    """Test 'before' as past-tense marker with minute frame - numeric cardinalities"""

    def test_1_minute_before(self):
        result = parse_time_references('1 minute before')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_5_minutes_before(self):
        result = parse_time_references('5 minutes before')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_15_minutes_before(self):
        result = parse_time_references('15 minutes before')
        assert len(result) == 1
        assert result[0].cardinality == 15
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_30_minutes_before(self):
        result = parse_time_references('30 minutes before')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_45_minutes_before(self):
        result = parse_time_references('45 minutes before')
        assert len(result) == 1
        assert result[0].cardinality == 45
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'


class TestBeforeMarkerSeconds:
    """Test 'before' as past-tense marker with second frame - numeric cardinalities"""

    def test_1_second_before(self):
        result = parse_time_references('1 second before')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_10_seconds_before(self):
        result = parse_time_references('10 seconds before')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_30_seconds_before(self):
        result = parse_time_references('30 seconds before')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_60_seconds_before(self):
        result = parse_time_references('60 seconds before')
        assert len(result) == 1
        assert result[0].cardinality == 60
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'


class TestBeforeMarkerWrittenNumbers:
    """Test 'before' with written-number cardinalities across all frames"""

    def test_one_day_before(self):
        result = parse_time_references('one day before')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_two_days_before(self):
        result = parse_time_references('two days before')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_three_days_before(self):
        result = parse_time_references('three days before')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_four_days_before(self):
        result = parse_time_references('four days before')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_five_days_before(self):
        result = parse_time_references('five days before')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_two_weeks_before(self):
        result = parse_time_references('two weeks before')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_three_weeks_before(self):
        result = parse_time_references('three weeks before')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_four_weeks_before(self):
        result = parse_time_references('four weeks before')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_two_months_before(self):
        result = parse_time_references('two months before')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_three_months_before(self):
        result = parse_time_references('three months before')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_six_months_before(self):
        result = parse_time_references('six months before')
        assert len(result) == 1
        assert result[0].cardinality == 6
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_two_years_before(self):
        result = parse_time_references('two years before')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_five_years_before(self):
        result = parse_time_references('five years before')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_two_hours_before(self):
        result = parse_time_references('two hours before')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_three_hours_before(self):
        result = parse_time_references('three hours before')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'


class TestBeforeMarkerSentenceEmbedding:
    """Test 'before' marker embedded in sentences"""

    def test_data_from_4_days_before(self):
        result = parse_time_references('data from 4 days before')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_events_2_months_before(self):
        result = parse_time_references('events 2 months before')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_starting_3_weeks_before(self):
        result = parse_time_references('starting 3 weeks before')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_updated_5_hours_before(self):
        result = parse_time_references('updated 5 hours before')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_posted_10_minutes_before(self):
        result = parse_time_references('posted 10 minutes before')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'


class TestSingularFrameWeek:
    """Test singular 'week' (not 'weeks') with numeric cardinalities 1-20"""

    def test_1_week_ago(self):
        result = parse_time_references('1 week ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_2_week_ago(self):
        result = parse_time_references('2 week ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_3_week_ago(self):
        result = parse_time_references('3 week ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_4_week_ago(self):
        result = parse_time_references('4 week ago')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_5_week_ago(self):
        result = parse_time_references('5 week ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_10_week_ago(self):
        result = parse_time_references('10 week ago')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_15_week_ago(self):
        result = parse_time_references('15 week ago')
        assert len(result) == 1
        assert result[0].cardinality == 15
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_20_week_ago(self):
        result = parse_time_references('20 week ago')
        assert len(result) == 1
        assert result[0].cardinality == 20
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'


class TestSingularFrameMonth:
    """Test singular 'month' (not 'months') with numeric cardinalities 1-20"""

    def test_1_month_ago(self):
        result = parse_time_references('1 month ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_2_month_ago(self):
        result = parse_time_references('2 month ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_3_month_ago(self):
        result = parse_time_references('3 month ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_6_month_ago(self):
        result = parse_time_references('6 month ago')
        assert len(result) == 1
        assert result[0].cardinality == 6
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_12_month_ago(self):
        result = parse_time_references('12 month ago')
        assert len(result) == 1
        assert result[0].cardinality == 12
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_18_month_ago(self):
        result = parse_time_references('18 month ago')
        assert len(result) == 1
        assert result[0].cardinality == 18
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_20_month_ago(self):
        result = parse_time_references('20 month ago')
        assert len(result) == 1
        assert result[0].cardinality == 20
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'


class TestSingularFrameYear:
    """Test singular 'year' (not 'years') with numeric cardinalities 1-20"""

    def test_1_year_ago(self):
        result = parse_time_references('1 year ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_2_year_ago(self):
        result = parse_time_references('2 year ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_3_year_ago(self):
        result = parse_time_references('3 year ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_5_year_ago(self):
        result = parse_time_references('5 year ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_10_year_ago(self):
        result = parse_time_references('10 year ago')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_15_year_ago(self):
        result = parse_time_references('15 year ago')
        assert len(result) == 1
        assert result[0].cardinality == 15
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_20_year_ago(self):
        result = parse_time_references('20 year ago')
        assert len(result) == 1
        assert result[0].cardinality == 20
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'


class TestSingularFrameHour:
    """Test singular 'hour' (not 'hours') with numeric cardinalities 1-24"""

    def test_1_hour_ago(self):
        result = parse_time_references('1 hour ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_2_hour_ago(self):
        result = parse_time_references('2 hour ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_3_hour_ago(self):
        result = parse_time_references('3 hour ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_6_hour_ago(self):
        result = parse_time_references('6 hour ago')
        assert len(result) == 1
        assert result[0].cardinality == 6
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_12_hour_ago(self):
        result = parse_time_references('12 hour ago')
        assert len(result) == 1
        assert result[0].cardinality == 12
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_24_hour_ago(self):
        result = parse_time_references('24 hour ago')
        assert len(result) == 1
        assert result[0].cardinality == 24
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'


class TestSingularFrameMinute:
    """Test singular 'minute' (not 'minutes') with numeric cardinalities"""

    def test_1_minute_ago(self):
        result = parse_time_references('1 minute ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_2_minute_ago(self):
        result = parse_time_references('2 minute ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_5_minute_ago(self):
        result = parse_time_references('5 minute ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_10_minute_ago(self):
        result = parse_time_references('10 minute ago')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_15_minute_ago(self):
        result = parse_time_references('15 minute ago')
        assert len(result) == 1
        assert result[0].cardinality == 15
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_30_minute_ago(self):
        result = parse_time_references('30 minute ago')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'


class TestSingularFrameSecond:
    """Test singular 'second' (not 'seconds') with numeric cardinalities"""

    def test_1_second_ago(self):
        result = parse_time_references('1 second ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_2_second_ago(self):
        result = parse_time_references('2 second ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_10_second_ago(self):
        result = parse_time_references('10 second ago')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_30_second_ago(self):
        result = parse_time_references('30 second ago')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_60_second_ago(self):
        result = parse_time_references('60 second ago')
        assert len(result) == 1
        assert result[0].cardinality == 60
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'


class TestSingularFrameWrittenNumbers:
    """Test singular frames with written-number cardinalities"""

    def test_two_week_ago(self):
        result = parse_time_references('two week ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_three_week_ago(self):
        result = parse_time_references('three week ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_four_week_ago(self):
        result = parse_time_references('four week ago')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_five_week_ago(self):
        result = parse_time_references('five week ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_ten_week_ago(self):
        result = parse_time_references('ten week ago')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_two_month_ago(self):
        result = parse_time_references('two month ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_three_month_ago(self):
        result = parse_time_references('three month ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_six_month_ago(self):
        result = parse_time_references('six month ago')
        assert len(result) == 1
        assert result[0].cardinality == 6
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_twelve_month_ago(self):
        result = parse_time_references('twelve month ago')
        assert len(result) == 1
        assert result[0].cardinality == 12
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_two_year_ago(self):
        result = parse_time_references('two year ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_five_year_ago(self):
        result = parse_time_references('five year ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_ten_year_ago(self):
        result = parse_time_references('ten year ago')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_two_hour_ago(self):
        result = parse_time_references('two hour ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_six_hour_ago(self):
        result = parse_time_references('six hour ago')
        assert len(result) == 1
        assert result[0].cardinality == 6
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_ten_minute_ago(self):
        result = parse_time_references('ten minute ago')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_thirty_second_ago(self):
        result = parse_time_references('thirty second ago')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'


class TestSingularFrameWithBefore:
    """Test singular frames combined with 'before' marker"""

    def test_2_week_before(self):
        result = parse_time_references('2 week before')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_4_week_before(self):
        result = parse_time_references('4 week before')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_3_month_before(self):
        result = parse_time_references('3 month before')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_6_month_before(self):
        result = parse_time_references('6 month before')
        assert len(result) == 1
        assert result[0].cardinality == 6
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_2_year_before(self):
        result = parse_time_references('2 year before')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_5_year_before(self):
        result = parse_time_references('5 year before')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_2_hour_before(self):
        result = parse_time_references('2 hour before')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_10_minute_before(self):
        result = parse_time_references('10 minute before')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_30_second_before(self):
        result = parse_time_references('30 second before')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'


class TestNegativeCases:
    """Test cases that should NOT match - no cardinality or invalid patterns"""

    def test_before_alone(self):
        """'before' without cardinality should not match"""
        result = parse_time_references('before')
        assert len(result) == 0

    def test_days_before_no_cardinality(self):
        """'days before' without cardinality should not match"""
        result = parse_time_references('days before')
        assert len(result) == 0

    def test_week_ago_no_cardinality(self):
        """'week ago' without cardinality should not match"""
        result = parse_time_references('week ago')
        assert len(result) == 0

    def test_month_alone(self):
        """'month' without context should not match"""
        result = parse_time_references('month')
        assert len(result) == 0

    def test_year_alone(self):
        """'year' without context should not match"""
        result = parse_time_references('year')
        assert len(result) == 0

    def test_hour_alone(self):
        """'hour' without context should not match"""
        result = parse_time_references('hour')
        assert len(result) == 0


class TestCaseInsensitivity:
    """Test that 'before' and frames are case-insensitive"""

    def test_4_days_BEFORE(self):
        result = parse_time_references('4 days BEFORE')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_3_WEEKS_before(self):
        result = parse_time_references('3 WEEKS before')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_2_MONTH_AGO(self):
        result = parse_time_references('2 MONTH AGO')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'


class TestBeforeMarkerDaysExtended:
    """Extended day tests for 'before' - filling numeric gaps 8-9, 11-14, 16-19, 21-29"""

    def test_8_days_before(self):
        result = parse_time_references('8 days before')
        assert len(result) == 1
        assert result[0].cardinality == 8
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_9_days_before(self):
        result = parse_time_references('9 days before')
        assert len(result) == 1
        assert result[0].cardinality == 9
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_11_days_before(self):
        result = parse_time_references('11 days before')
        assert len(result) == 1
        assert result[0].cardinality == 11
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_12_days_before(self):
        result = parse_time_references('12 days before')
        assert len(result) == 1
        assert result[0].cardinality == 12
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_13_days_before(self):
        result = parse_time_references('13 days before')
        assert len(result) == 1
        assert result[0].cardinality == 13
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_14_days_before(self):
        result = parse_time_references('14 days before')
        assert len(result) == 1
        assert result[0].cardinality == 14
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_16_days_before(self):
        result = parse_time_references('16 days before')
        assert len(result) == 1
        assert result[0].cardinality == 16
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_17_days_before(self):
        result = parse_time_references('17 days before')
        assert len(result) == 1
        assert result[0].cardinality == 17
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_18_days_before(self):
        result = parse_time_references('18 days before')
        assert len(result) == 1
        assert result[0].cardinality == 18
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_19_days_before(self):
        result = parse_time_references('19 days before')
        assert len(result) == 1
        assert result[0].cardinality == 19
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_21_days_before(self):
        result = parse_time_references('21 days before')
        assert len(result) == 1
        assert result[0].cardinality == 21
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_22_days_before(self):
        result = parse_time_references('22 days before')
        assert len(result) == 1
        assert result[0].cardinality == 22
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_23_days_before(self):
        result = parse_time_references('23 days before')
        assert len(result) == 1
        assert result[0].cardinality == 23
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_24_days_before(self):
        result = parse_time_references('24 days before')
        assert len(result) == 1
        assert result[0].cardinality == 24
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_25_days_before(self):
        result = parse_time_references('25 days before')
        assert len(result) == 1
        assert result[0].cardinality == 25
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_26_days_before(self):
        result = parse_time_references('26 days before')
        assert len(result) == 1
        assert result[0].cardinality == 26
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_27_days_before(self):
        result = parse_time_references('27 days before')
        assert len(result) == 1
        assert result[0].cardinality == 27
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_28_days_before(self):
        result = parse_time_references('28 days before')
        assert len(result) == 1
        assert result[0].cardinality == 28
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_29_days_before(self):
        result = parse_time_references('29 days before')
        assert len(result) == 1
        assert result[0].cardinality == 29
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'


class TestBeforeMarkerWeeksExtended:
    """Extended week tests for 'before' - filling numeric gaps 6-9, 11-14, 16-19"""

    def test_6_weeks_before(self):
        result = parse_time_references('6 weeks before')
        assert len(result) == 1
        assert result[0].cardinality == 6
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_7_weeks_before(self):
        result = parse_time_references('7 weeks before')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_8_weeks_before(self):
        result = parse_time_references('8 weeks before')
        assert len(result) == 1
        assert result[0].cardinality == 8
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_9_weeks_before(self):
        result = parse_time_references('9 weeks before')
        assert len(result) == 1
        assert result[0].cardinality == 9
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_11_weeks_before(self):
        result = parse_time_references('11 weeks before')
        assert len(result) == 1
        assert result[0].cardinality == 11
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_12_weeks_before(self):
        result = parse_time_references('12 weeks before')
        assert len(result) == 1
        assert result[0].cardinality == 12
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_13_weeks_before(self):
        result = parse_time_references('13 weeks before')
        assert len(result) == 1
        assert result[0].cardinality == 13
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_14_weeks_before(self):
        result = parse_time_references('14 weeks before')
        assert len(result) == 1
        assert result[0].cardinality == 14
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_16_weeks_before(self):
        result = parse_time_references('16 weeks before')
        assert len(result) == 1
        assert result[0].cardinality == 16
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_17_weeks_before(self):
        result = parse_time_references('17 weeks before')
        assert len(result) == 1
        assert result[0].cardinality == 17
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_18_weeks_before(self):
        result = parse_time_references('18 weeks before')
        assert len(result) == 1
        assert result[0].cardinality == 18
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_19_weeks_before(self):
        result = parse_time_references('19 weeks before')
        assert len(result) == 1
        assert result[0].cardinality == 19
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'


class TestBeforeMarkerMonthsExtended:
    """Extended month tests for 'before' - filling numeric gaps 4-5, 7-11, 13-17, 19-23"""

    def test_4_months_before(self):
        result = parse_time_references('4 months before')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_5_months_before(self):
        result = parse_time_references('5 months before')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_7_months_before(self):
        result = parse_time_references('7 months before')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_8_months_before(self):
        result = parse_time_references('8 months before')
        assert len(result) == 1
        assert result[0].cardinality == 8
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_9_months_before(self):
        result = parse_time_references('9 months before')
        assert len(result) == 1
        assert result[0].cardinality == 9
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_10_months_before(self):
        result = parse_time_references('10 months before')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_11_months_before(self):
        result = parse_time_references('11 months before')
        assert len(result) == 1
        assert result[0].cardinality == 11
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_13_months_before(self):
        result = parse_time_references('13 months before')
        assert len(result) == 1
        assert result[0].cardinality == 13
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_14_months_before(self):
        result = parse_time_references('14 months before')
        assert len(result) == 1
        assert result[0].cardinality == 14
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_15_months_before(self):
        result = parse_time_references('15 months before')
        assert len(result) == 1
        assert result[0].cardinality == 15
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'


class TestBeforeMarkerYearsExtended:
    """Extended year tests for 'before' - filling numeric gaps 4, 6-9, 11-19"""

    def test_4_years_before(self):
        result = parse_time_references('4 years before')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_6_years_before(self):
        result = parse_time_references('6 years before')
        assert len(result) == 1
        assert result[0].cardinality == 6
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_7_years_before(self):
        result = parse_time_references('7 years before')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_8_years_before(self):
        result = parse_time_references('8 years before')
        assert len(result) == 1
        assert result[0].cardinality == 8
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_9_years_before(self):
        result = parse_time_references('9 years before')
        assert len(result) == 1
        assert result[0].cardinality == 9
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_11_years_before(self):
        result = parse_time_references('11 years before')
        assert len(result) == 1
        assert result[0].cardinality == 11
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_12_years_before(self):
        result = parse_time_references('12 years before')
        assert len(result) == 1
        assert result[0].cardinality == 12
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_15_years_before(self):
        result = parse_time_references('15 years before')
        assert len(result) == 1
        assert result[0].cardinality == 15
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'


class TestBeforeMarkerWrittenNumbersExtended:
    """Extended written-number tests for 'before' - six through twenty"""

    def test_six_days_before(self):
        result = parse_time_references('six days before')
        assert len(result) == 1
        assert result[0].cardinality == 6
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_seven_days_before(self):
        result = parse_time_references('seven days before')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_eight_days_before(self):
        result = parse_time_references('eight days before')
        assert len(result) == 1
        assert result[0].cardinality == 8
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_nine_days_before(self):
        result = parse_time_references('nine days before')
        assert len(result) == 1
        assert result[0].cardinality == 9
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_ten_days_before(self):
        result = parse_time_references('ten days before')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_eleven_days_before(self):
        result = parse_time_references('eleven days before')
        assert len(result) == 1
        assert result[0].cardinality == 11
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_twelve_days_before(self):
        result = parse_time_references('twelve days before')
        assert len(result) == 1
        assert result[0].cardinality == 12
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_fifteen_days_before(self):
        result = parse_time_references('fifteen days before')
        assert len(result) == 1
        assert result[0].cardinality == 15
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_twenty_days_before(self):
        result = parse_time_references('twenty days before')
        assert len(result) == 1
        assert result[0].cardinality == 20
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_five_weeks_before(self):
        result = parse_time_references('five weeks before')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_seven_weeks_before(self):
        result = parse_time_references('seven weeks before')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_ten_weeks_before(self):
        result = parse_time_references('ten weeks before')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'


class TestSingularFrameDay:
    """Test singular 'day' (not 'days') with numeric cardinalities - comprehensive"""

    def test_2_day_ago(self):
        result = parse_time_references('2 day ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_3_day_ago(self):
        result = parse_time_references('3 day ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_5_day_ago(self):
        result = parse_time_references('5 day ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_7_day_ago(self):
        result = parse_time_references('7 day ago')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_10_day_ago(self):
        result = parse_time_references('10 day ago')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_14_day_ago(self):
        result = parse_time_references('14 day ago')
        assert len(result) == 1
        assert result[0].cardinality == 14
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_21_day_ago(self):
        result = parse_time_references('21 day ago')
        assert len(result) == 1
        assert result[0].cardinality == 21
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_30_day_ago(self):
        result = parse_time_references('30 day ago')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'


class TestSingularFrameWeekExtended:
    """Extended singular week tests - filling numeric gaps 6-9, 11-14, 16-19"""

    def test_6_week_ago(self):
        result = parse_time_references('6 week ago')
        assert len(result) == 1
        assert result[0].cardinality == 6
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_7_week_ago(self):
        result = parse_time_references('7 week ago')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_8_week_ago(self):
        result = parse_time_references('8 week ago')
        assert len(result) == 1
        assert result[0].cardinality == 8
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_9_week_ago(self):
        result = parse_time_references('9 week ago')
        assert len(result) == 1
        assert result[0].cardinality == 9
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_11_week_ago(self):
        result = parse_time_references('11 week ago')
        assert len(result) == 1
        assert result[0].cardinality == 11
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_12_week_ago(self):
        result = parse_time_references('12 week ago')
        assert len(result) == 1
        assert result[0].cardinality == 12
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_13_week_ago(self):
        result = parse_time_references('13 week ago')
        assert len(result) == 1
        assert result[0].cardinality == 13
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_14_week_ago(self):
        result = parse_time_references('14 week ago')
        assert len(result) == 1
        assert result[0].cardinality == 14
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'


class TestSingularFrameMonthExtended:
    """Extended singular month tests - filling numeric gaps 4-5, 7-11, 13-17, 19"""

    def test_4_month_ago(self):
        result = parse_time_references('4 month ago')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_5_month_ago(self):
        result = parse_time_references('5 month ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_7_month_ago(self):
        result = parse_time_references('7 month ago')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_8_month_ago(self):
        result = parse_time_references('8 month ago')
        assert len(result) == 1
        assert result[0].cardinality == 8
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_9_month_ago(self):
        result = parse_time_references('9 month ago')
        assert len(result) == 1
        assert result[0].cardinality == 9
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_10_month_ago(self):
        result = parse_time_references('10 month ago')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_11_month_ago(self):
        result = parse_time_references('11 month ago')
        assert len(result) == 1
        assert result[0].cardinality == 11
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'


class TestSingularFrameYearExtended:
    """Extended singular year tests - filling numeric gaps 4, 6-9, 11-14, 16-19"""

    def test_4_year_ago(self):
        result = parse_time_references('4 year ago')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_6_year_ago(self):
        result = parse_time_references('6 year ago')
        assert len(result) == 1
        assert result[0].cardinality == 6
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_7_year_ago(self):
        result = parse_time_references('7 year ago')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_8_year_ago(self):
        result = parse_time_references('8 year ago')
        assert len(result) == 1
        assert result[0].cardinality == 8
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_9_year_ago(self):
        result = parse_time_references('9 year ago')
        assert len(result) == 1
        assert result[0].cardinality == 9
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_11_year_ago(self):
        result = parse_time_references('11 year ago')
        assert len(result) == 1
        assert result[0].cardinality == 11
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'


class TestSingularFrameHourExtended:
    """Extended singular hour tests - filling numeric gaps 4-5, 7-11, 13-23"""

    def test_4_hour_ago(self):
        result = parse_time_references('4 hour ago')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_5_hour_ago(self):
        result = parse_time_references('5 hour ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_8_hour_ago(self):
        result = parse_time_references('8 hour ago')
        assert len(result) == 1
        assert result[0].cardinality == 8
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_10_hour_ago(self):
        result = parse_time_references('10 hour ago')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_18_hour_ago(self):
        result = parse_time_references('18 hour ago')
        assert len(result) == 1
        assert result[0].cardinality == 18
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'


class TestSingularFrameMinuteExtended:
    """Extended singular minute tests - additional cardinalities"""

    def test_3_minute_ago(self):
        result = parse_time_references('3 minute ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_20_minute_ago(self):
        result = parse_time_references('20 minute ago')
        assert len(result) == 1
        assert result[0].cardinality == 20
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_45_minute_ago(self):
        result = parse_time_references('45 minute ago')
        assert len(result) == 1
        assert result[0].cardinality == 45
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_60_minute_ago(self):
        result = parse_time_references('60 minute ago')
        assert len(result) == 1
        assert result[0].cardinality == 60
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'


class TestSingularFrameSecondExtended:
    """Extended singular second tests - additional cardinalities"""

    def test_5_second_ago(self):
        result = parse_time_references('5 second ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_15_second_ago(self):
        result = parse_time_references('15 second ago')
        assert len(result) == 1
        assert result[0].cardinality == 15
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_45_second_ago(self):
        result = parse_time_references('45 second ago')
        assert len(result) == 1
        assert result[0].cardinality == 45
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'


class TestSingularFrameWrittenNumbersExtended:
    """Extended written-number tests for singular frames - seven through twenty"""

    def test_seven_week_ago(self):
        result = parse_time_references('seven week ago')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_eight_week_ago(self):
        result = parse_time_references('eight week ago')
        assert len(result) == 1
        assert result[0].cardinality == 8
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_nine_week_ago(self):
        result = parse_time_references('nine week ago')
        assert len(result) == 1
        assert result[0].cardinality == 9
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_four_month_ago(self):
        result = parse_time_references('four month ago')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_five_month_ago(self):
        result = parse_time_references('five month ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_seven_month_ago(self):
        result = parse_time_references('seven month ago')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_eight_month_ago(self):
        result = parse_time_references('eight month ago')
        assert len(result) == 1
        assert result[0].cardinality == 8
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_three_year_ago(self):
        result = parse_time_references('three year ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_four_year_ago(self):
        result = parse_time_references('four year ago')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_seven_year_ago(self):
        result = parse_time_references('seven year ago')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'


class TestSingularFrameWithBeforeExtended:
    """Extended singular frame with 'before' - additional combinations"""

    def test_3_week_before(self):
        result = parse_time_references('3 week before')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_5_week_before(self):
        result = parse_time_references('5 week before')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_1_month_before(self):
        result = parse_time_references('1 month before')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_4_month_before(self):
        result = parse_time_references('4 month before')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_1_year_before(self):
        result = parse_time_references('1 year before')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_3_year_before(self):
        result = parse_time_references('3 year before')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_1_hour_before(self):
        result = parse_time_references('1 hour before')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_5_minute_before(self):
        result = parse_time_references('5 minute before')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_15_second_before(self):
        result = parse_time_references('15 second before')
        assert len(result) == 1
        assert result[0].cardinality == 15
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'


class TestSentenceEmbeddingExtended:
    """Extended sentence embedding tests - more realistic contexts"""

    def test_metrics_from_5_weeks_before(self):
        result = parse_time_references('metrics from 5 weeks before')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_records_3_year_before(self):
        result = parse_time_references('records 3 year before')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_snapshot_10_hour_before(self):
        result = parse_time_references('snapshot 10 hour before')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_backup_7_day_before(self):
        result = parse_time_references('backup 7 day before')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_logs_from_2_hour_ago(self):
        result = parse_time_references('logs from 2 hour ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_data_5_minute_ago(self):
        result = parse_time_references('data 5 minute ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'
