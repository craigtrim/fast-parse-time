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


class TestMixedCase:
    """Eod, Eom, Eoy (title case) should work identically to lowercase."""

    def test_Eod_mixed_case(self):
        result = parse_time_references('Eod')
        assert len(result) == 1
        assert result[0].frame == 'day'

    def test_Eom_mixed_case(self):
        result = parse_time_references('Eom')
        assert len(result) == 1
        assert result[0].frame == 'month'

    def test_Eoy_mixed_case(self):
        result = parse_time_references('Eoy')
        assert len(result) == 1
        assert result[0].frame == 'year'


# ============================================================================
# Group 6: Phrase context -- leading non-time words + eod
# ============================================================================
