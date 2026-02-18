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


class TestResolveToTimedelta:
    """resolve_to_timedelta returns a timedelta for eod/eom/eoy."""

    def test_eod_timedelta_is_timedelta(self):
        result = resolve_to_timedelta('eod')
        assert len(result) == 1
        assert isinstance(result[0], timedelta)

    def test_eom_timedelta_is_timedelta(self):
        result = resolve_to_timedelta('eom')
        assert len(result) == 1
        assert isinstance(result[0], timedelta)

    def test_eoy_timedelta_is_timedelta(self):
        result = resolve_to_timedelta('eoy')
        assert len(result) == 1
        assert isinstance(result[0], timedelta)

    def test_eod_timedelta_not_negative(self):
        """eod is a future reference so delta should not be negative."""
        result = resolve_to_timedelta('eod')
        assert result[0] >= timedelta(0)

    def test_eom_timedelta_not_negative(self):
        result = resolve_to_timedelta('eom')
        assert result[0] >= timedelta(0)

    def test_eoy_timedelta_not_negative(self):
        result = resolve_to_timedelta('eoy')
        assert result[0] >= timedelta(0)


# ============================================================================
# Group 15: parse_dates integration
# ============================================================================
