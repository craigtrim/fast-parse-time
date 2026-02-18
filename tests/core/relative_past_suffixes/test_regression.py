#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest

from fast_parse_time import (
    RelativeTime,
    extract_future_references,
    extract_past_references,
    extract_relative_times,
    has_temporal_info,
    parse_dates,
    parse_time_references,
    resolve_to_timedelta,
)
from datetime import timedelta


# ============================================================================
# Group 1: 'before now' -- core unit coverage
# ============================================================================


class TestRegression:
    """Existing patterns still work after adding before now / prior / back."""

    def test_5_days_ago_still_works(self):
        result = parse_time_references('5 days ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].tense == 'past'

    def test_last_week_still_works(self):
        result = parse_time_references('last week')
        assert len(result) == 1
        assert result[0].tense == 'past'

    def test_3_months_ago_still_works(self):
        result = parse_time_references('3 months ago')
        assert len(result) == 1
        assert result[0].cardinality == 3

    def test_tomorrow_still_works(self):
        result = parse_time_references('tomorrow')
        assert len(result) == 1
        assert result[0].tense == 'future'

    def test_5_days_from_now_still_works(self):
        result = parse_time_references('5 days from now')
        assert len(result) == 1
        assert result[0].tense == 'future'
        assert result[0].cardinality == 5

    def test_now_still_works(self):
        result = parse_time_references('now')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_eod_still_works(self):
        result = parse_time_references('eod')
        assert len(result) == 1
        assert result[0].tense == 'future'

    def test_yesterday_still_works(self):
        result = parse_time_references('yesterday')
        assert len(result) == 1
        assert result[0].tense == 'past'

    def test_half_an_hour_ago_still_works(self):
        result = parse_time_references('half an hour ago')
        assert len(result) == 1
        assert result[0].cardinality == 30

    def test_several_weeks_ago_still_works(self):
        result = parse_time_references('several weeks ago')
        assert len(result) == 1
        assert result[0].cardinality == 3

    def test_right_now_still_works(self):
        result = parse_time_references('right now')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_2_years_from_now_still_works(self):
        result = parse_time_references('2 years from now')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].tense == 'future'

    def test_has_temporal_info_regression_true(self):
        assert has_temporal_info('5 days ago') is True

    def test_has_temporal_info_regression_false(self):
        assert has_temporal_info('hello world') is False

    def test_10_hours_ago_still_works(self):
        result = parse_time_references('10 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'hour'

    def test_next_week_still_works(self):
        result = parse_time_references('next week')
        assert len(result) == 1
        assert result[0].tense == 'future'

    def test_eom_still_works(self):
        result = parse_time_references('eom')
        assert len(result) == 1
        assert result[0].frame == 'month'


# ============================================================================
# Group 15: Cardinality accuracy across all three patterns
# ============================================================================
