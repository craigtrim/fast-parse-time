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


class TestEomBare:
    """Bare 'eom' returns exactly one RelativeTime with correct attributes."""

    def test_eom_returns_one_result(self):
        result = parse_time_references('eom')
        assert len(result) == 1

    def test_eom_cardinality(self):
        result = parse_time_references('eom')
        assert result[0].cardinality == 0

    def test_eom_frame(self):
        result = parse_time_references('eom')
        assert result[0].frame == 'month'

    def test_eom_tense(self):
        result = parse_time_references('eom')
        assert result[0].tense == 'future'

    def test_eom_is_relative_time(self):
        result = parse_time_references('eom')
        assert isinstance(result[0], RelativeTime)


# ============================================================================
# Group 3: Bare 'eoy' -- basic attribute checks
# ============================================================================
