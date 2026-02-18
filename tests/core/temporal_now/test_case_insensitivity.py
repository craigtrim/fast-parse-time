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


class TestCaseInsensitivity:
    """now and right now are case-insensitive (input is lowercased)."""

    def test_NOW_uppercase(self):
        result = parse_time_references('NOW')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_Now_mixed_case(self):
        result = parse_time_references('Now')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_RIGHT_NOW_uppercase(self):
        result = parse_time_references('RIGHT NOW')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_Right_Now_mixed_case(self):
        result = parse_time_references('Right Now')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_NOW_frame(self):
        result = parse_time_references('NOW')
        assert result[0].frame == 'second'

    def test_RIGHT_NOW_frame(self):
        result = parse_time_references('RIGHT NOW')
        assert result[0].frame == 'second'


# ============================================================================
# Group 4: 'now' in phrase context -- leading non-time words
# ============================================================================
