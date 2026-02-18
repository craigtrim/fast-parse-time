#!/usr/bin/env python
# -*- coding: UTF-8 -*-
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
from datetime import timedelta


# ============================================================================
# Group 1: 'before now' -- core unit coverage
# ============================================================================


class TestNotFutureReferences:
    """Past-tense expressions must not appear in future results."""

    def test_before_now_not_future(self):
        result = extract_future_references('5 minutes before now')
        assert len(result) == 0

    def test_prior_not_future(self):
        result = extract_future_references('3 days prior')
        assert len(result) == 0

    def test_back_not_future(self):
        result = extract_future_references('7 hours back')
        assert len(result) == 0


# ============================================================================
# Group 11: resolve_to_timedelta -- negative delta (past)
# ============================================================================
