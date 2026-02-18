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


class TestHasTemporalInfo:
    """has_temporal_info returns True for texts containing now/right now."""

    def test_now_has_temporal_info(self):
        assert has_temporal_info('now') is True

    def test_right_now_has_temporal_info(self):
        assert has_temporal_info('right now') is True

    def test_NOW_has_temporal_info(self):
        assert has_temporal_info('NOW') is True

    def test_RIGHT_NOW_has_temporal_info(self):
        assert has_temporal_info('RIGHT NOW') is True

    def test_meeting_now_has_temporal_info(self):
        assert has_temporal_info('meeting now') is True

    def test_meeting_right_now_has_temporal_info(self):
        assert has_temporal_info('meeting right now') is True

    def test_non_temporal_false(self):
        assert has_temporal_info('regular sentence') is False

    def test_another_non_temporal_false(self):
        assert has_temporal_info('hello world') is False


# ============================================================================
# Group 9: extract_relative_times
# ============================================================================
