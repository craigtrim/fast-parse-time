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


class TestExtractRelativeTimes:
    """extract_relative_times returns RelativeTime for now/right now."""

    def test_now_is_relative_time_instance(self):
        result = extract_relative_times('now')
        assert len(result) == 1
        assert isinstance(result[0], RelativeTime)

    def test_right_now_is_relative_time_instance(self):
        result = extract_relative_times('right now')
        assert len(result) == 1
        assert isinstance(result[0], RelativeTime)

    def test_now_frame_via_extract(self):
        result = extract_relative_times('now')
        assert result[0].frame == 'second'

    def test_right_now_frame_via_extract(self):
        result = extract_relative_times('right now')
        assert result[0].frame == 'second'

    def test_now_tense_via_extract(self):
        result = extract_relative_times('now')
        assert result[0].tense == 'present'

    def test_right_now_tense_via_extract(self):
        result = extract_relative_times('right now')
        assert result[0].tense == 'present'


# ============================================================================
# Group 10: Not a past or future reference
# ============================================================================
