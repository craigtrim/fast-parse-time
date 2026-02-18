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


class TestNoPastReferences:
    """eod/eom/eoy are future references and should not appear in past results."""

    def test_eod_not_past(self):
        result = extract_past_references('eod')
        assert len(result) == 0

    def test_eom_not_past(self):
        result = extract_past_references('eom')
        assert len(result) == 0

    def test_eoy_not_past(self):
        result = extract_past_references('eoy')
        assert len(result) == 0


# ============================================================================
# Group 13: extract_relative_times
# ============================================================================
