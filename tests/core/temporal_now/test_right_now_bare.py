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


class TestRightNowBare:
    """Bare 'right now' returns exactly one present-tense RelativeTime."""

    def test_right_now_returns_one_result(self):
        result = parse_time_references('right now')
        assert len(result) == 1

    def test_right_now_cardinality(self):
        result = parse_time_references('right now')
        assert result[0].cardinality == 0

    def test_right_now_frame(self):
        result = parse_time_references('right now')
        assert result[0].frame == 'second'

    def test_right_now_tense(self):
        result = parse_time_references('right now')
        assert result[0].tense == 'present'

    def test_right_now_is_relative_time(self):
        result = parse_time_references('right now')
        assert isinstance(result[0], RelativeTime)


# ============================================================================
# Group 3: Case insensitivity
# ============================================================================
