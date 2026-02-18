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


class TestNotPastOrFuture:
    """now/right now are present-tense and must not appear in past/future results."""

    def test_now_not_in_past(self):
        result = extract_past_references('now')
        assert len(result) == 0

    def test_right_now_not_in_past(self):
        result = extract_past_references('right now')
        assert len(result) == 0

    def test_now_not_in_future(self):
        result = extract_future_references('now')
        assert len(result) == 0

    def test_right_now_not_in_future(self):
        result = extract_future_references('right now')
        assert len(result) == 0


# ============================================================================
# Group 11: resolve_to_timedelta
# ============================================================================
