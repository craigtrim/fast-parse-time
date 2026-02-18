#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
from fast_parse_time import parse_time_references, has_temporal_info


# ============================================================================
# Group 1: hours -- gap range 25-168 (above current max of 24)
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
