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


class TestMultipleAbbreviations:
    """Multiple end-of-period abbreviations in one sentence are all extracted."""

    def test_eod_and_eom(self):
        """Text with both eod and eom should return 2 results."""
        result = parse_time_references('eod and eom')
        assert len(result) == 2
        frames = {r.frame for r in result}
        assert 'day' in frames
        assert 'month' in frames

    def test_eod_and_eoy(self):
        result = parse_time_references('eod and eoy')
        assert len(result) == 2
        frames = {r.frame for r in result}
        assert 'day' in frames
        assert 'year' in frames

    def test_eom_and_eoy(self):
        result = parse_time_references('eom and eoy')
        assert len(result) == 2
        frames = {r.frame for r in result}
        assert 'month' in frames
        assert 'year' in frames

    def test_all_three_abbreviations(self):
        """Three abbreviations separated by non-time words produce 3 results."""
        result = parse_time_references('eod and eom and eoy')
        assert len(result) == 3
        frames = {r.frame for r in result}
        assert frames == {'day', 'month', 'year'}


# ============================================================================
# Group 17: RelativeTime.to_timedelta via dataclass method
# ============================================================================
