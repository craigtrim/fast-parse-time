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


class TestExtractRelativeTimes:
    """extract_relative_times returns RelativeTime instances for eod/eom/eoy."""

    def test_eod_relative_time_instance(self):
        result = extract_relative_times('eod')
        assert len(result) == 1
        assert isinstance(result[0], RelativeTime)

    def test_eom_relative_time_instance(self):
        result = extract_relative_times('eom')
        assert len(result) == 1
        assert isinstance(result[0], RelativeTime)

    def test_eoy_relative_time_instance(self):
        result = extract_relative_times('eoy')
        assert len(result) == 1
        assert isinstance(result[0], RelativeTime)

    def test_eod_relative_time_frame(self):
        result = extract_relative_times('eod')
        assert result[0].frame == 'day'

    def test_eom_relative_time_frame(self):
        result = extract_relative_times('eom')
        assert result[0].frame == 'month'

    def test_eoy_relative_time_frame(self):
        result = extract_relative_times('eoy')
        assert result[0].frame == 'year'


# ============================================================================
# Group 14: resolve_to_timedelta
# ============================================================================
