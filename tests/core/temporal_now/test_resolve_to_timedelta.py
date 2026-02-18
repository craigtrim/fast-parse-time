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


class TestResolveToTimedelta:
    """resolve_to_timedelta returns timedelta(0) for now/right now."""

    def test_now_timedelta_is_timedelta(self):
        result = resolve_to_timedelta('now')
        assert len(result) == 1
        assert isinstance(result[0], timedelta)

    def test_right_now_timedelta_is_timedelta(self):
        result = resolve_to_timedelta('right now')
        assert len(result) == 1
        assert isinstance(result[0], timedelta)

    def test_now_timedelta_is_zero(self):
        """Zero cardinality present-tense = no offset."""
        result = resolve_to_timedelta('now')
        assert result[0] == timedelta(0)

    def test_right_now_timedelta_is_zero(self):
        result = resolve_to_timedelta('right now')
        assert result[0] == timedelta(0)

    def test_now_timedelta_not_negative(self):
        result = resolve_to_timedelta('now')
        assert result[0] >= timedelta(0)

    def test_right_now_timedelta_not_negative(self):
        result = resolve_to_timedelta('right now')
        assert result[0] >= timedelta(0)


# ============================================================================
# Group 12: parse_dates integration
# ============================================================================
