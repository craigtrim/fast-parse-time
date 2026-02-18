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


class TestBeforeNowCoreUnits:
    """N unit before now returns past-tense RelativeTime with correct fields."""

    def test_5_minutes_before_now(self):
        result = parse_time_references('5 minutes before now')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_5_hours_before_now(self):
        result = parse_time_references('5 hours before now')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_7_days_before_now(self):
        result = parse_time_references('7 days before now')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_1_week_before_now(self):
        result = parse_time_references('1 week before now')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_3_months_before_now(self):
        result = parse_time_references('3 months before now')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_2_years_before_now(self):
        result = parse_time_references('2 years before now')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_30_seconds_before_now(self):
        result = parse_time_references('30 seconds before now')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'


# ============================================================================
# Group 2: 'before now' -- abbreviated unit forms
# ============================================================================
