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
# Group 1: Bare 'now' -- basic attribute checks
# ============================================================================


class TestDisambiguation:
    """'now' inside existing patterns must not produce an extra present result."""

    def test_5_days_from_now_is_one_result(self):
        """'5 days from now' → exactly 1 result (future), not 2."""
        result = parse_time_references('5 days from now')
        assert len(result) == 1

    def test_5_days_from_now_is_future(self):
        result = parse_time_references('5 days from now')
        assert result[0].tense == 'future'

    def test_5_days_from_now_cardinality(self):
        result = parse_time_references('5 days from now')
        assert result[0].cardinality == 5

    def test_3_weeks_from_now_is_one_result(self):
        result = parse_time_references('3 weeks from now')
        assert len(result) == 1
        assert result[0].tense == 'future'

    def test_1_hour_from_now_is_one_result(self):
        result = parse_time_references('1 hour from now')
        assert len(result) == 1
        assert result[0].tense == 'future'

    def test_2_months_from_now_is_one_result(self):
        result = parse_time_references('2 months from now')
        assert len(result) == 1
        assert result[0].tense == 'future'

    def test_10_minutes_from_now_is_one_result(self):
        result = parse_time_references('10 minutes from now')
        assert len(result) == 1
        assert result[0].tense == 'future'


# ============================================================================
# Group 14: RelativeTime dataclass methods
# ============================================================================
