#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Tests for large cardinality support across all units and suffix patterns.

Related GitHub Issue:
    #14 - Gap: large cardinalities not recognized (34 hours ago, numbers above ~31)
    https://github.com/craigtrim/fast-parse-time/issues/14

Current KB limits (before fix):
    second: 1-60    minute: 1-60    hour: 1-24
    day: 1-365      week: 1-52      month: 1-24    year: 1-100

Target KB limits (after fix):
    All units: 1-1000

Suffix patterns covered:
    ago, before now, prior, back

All tests in this file are EXPECTED TO FAIL until the KB is extended.
"""

import pytest
from fast_parse_time import parse_time_references, has_temporal_info


# ============================================================================
# Group 1: hours -- gap range 25-168 (above current max of 24)
# ============================================================================

class TestHoursAgoLargeCardinality:
    """'ago' suffix for hours above current max of 24."""

    def test_25_hours_ago(self):
        result = parse_time_references('25 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 25
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_34_hours_ago(self):
        """Explicit parsedatetime regression case."""
        result = parse_time_references('34 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 34
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_48_hours_ago(self):
        """2 days expressed in hours — very common."""
        result = parse_time_references('48 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 48
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_72_hours_ago(self):
        """3 days expressed in hours — very common."""
        result = parse_time_references('72 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 72
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_96_hours_ago(self):
        result = parse_time_references('96 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 96
        assert result[0].frame == 'hour'

    def test_100_hours_ago(self):
        result = parse_time_references('100 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 100
        assert result[0].frame == 'hour'

    def test_120_hours_ago(self):
        result = parse_time_references('120 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 120
        assert result[0].frame == 'hour'

    def test_168_hours_ago(self):
        """1 week expressed in hours."""
        result = parse_time_references('168 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 168
        assert result[0].frame == 'hour'

    def test_200_hours_ago(self):
        result = parse_time_references('200 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 200
        assert result[0].frame == 'hour'

    def test_500_hours_ago(self):
        result = parse_time_references('500 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 500
        assert result[0].frame == 'hour'

    def test_720_hours_ago(self):
        """1 month expressed in hours."""
        result = parse_time_references('720 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 720
        assert result[0].frame == 'hour'

    def test_1000_hours_ago(self):
        result = parse_time_references('1000 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'hour'


# ============================================================================
# Group 2: hours -- before now, prior, back (large cardinality)
# ============================================================================

class TestHoursBeforeNowLargeCardinality:
    """'before now' suffix for hours above current max of 24."""

    def test_25_hours_before_now(self):
        result = parse_time_references('25 hours before now')
        assert len(result) == 1
        assert result[0].cardinality == 25
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_48_hours_before_now(self):
        result = parse_time_references('48 hours before now')
        assert len(result) == 1
        assert result[0].cardinality == 48
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_72_hours_before_now(self):
        result = parse_time_references('72 hours before now')
        assert len(result) == 1
        assert result[0].cardinality == 72
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_500_hours_before_now(self):
        result = parse_time_references('500 hours before now')
        assert len(result) == 1
        assert result[0].cardinality == 500
        assert result[0].frame == 'hour'

    def test_1000_hours_before_now(self):
        result = parse_time_references('1000 hours before now')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'hour'


class TestHoursPriorLargeCardinality:
    """'prior' suffix for hours above current max of 24."""

    def test_25_hours_prior(self):
        result = parse_time_references('25 hours prior')
        assert len(result) == 1
        assert result[0].cardinality == 25
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_48_hours_prior(self):
        result = parse_time_references('48 hours prior')
        assert len(result) == 1
        assert result[0].cardinality == 48
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_1000_hours_prior(self):
        result = parse_time_references('1000 hours prior')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'hour'


class TestHoursBackLargeCardinality:
    """'back' suffix for hours above current max of 24."""

    def test_25_hours_back(self):
        result = parse_time_references('25 hours back')
        assert len(result) == 1
        assert result[0].cardinality == 25
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_48_hours_back(self):
        result = parse_time_references('48 hours back')
        assert len(result) == 1
        assert result[0].cardinality == 48
        assert result[0].frame == 'hour'

    def test_1000_hours_back(self):
        result = parse_time_references('1000 hours back')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'hour'


# ============================================================================
# Group 3: minutes -- gap range 61-1440 (above current max of 60)
# ============================================================================

class TestMinutesAgoLargeCardinality:
    """'ago' suffix for minutes above current max of 60."""

    def test_61_minutes_ago(self):
        result = parse_time_references('61 minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 61
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_90_minutes_ago(self):
        """Very common — 'an hour and a half ago'."""
        result = parse_time_references('90 minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 90
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_120_minutes_ago(self):
        """2 hours expressed in minutes."""
        result = parse_time_references('120 minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 120
        assert result[0].frame == 'minute'

    def test_180_minutes_ago(self):
        result = parse_time_references('180 minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 180
        assert result[0].frame == 'minute'

    def test_240_minutes_ago(self):
        result = parse_time_references('240 minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 240
        assert result[0].frame == 'minute'

    def test_500_minutes_ago(self):
        result = parse_time_references('500 minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 500
        assert result[0].frame == 'minute'

    def test_1000_minutes_ago(self):
        result = parse_time_references('1000 minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'minute'


class TestMinutesBeforeNowLargeCardinality:
    """'before now' for minutes above current max."""

    def test_90_minutes_before_now(self):
        result = parse_time_references('90 minutes before now')
        assert len(result) == 1
        assert result[0].cardinality == 90
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_120_minutes_before_now(self):
        result = parse_time_references('120 minutes before now')
        assert len(result) == 1
        assert result[0].cardinality == 120
        assert result[0].frame == 'minute'

    def test_1000_minutes_before_now(self):
        result = parse_time_references('1000 minutes before now')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'minute'


class TestMinutesPriorLargeCardinality:
    def test_90_minutes_prior(self):
        result = parse_time_references('90 minutes prior')
        assert len(result) == 1
        assert result[0].cardinality == 90
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_1000_minutes_prior(self):
        result = parse_time_references('1000 minutes prior')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'minute'


class TestMinutesBackLargeCardinality:
    def test_90_minutes_back(self):
        result = parse_time_references('90 minutes back')
        assert len(result) == 1
        assert result[0].cardinality == 90
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_1000_minutes_back(self):
        result = parse_time_references('1000 minutes back')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'minute'


# ============================================================================
# Group 4: seconds -- gap range 61-3600 (above current max of 60)
# ============================================================================

class TestSecondsAgoLargeCardinality:
    """'ago' suffix for seconds above current max of 60."""

    def test_61_seconds_ago(self):
        result = parse_time_references('61 seconds ago')
        assert len(result) == 1
        assert result[0].cardinality == 61
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_90_seconds_ago(self):
        result = parse_time_references('90 seconds ago')
        assert len(result) == 1
        assert result[0].cardinality == 90
        assert result[0].frame == 'second'

    def test_120_seconds_ago(self):
        result = parse_time_references('120 seconds ago')
        assert len(result) == 1
        assert result[0].cardinality == 120
        assert result[0].frame == 'second'

    def test_500_seconds_ago(self):
        result = parse_time_references('500 seconds ago')
        assert len(result) == 1
        assert result[0].cardinality == 500
        assert result[0].frame == 'second'

    def test_1000_seconds_ago(self):
        result = parse_time_references('1000 seconds ago')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'second'


class TestSecondsBeforeNowLargeCardinality:
    def test_90_seconds_before_now(self):
        result = parse_time_references('90 seconds before now')
        assert len(result) == 1
        assert result[0].cardinality == 90
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_1000_seconds_before_now(self):
        result = parse_time_references('1000 seconds before now')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'second'


class TestSecondsPriorLargeCardinality:
    def test_90_seconds_prior(self):
        result = parse_time_references('90 seconds prior')
        assert len(result) == 1
        assert result[0].cardinality == 90
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_1000_seconds_prior(self):
        result = parse_time_references('1000 seconds prior')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'second'


class TestSecondsBackLargeCardinality:
    def test_90_seconds_back(self):
        result = parse_time_references('90 seconds back')
        assert len(result) == 1
        assert result[0].cardinality == 90
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_1000_seconds_back(self):
        result = parse_time_references('1000 seconds back')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'second'


# ============================================================================
# Group 5: weeks -- gap range 53-1000 (above current max of 52)
# ============================================================================

class TestWeeksAgoLargeCardinality:
    """'ago' suffix for weeks above current max of 52."""

    def test_53_weeks_ago(self):
        result = parse_time_references('53 weeks ago')
        assert len(result) == 1
        assert result[0].cardinality == 53
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_60_weeks_ago(self):
        result = parse_time_references('60 weeks ago')
        assert len(result) == 1
        assert result[0].cardinality == 60
        assert result[0].frame == 'week'

    def test_104_weeks_ago(self):
        """2 years expressed in weeks."""
        result = parse_time_references('104 weeks ago')
        assert len(result) == 1
        assert result[0].cardinality == 104
        assert result[0].frame == 'week'

    def test_200_weeks_ago(self):
        result = parse_time_references('200 weeks ago')
        assert len(result) == 1
        assert result[0].cardinality == 200
        assert result[0].frame == 'week'

    def test_500_weeks_ago(self):
        result = parse_time_references('500 weeks ago')
        assert len(result) == 1
        assert result[0].cardinality == 500
        assert result[0].frame == 'week'

    def test_1000_weeks_ago(self):
        result = parse_time_references('1000 weeks ago')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'week'


class TestWeeksBeforeNowLargeCardinality:
    def test_53_weeks_before_now(self):
        result = parse_time_references('53 weeks before now')
        assert len(result) == 1
        assert result[0].cardinality == 53
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_104_weeks_before_now(self):
        result = parse_time_references('104 weeks before now')
        assert len(result) == 1
        assert result[0].cardinality == 104
        assert result[0].frame == 'week'

    def test_1000_weeks_before_now(self):
        result = parse_time_references('1000 weeks before now')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'week'


class TestWeeksPriorLargeCardinality:
    def test_53_weeks_prior(self):
        result = parse_time_references('53 weeks prior')
        assert len(result) == 1
        assert result[0].cardinality == 53
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_1000_weeks_prior(self):
        result = parse_time_references('1000 weeks prior')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'week'


class TestWeeksBackLargeCardinality:
    def test_53_weeks_back(self):
        result = parse_time_references('53 weeks back')
        assert len(result) == 1
        assert result[0].cardinality == 53
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_1000_weeks_back(self):
        result = parse_time_references('1000 weeks back')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'week'


# ============================================================================
# Group 6: months -- gap range 25-1000 (above current max of 24)
# ============================================================================

class TestMonthsAgoLargeCardinality:
    """'ago' suffix for months above current max of 24."""

    def test_25_months_ago(self):
        result = parse_time_references('25 months ago')
        assert len(result) == 1
        assert result[0].cardinality == 25
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_36_months_ago(self):
        """3 years expressed in months — very common."""
        result = parse_time_references('36 months ago')
        assert len(result) == 1
        assert result[0].cardinality == 36
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_48_months_ago(self):
        """4 years in months."""
        result = parse_time_references('48 months ago')
        assert len(result) == 1
        assert result[0].cardinality == 48
        assert result[0].frame == 'month'

    def test_60_months_ago(self):
        """5 years in months."""
        result = parse_time_references('60 months ago')
        assert len(result) == 1
        assert result[0].cardinality == 60
        assert result[0].frame == 'month'

    def test_120_months_ago(self):
        """10 years in months."""
        result = parse_time_references('120 months ago')
        assert len(result) == 1
        assert result[0].cardinality == 120
        assert result[0].frame == 'month'

    def test_200_months_ago(self):
        result = parse_time_references('200 months ago')
        assert len(result) == 1
        assert result[0].cardinality == 200
        assert result[0].frame == 'month'

    def test_500_months_ago(self):
        result = parse_time_references('500 months ago')
        assert len(result) == 1
        assert result[0].cardinality == 500
        assert result[0].frame == 'month'

    def test_1000_months_ago(self):
        result = parse_time_references('1000 months ago')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'month'


class TestMonthsBeforeNowLargeCardinality:
    def test_36_months_before_now(self):
        result = parse_time_references('36 months before now')
        assert len(result) == 1
        assert result[0].cardinality == 36
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_120_months_before_now(self):
        result = parse_time_references('120 months before now')
        assert len(result) == 1
        assert result[0].cardinality == 120
        assert result[0].frame == 'month'

    def test_1000_months_before_now(self):
        result = parse_time_references('1000 months before now')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'month'


class TestMonthsPriorLargeCardinality:
    def test_36_months_prior(self):
        result = parse_time_references('36 months prior')
        assert len(result) == 1
        assert result[0].cardinality == 36
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_1000_months_prior(self):
        result = parse_time_references('1000 months prior')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'month'


class TestMonthsBackLargeCardinality:
    def test_36_months_back(self):
        result = parse_time_references('36 months back')
        assert len(result) == 1
        assert result[0].cardinality == 36
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_1000_months_back(self):
        result = parse_time_references('1000 months back')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'month'


# ============================================================================
# Group 7: days -- gap range 366-1000 (above current max of 365)
# ============================================================================

class TestDaysAgoLargeCardinality:
    """'ago' suffix for days above current max of 365."""

    def test_366_days_ago(self):
        result = parse_time_references('366 days ago')
        assert len(result) == 1
        assert result[0].cardinality == 366
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_400_days_ago(self):
        result = parse_time_references('400 days ago')
        assert len(result) == 1
        assert result[0].cardinality == 400
        assert result[0].frame == 'day'

    def test_500_days_ago(self):
        result = parse_time_references('500 days ago')
        assert len(result) == 1
        assert result[0].cardinality == 500
        assert result[0].frame == 'day'

    def test_730_days_ago(self):
        """2 years in days."""
        result = parse_time_references('730 days ago')
        assert len(result) == 1
        assert result[0].cardinality == 730
        assert result[0].frame == 'day'

    def test_1000_days_ago(self):
        result = parse_time_references('1000 days ago')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'day'


class TestDaysBeforeNowLargeCardinality:
    def test_366_days_before_now(self):
        result = parse_time_references('366 days before now')
        assert len(result) == 1
        assert result[0].cardinality == 366
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_1000_days_before_now(self):
        result = parse_time_references('1000 days before now')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'day'


class TestDaysPriorLargeCardinality:
    def test_366_days_prior(self):
        result = parse_time_references('366 days prior')
        assert len(result) == 1
        assert result[0].cardinality == 366
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_1000_days_prior(self):
        result = parse_time_references('1000 days prior')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'day'


class TestDaysBackLargeCardinality:
    def test_366_days_back(self):
        result = parse_time_references('366 days back')
        assert len(result) == 1
        assert result[0].cardinality == 366
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_1000_days_back(self):
        result = parse_time_references('1000 days back')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'day'


# ============================================================================
# Group 8: years -- gap range 101-1000 (above current max of 100)
# ============================================================================

class TestYearsAgoLargeCardinality:
    """'ago' suffix for years above current max of 100."""

    def test_101_years_ago(self):
        result = parse_time_references('101 years ago')
        assert len(result) == 1
        assert result[0].cardinality == 101
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_150_years_ago(self):
        result = parse_time_references('150 years ago')
        assert len(result) == 1
        assert result[0].cardinality == 150
        assert result[0].frame == 'year'

    def test_200_years_ago(self):
        result = parse_time_references('200 years ago')
        assert len(result) == 1
        assert result[0].cardinality == 200
        assert result[0].frame == 'year'

    def test_500_years_ago(self):
        result = parse_time_references('500 years ago')
        assert len(result) == 1
        assert result[0].cardinality == 500
        assert result[0].frame == 'year'

    def test_1000_years_ago(self):
        result = parse_time_references('1000 years ago')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'year'


class TestYearsBeforeNowLargeCardinality:
    def test_101_years_before_now(self):
        result = parse_time_references('101 years before now')
        assert len(result) == 1
        assert result[0].cardinality == 101
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_500_years_before_now(self):
        result = parse_time_references('500 years before now')
        assert len(result) == 1
        assert result[0].cardinality == 500
        assert result[0].frame == 'year'

    def test_1000_years_before_now(self):
        result = parse_time_references('1000 years before now')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'year'


class TestYearsPriorLargeCardinality:
    def test_101_years_prior(self):
        result = parse_time_references('101 years prior')
        assert len(result) == 1
        assert result[0].cardinality == 101
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_1000_years_prior(self):
        result = parse_time_references('1000 years prior')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'year'


class TestYearsBackLargeCardinality:
    def test_101_years_back(self):
        result = parse_time_references('101 years back')
        assert len(result) == 1
        assert result[0].cardinality == 101
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_1000_years_back(self):
        result = parse_time_references('1000 years back')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'year'


# ============================================================================
# Group 9: Future tense -- from now (large cardinalities)
# ============================================================================

class TestHoursFromNowLargeCardinality:
    """Future expressions with large cardinalities."""

    def test_25_hours_from_now(self):
        result = parse_time_references('25 hours from now')
        assert len(result) == 1
        assert result[0].cardinality == 25
        assert result[0].frame == 'hour'
        assert result[0].tense == 'future'

    def test_48_hours_from_now(self):
        result = parse_time_references('48 hours from now')
        assert len(result) == 1
        assert result[0].cardinality == 48
        assert result[0].frame == 'hour'
        assert result[0].tense == 'future'

    def test_72_hours_from_now(self):
        result = parse_time_references('72 hours from now')
        assert len(result) == 1
        assert result[0].cardinality == 72
        assert result[0].frame == 'hour'
        assert result[0].tense == 'future'

    def test_1000_hours_from_now(self):
        result = parse_time_references('1000 hours from now')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'hour'
        assert result[0].tense == 'future'


class TestMinutesFromNowLargeCardinality:
    def test_90_minutes_from_now(self):
        result = parse_time_references('90 minutes from now')
        assert len(result) == 1
        assert result[0].cardinality == 90
        assert result[0].frame == 'minute'
        assert result[0].tense == 'future'

    def test_1000_minutes_from_now(self):
        result = parse_time_references('1000 minutes from now')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'minute'
        assert result[0].tense == 'future'


class TestWeeksFromNowLargeCardinality:
    def test_53_weeks_from_now(self):
        result = parse_time_references('53 weeks from now')
        assert len(result) == 1
        assert result[0].cardinality == 53
        assert result[0].frame == 'week'
        assert result[0].tense == 'future'

    def test_1000_weeks_from_now(self):
        result = parse_time_references('1000 weeks from now')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'week'
        assert result[0].tense == 'future'


class TestMonthsFromNowLargeCardinality:
    def test_36_months_from_now(self):
        result = parse_time_references('36 months from now')
        assert len(result) == 1
        assert result[0].cardinality == 36
        assert result[0].frame == 'month'
        assert result[0].tense == 'future'

    def test_1000_months_from_now(self):
        result = parse_time_references('1000 months from now')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'month'
        assert result[0].tense == 'future'


class TestDaysFromNowLargeCardinality:
    def test_366_days_from_now(self):
        result = parse_time_references('366 days from now')
        assert len(result) == 1
        assert result[0].cardinality == 366
        assert result[0].frame == 'day'
        assert result[0].tense == 'future'

    def test_1000_days_from_now(self):
        result = parse_time_references('1000 days from now')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'day'
        assert result[0].tense == 'future'


# ============================================================================
# Group 10: Future tense -- 'in N units' (large cardinalities)
# ============================================================================

class TestInNUnitsLargeCardinality:
    """'in N units' future pattern with large cardinalities."""

    def test_in_48_hours(self):
        result = parse_time_references('in 48 hours')
        assert len(result) == 1
        assert result[0].cardinality == 48
        assert result[0].frame == 'hour'
        assert result[0].tense == 'future'

    def test_in_90_minutes(self):
        result = parse_time_references('in 90 minutes')
        assert len(result) == 1
        assert result[0].cardinality == 90
        assert result[0].frame == 'minute'
        assert result[0].tense == 'future'

    def test_in_53_weeks(self):
        result = parse_time_references('in 53 weeks')
        assert len(result) == 1
        assert result[0].cardinality == 53
        assert result[0].frame == 'week'
        assert result[0].tense == 'future'

    def test_in_36_months(self):
        result = parse_time_references('in 36 months')
        assert len(result) == 1
        assert result[0].cardinality == 36
        assert result[0].frame == 'month'
        assert result[0].tense == 'future'

    def test_in_500_days(self):
        result = parse_time_references('in 500 days')
        assert len(result) == 1
        assert result[0].cardinality == 500
        assert result[0].frame == 'day'
        assert result[0].tense == 'future'

    def test_in_1000_hours(self):
        result = parse_time_references('in 1000 hours')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'hour'
        assert result[0].tense == 'future'


# ============================================================================
# Group 11: has_temporal_info for large cardinalities
# ============================================================================

class TestHasTemporalInfoLargeCardinality:
    """has_temporal_info correctly detects large cardinality expressions."""

    def test_34_hours_ago(self):
        assert has_temporal_info('34 hours ago') is True

    def test_90_minutes_ago(self):
        assert has_temporal_info('90 minutes ago') is True

    def test_36_months_ago(self):
        assert has_temporal_info('36 months ago') is True

    def test_366_days_ago(self):
        assert has_temporal_info('366 days ago') is True

    def test_1000_weeks_ago(self):
        assert has_temporal_info('1000 weeks ago') is True

    def test_500_years_ago(self):
        assert has_temporal_info('500 years ago') is True

    def test_48_hours_from_now(self):
        assert has_temporal_info('48 hours from now') is True

    def test_1000_days_from_now(self):
        assert has_temporal_info('1000 days from now') is True

    def test_no_false_positive_random_number(self):
        """A bare number is not a time reference."""
        assert has_temporal_info('the answer is 42') is False

    def test_no_false_positive_large_number(self):
        assert has_temporal_info('there are 1000 reasons') is False


# ============================================================================
# Group 12: Phrase context -- large cardinalities embedded in prose
# ============================================================================

class TestPhraseContextLargeCardinality:
    """Large cardinality time references embedded in sentences."""

    def test_48_hours_ago_in_prose(self):
        result = parse_time_references('the outage started 48 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 48
        assert result[0].frame == 'hour'

    def test_90_minutes_ago_in_prose(self):
        result = parse_time_references('she called 90 minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 90
        assert result[0].frame == 'minute'

    def test_36_months_ago_in_prose(self):
        result = parse_time_references('that happened 36 months ago')
        assert len(result) == 1
        assert result[0].cardinality == 36
        assert result[0].frame == 'month'

    def test_500_days_ago_in_prose(self):
        result = parse_time_references('the project started 500 days ago')
        assert len(result) == 1
        assert result[0].cardinality == 500
        assert result[0].frame == 'day'

    def test_1000_hours_from_now_in_prose(self):
        result = parse_time_references('the deadline is 1000 hours from now')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'hour'
        assert result[0].tense == 'future'

    def test_72_hours_before_now_in_prose(self):
        result = parse_time_references('the backup was created 72 hours before now')
        assert len(result) == 1
        assert result[0].cardinality == 72
        assert result[0].frame == 'hour'

    def test_104_weeks_prior_in_prose(self):
        result = parse_time_references('the contract expired 104 weeks prior')
        assert len(result) == 1
        assert result[0].cardinality == 104
        assert result[0].frame == 'week'


# ============================================================================
# Group 13: Cardinality accuracy at boundary values
# ============================================================================

class TestCardinalityAccuracyBoundary:
    """Cardinality values are precisely preserved at boundary points."""

    def test_hours_boundary_24(self):
        """Still works at old max."""
        result = parse_time_references('24 hours ago')
        assert result[0].cardinality == 24

    def test_hours_boundary_25(self):
        """First new value."""
        result = parse_time_references('25 hours ago')
        assert result[0].cardinality == 25

    def test_minutes_boundary_60(self):
        result = parse_time_references('60 minutes ago')
        assert result[0].cardinality == 60

    def test_minutes_boundary_61(self):
        result = parse_time_references('61 minutes ago')
        assert result[0].cardinality == 61

    def test_seconds_boundary_60(self):
        result = parse_time_references('60 seconds ago')
        assert result[0].cardinality == 60

    def test_seconds_boundary_61(self):
        result = parse_time_references('61 seconds ago')
        assert result[0].cardinality == 61

    def test_weeks_boundary_52(self):
        result = parse_time_references('52 weeks ago')
        assert result[0].cardinality == 52

    def test_weeks_boundary_53(self):
        result = parse_time_references('53 weeks ago')
        assert result[0].cardinality == 53

    def test_months_boundary_24(self):
        result = parse_time_references('24 months ago')
        assert result[0].cardinality == 24

    def test_months_boundary_25(self):
        result = parse_time_references('25 months ago')
        assert result[0].cardinality == 25

    def test_days_boundary_365(self):
        result = parse_time_references('365 days ago')
        assert result[0].cardinality == 365

    def test_days_boundary_366(self):
        result = parse_time_references('366 days ago')
        assert result[0].cardinality == 366

    def test_years_boundary_100(self):
        result = parse_time_references('100 years ago')
        assert result[0].cardinality == 100

    def test_years_boundary_101(self):
        result = parse_time_references('101 years ago')
        assert result[0].cardinality == 101

    def test_all_at_max_1000(self):
        """All units reach 1000."""
        for unit in ['hours', 'minutes', 'seconds', 'days', 'weeks', 'months', 'years']:
            result = parse_time_references(f'1000 {unit} ago')
            assert len(result) == 1, f'Failed for 1000 {unit} ago'
            assert result[0].cardinality == 1000, f'Wrong cardinality for 1000 {unit} ago'


# ============================================================================
# Group 14: Tense accuracy for large cardinalities
# ============================================================================

class TestTenseAccuracyLargeCardinality:
    """Tense is correctly past or future for large cardinality expressions."""

    def test_past_tense_ago(self):
        result = parse_time_references('48 hours ago')
        assert result[0].tense == 'past'

    def test_past_tense_before_now(self):
        result = parse_time_references('48 hours before now')
        assert result[0].tense == 'past'

    def test_past_tense_prior(self):
        result = parse_time_references('48 hours prior')
        assert result[0].tense == 'past'

    def test_past_tense_back(self):
        result = parse_time_references('48 hours back')
        assert result[0].tense == 'past'

    def test_future_tense_from_now(self):
        result = parse_time_references('48 hours from now')
        assert result[0].tense == 'future'

    def test_future_tense_in_n_hours(self):
        result = parse_time_references('in 48 hours')
        assert result[0].tense == 'future'

    def test_future_tense_large_months(self):
        result = parse_time_references('36 months from now')
        assert result[0].tense == 'future'

    def test_past_tense_large_months_ago(self):
        result = parse_time_references('36 months ago')
        assert result[0].tense == 'past'


# ============================================================================
# Group 15: Frame accuracy for large cardinalities
# ============================================================================

class TestFrameAccuracyLargeCardinality:
    """Frame (unit) is correctly identified for large cardinality expressions."""

    def test_frame_hours_large(self):
        result = parse_time_references('500 hours ago')
        assert result[0].frame == 'hour'

    def test_frame_minutes_large(self):
        result = parse_time_references('500 minutes ago')
        assert result[0].frame == 'minute'

    def test_frame_seconds_large(self):
        result = parse_time_references('500 seconds ago')
        assert result[0].frame == 'second'

    def test_frame_days_large(self):
        result = parse_time_references('500 days ago')
        assert result[0].frame == 'day'

    def test_frame_weeks_large(self):
        result = parse_time_references('500 weeks ago')
        assert result[0].frame == 'week'

    def test_frame_months_large(self):
        result = parse_time_references('500 months ago')
        assert result[0].frame == 'month'

    def test_frame_years_large(self):
        result = parse_time_references('500 years ago')
        assert result[0].frame == 'year'


# ============================================================================
# Group 16: Result count -- exactly one result per expression
# ============================================================================

class TestResultCountLargeCardinality:
    """Exactly one result is returned for each large cardinality expression."""

    def test_single_result_48_hours_ago(self):
        assert len(parse_time_references('48 hours ago')) == 1

    def test_single_result_90_minutes_ago(self):
        assert len(parse_time_references('90 minutes ago')) == 1

    def test_single_result_36_months_ago(self):
        assert len(parse_time_references('36 months ago')) == 1

    def test_single_result_1000_days_ago(self):
        assert len(parse_time_references('1000 days ago')) == 1

    def test_single_result_500_years_ago(self):
        assert len(parse_time_references('500 years ago')) == 1

    def test_single_result_104_weeks_before_now(self):
        assert len(parse_time_references('104 weeks before now')) == 1

    def test_single_result_200_hours_prior(self):
        assert len(parse_time_references('200 hours prior')) == 1

    def test_single_result_1000_months_back(self):
        assert len(parse_time_references('1000 months back')) == 1


# ============================================================================
# Group 17: Regressions -- previously passing tests still work
# ============================================================================

class TestRegressions:
    """Existing in-range cardinalities still work after KB extension."""

    def test_1_hour_ago(self):
        result = parse_time_references('1 hour ago')
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_24_hours_ago(self):
        result = parse_time_references('24 hours ago')
        assert result[0].cardinality == 24
        assert result[0].frame == 'hour'

    def test_60_minutes_ago(self):
        result = parse_time_references('60 minutes ago')
        assert result[0].cardinality == 60
        assert result[0].frame == 'minute'

    def test_60_seconds_ago(self):
        result = parse_time_references('60 seconds ago')
        assert result[0].cardinality == 60
        assert result[0].frame == 'second'

    def test_52_weeks_ago(self):
        result = parse_time_references('52 weeks ago')
        assert result[0].cardinality == 52
        assert result[0].frame == 'week'

    def test_24_months_ago(self):
        result = parse_time_references('24 months ago')
        assert result[0].cardinality == 24
        assert result[0].frame == 'month'

    def test_365_days_ago(self):
        result = parse_time_references('365 days ago')
        assert result[0].cardinality == 365
        assert result[0].frame == 'day'

    def test_100_years_ago(self):
        result = parse_time_references('100 years ago')
        assert result[0].cardinality == 100
        assert result[0].frame == 'year'

    def test_5_days_ago_still_works(self):
        result = parse_time_references('5 days ago')
        assert result[0].cardinality == 5
        assert result[0].frame == 'day'

    def test_next_week_still_works(self):
        result = parse_time_references('next week')
        assert result[0].tense == 'future'

    def test_eom_still_works(self):
        result = parse_time_references('eom')
        assert result[0].frame == 'month'

    def test_now_still_works(self):
        result = parse_time_references('now')
        assert result[0].tense == 'present'

    def test_5_days_before_now_still_works(self):
        result = parse_time_references('5 days before now')
        assert result[0].cardinality == 5
        assert result[0].tense == 'past'

    def test_3_weeks_prior_still_works(self):
        result = parse_time_references('3 weeks prior')
        assert result[0].cardinality == 3
        assert result[0].tense == 'past'

    def test_2_months_back_still_works(self):
        result = parse_time_references('2 months back')
        assert result[0].cardinality == 2
        assert result[0].tense == 'past'

    def test_has_temporal_info_positive(self):
        assert has_temporal_info('5 days ago') is True

    def test_has_temporal_info_negative(self):
        assert has_temporal_info('hello world') is False


# ============================================================================
# Group 18: Hours -- granular gap coverage (25-40)
# ============================================================================

class TestHoursGranularGap:
    """Every value from 25-40 works for 'N hours ago'."""

    def test_25(self):
        assert parse_time_references('25 hours ago')[0].cardinality == 25

    def test_26(self):
        assert parse_time_references('26 hours ago')[0].cardinality == 26

    def test_27(self):
        assert parse_time_references('27 hours ago')[0].cardinality == 27

    def test_28(self):
        assert parse_time_references('28 hours ago')[0].cardinality == 28

    def test_29(self):
        assert parse_time_references('29 hours ago')[0].cardinality == 29

    def test_30(self):
        assert parse_time_references('30 hours ago')[0].cardinality == 30

    def test_31(self):
        assert parse_time_references('31 hours ago')[0].cardinality == 31

    def test_32(self):
        assert parse_time_references('32 hours ago')[0].cardinality == 32

    def test_33(self):
        assert parse_time_references('33 hours ago')[0].cardinality == 33

    def test_34(self):
        assert parse_time_references('34 hours ago')[0].cardinality == 34

    def test_35(self):
        assert parse_time_references('35 hours ago')[0].cardinality == 35

    def test_36(self):
        assert parse_time_references('36 hours ago')[0].cardinality == 36

    def test_37(self):
        assert parse_time_references('37 hours ago')[0].cardinality == 37

    def test_38(self):
        assert parse_time_references('38 hours ago')[0].cardinality == 38

    def test_39(self):
        assert parse_time_references('39 hours ago')[0].cardinality == 39

    def test_40(self):
        assert parse_time_references('40 hours ago')[0].cardinality == 40


# ============================================================================
# Group 19: Minutes -- granular gap coverage (61-75)
# ============================================================================

class TestMinutesGranularGap:
    """Values from 61-75 work for 'N minutes ago'."""

    def test_61(self):
        assert parse_time_references('61 minutes ago')[0].cardinality == 61

    def test_62(self):
        assert parse_time_references('62 minutes ago')[0].cardinality == 62

    def test_63(self):
        assert parse_time_references('63 minutes ago')[0].cardinality == 63

    def test_65(self):
        assert parse_time_references('65 minutes ago')[0].cardinality == 65

    def test_70(self):
        assert parse_time_references('70 minutes ago')[0].cardinality == 70

    def test_75(self):
        assert parse_time_references('75 minutes ago')[0].cardinality == 75

    def test_80(self):
        assert parse_time_references('80 minutes ago')[0].cardinality == 80

    def test_85(self):
        assert parse_time_references('85 minutes ago')[0].cardinality == 85

    def test_90(self):
        assert parse_time_references('90 minutes ago')[0].cardinality == 90

    def test_100(self):
        assert parse_time_references('100 minutes ago')[0].cardinality == 100


# ============================================================================
# Group 20: Months -- granular gap coverage (25-36)
# ============================================================================

class TestMonthsGranularGap:
    """Values from 25-36 work for 'N months ago'."""

    def test_25(self):
        assert parse_time_references('25 months ago')[0].cardinality == 25

    def test_26(self):
        assert parse_time_references('26 months ago')[0].cardinality == 26

    def test_27(self):
        assert parse_time_references('27 months ago')[0].cardinality == 27

    def test_28(self):
        assert parse_time_references('28 months ago')[0].cardinality == 28

    def test_30(self):
        assert parse_time_references('30 months ago')[0].cardinality == 30

    def test_33(self):
        assert parse_time_references('33 months ago')[0].cardinality == 33

    def test_36(self):
        assert parse_time_references('36 months ago')[0].cardinality == 36


# ============================================================================
# Group 21: Weeks -- granular gap coverage (53-65)
# ============================================================================

class TestWeeksGranularGap:
    """Values from 53-65 work for 'N weeks ago'."""

    def test_53(self):
        assert parse_time_references('53 weeks ago')[0].cardinality == 53

    def test_54(self):
        assert parse_time_references('54 weeks ago')[0].cardinality == 54

    def test_55(self):
        assert parse_time_references('55 weeks ago')[0].cardinality == 55

    def test_60(self):
        assert parse_time_references('60 weeks ago')[0].cardinality == 60

    def test_65(self):
        assert parse_time_references('65 weeks ago')[0].cardinality == 65


# ============================================================================
# Group 22: Cross-unit result isolation -- no spillover
# ============================================================================

class TestResultIsolation:
    """Only one result returned; no extra matches from numeric tokens."""

    def test_48_hours_ago_only_one_result(self):
        result = parse_time_references('48 hours ago')
        assert len(result) == 1

    def test_90_minutes_ago_only_one_result(self):
        result = parse_time_references('90 minutes ago')
        assert len(result) == 1

    def test_36_months_ago_only_one_result(self):
        result = parse_time_references('36 months ago')
        assert len(result) == 1

    def test_730_days_ago_only_one_result(self):
        result = parse_time_references('730 days ago')
        assert len(result) == 1

    def test_104_weeks_ago_only_one_result(self):
        result = parse_time_references('104 weeks ago')
        assert len(result) == 1

    def test_500_years_ago_only_one_result(self):
        result = parse_time_references('500 years ago')
        assert len(result) == 1

    def test_1000_seconds_ago_only_one_result(self):
        result = parse_time_references('1000 seconds ago')
        assert len(result) == 1


# ============================================================================
# Group 23: Seconds -- granular gap coverage (61-80)
# ============================================================================

class TestSecondsGranularGap:
    """Values from 61-80 work for 'N seconds ago'."""

    def test_61(self):
        assert parse_time_references('61 seconds ago')[0].cardinality == 61

    def test_62(self):
        assert parse_time_references('62 seconds ago')[0].cardinality == 62

    def test_63(self):
        assert parse_time_references('63 seconds ago')[0].cardinality == 63

    def test_70(self):
        assert parse_time_references('70 seconds ago')[0].cardinality == 70

    def test_75(self):
        assert parse_time_references('75 seconds ago')[0].cardinality == 75

    def test_80(self):
        assert parse_time_references('80 seconds ago')[0].cardinality == 80

    def test_90(self):
        assert parse_time_references('90 seconds ago')[0].cardinality == 90

    def test_100(self):
        assert parse_time_references('100 seconds ago')[0].cardinality == 100

    def test_200(self):
        assert parse_time_references('200 seconds ago')[0].cardinality == 200


# ============================================================================
# Group 24: Days -- granular gap coverage (366-380)
# ============================================================================

class TestDaysGranularGap:
    """Values from 366-380 work for 'N days ago'."""

    def test_366(self):
        assert parse_time_references('366 days ago')[0].cardinality == 366

    def test_367(self):
        assert parse_time_references('367 days ago')[0].cardinality == 367

    def test_370(self):
        assert parse_time_references('370 days ago')[0].cardinality == 370

    def test_400(self):
        assert parse_time_references('400 days ago')[0].cardinality == 400

    def test_500(self):
        assert parse_time_references('500 days ago')[0].cardinality == 500

    def test_600(self):
        assert parse_time_references('600 days ago')[0].cardinality == 600

    def test_730(self):
        assert parse_time_references('730 days ago')[0].cardinality == 730

    def test_1000(self):
        assert parse_time_references('1000 days ago')[0].cardinality == 1000
