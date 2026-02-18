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


class TestNowTrailing:
    """'now' is extracted when followed by non-time words."""

    def test_now_please(self):
        result = parse_time_references('now please')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_now_meeting(self):
        result = parse_time_references('now meeting')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_now_call(self):
        result = parse_time_references('now call')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_now_available(self):
        result = parse_time_references('now available')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_now_starting(self):
        result = parse_time_references('now starting')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_now_or_later(self):
        result = parse_time_references('now or later')
        assert len(result) == 1
        assert result[0].tense == 'present'


# ============================================================================
# Group 6: 'right now' in phrase context -- leading non-time words
# ============================================================================
