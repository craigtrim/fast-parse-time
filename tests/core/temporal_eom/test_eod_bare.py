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


class TestEodBare:
    """Bare 'eod' returns exactly one RelativeTime with correct attributes."""

    def test_eod_returns_one_result(self):
        result = parse_time_references('eod')
        assert len(result) == 1

    def test_eod_cardinality(self):
        result = parse_time_references('eod')
        assert result[0].cardinality == 0

    def test_eod_frame(self):
        result = parse_time_references('eod')
        assert result[0].frame == 'day'

    def test_eod_tense(self):
        result = parse_time_references('eod')
        assert result[0].tense == 'future'

    def test_eod_is_relative_time(self):
        result = parse_time_references('eod')
        assert isinstance(result[0], RelativeTime)


# ============================================================================
# Group 2: Bare 'eom' -- basic attribute checks
# ============================================================================
