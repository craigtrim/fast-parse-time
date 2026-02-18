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


class TestResolveToTimedelta:
    """Past-tense results resolve to negative timedeltas."""

    def test_before_now_timedelta_is_timedelta(self):
        result = resolve_to_timedelta('5 days before now')
        assert len(result) == 1
        assert isinstance(result[0], timedelta)

    def test_before_now_timedelta_negative(self):
        result = resolve_to_timedelta('5 days before now')
        assert result[0] < timedelta(0)

    def test_prior_timedelta_negative(self):
        result = resolve_to_timedelta('3 months prior')
        assert len(result) == 1
        assert result[0] < timedelta(0)

    def test_back_timedelta_negative(self):
        result = resolve_to_timedelta('2 weeks back')
        assert len(result) == 1
        assert result[0] < timedelta(0)

    def test_before_now_5_days_delta_value(self):
        result = resolve_to_timedelta('5 days before now')
        assert result[0] == timedelta(days=-5)

    def test_prior_2_weeks_delta_value(self):
        result = resolve_to_timedelta('2 weeks prior')
        assert result[0] == timedelta(days=-14)


# ============================================================================
# Group 12: parse_dates integration
# ============================================================================
