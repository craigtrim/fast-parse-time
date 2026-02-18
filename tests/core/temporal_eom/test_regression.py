#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from datetime import timedelta

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


# ============================================================================
# Group 1: Bare 'eod' -- basic attribute checks
# ============================================================================


class TestRegression:
    """Existing time reference patterns still work after adding eod/eom/eoy."""

    def test_yesterday_still_works(self):
        result = parse_time_references('yesterday')
        assert len(result) == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_tomorrow_still_works(self):
        result = parse_time_references('tomorrow')
        assert len(result) == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'future'

    def test_5_days_ago(self):
        result = parse_time_references('5 days ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_last_week(self):
        result = parse_time_references('last week')
        assert len(result) == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_next_week(self):
        result = parse_time_references('next week')
        assert len(result) == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'future'

    def test_3_months_ago(self):
        result = parse_time_references('3 months ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_2_years_from_now(self):
        result = parse_time_references('2 years from now')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'year'
        assert result[0].tense == 'future'

    def test_1_hour_ago(self):
        result = parse_time_references('1 hour ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'

    def test_10_minutes_from_now(self):
        result = parse_time_references('10 minutes from now')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'minute'

    def test_30_seconds_ago(self):
        result = parse_time_references('30 seconds ago')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'second'

    def test_half_an_hour_ago(self):
        result = parse_time_references('half an hour ago')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'minute'

    def test_several_days_ago(self):
        result = parse_time_references('several days ago')
        assert len(result) == 1
        assert result[0].cardinality == 3

    def test_has_temporal_info_regression(self):
        assert has_temporal_info('5 days ago') is True

    def test_no_temporal_info_regression(self):
        assert has_temporal_info('hello world') is False
