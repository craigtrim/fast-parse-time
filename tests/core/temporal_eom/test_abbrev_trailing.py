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
# Group 1: Bare 'eod' -- basic attribute checks
# ============================================================================


class TestAbbrevTrailing:
    """Abbreviations followed by non-time words are still extracted."""

    def test_eod_meeting(self):
        result = parse_time_references('eod meeting')
        assert len(result) == 1
        assert result[0].frame == 'day'

    def test_eod_call(self):
        result = parse_time_references('eod call')
        assert len(result) == 1
        assert result[0].frame == 'day'

    def test_eod_deadline(self):
        result = parse_time_references('eod deadline')
        assert len(result) == 1
        assert result[0].frame == 'day'

    def test_eom_meeting(self):
        result = parse_time_references('eom meeting')
        assert len(result) == 1
        assert result[0].frame == 'month'

    def test_eom_close(self):
        result = parse_time_references('eom close')
        assert len(result) == 1
        assert result[0].frame == 'month'

    def test_eoy_meeting(self):
        result = parse_time_references('eoy meeting')
        assert len(result) == 1
        assert result[0].frame == 'year'

    def test_eoy_close(self):
        result = parse_time_references('eoy close')
        assert len(result) == 1
        assert result[0].frame == 'year'


# ============================================================================
# Group 10: has_temporal_info
# ============================================================================
