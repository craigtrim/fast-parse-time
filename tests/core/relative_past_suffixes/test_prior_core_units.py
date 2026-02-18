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


class TestPriorCoreUnits:
    """N unit prior returns past-tense RelativeTime with correct fields."""

    def test_5_minutes_prior(self):
        result = parse_time_references('5 minutes prior')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_5_hours_prior(self):
        result = parse_time_references('5 hours prior')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_7_days_prior(self):
        result = parse_time_references('7 days prior')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_1_week_prior(self):
        result = parse_time_references('1 week prior')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_3_months_prior(self):
        result = parse_time_references('3 months prior')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_2_years_prior(self):
        result = parse_time_references('2 years prior')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_30_seconds_prior(self):
        result = parse_time_references('30 seconds prior')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'


# ============================================================================
# Group 4: 'prior' -- abbreviated unit forms
# ============================================================================
