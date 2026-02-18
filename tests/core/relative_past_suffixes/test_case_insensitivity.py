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


class TestCaseInsensitivity:
    """All patterns are case-insensitive (input is lowercased)."""

    def test_BEFORE_NOW_uppercase(self):
        result = parse_time_references('5 DAYS BEFORE NOW')
        assert len(result) == 1
        assert result[0].tense == 'past'

    def test_PRIOR_uppercase(self):
        result = parse_time_references('3 MONTHS PRIOR')
        assert len(result) == 1
        assert result[0].tense == 'past'

    def test_BACK_uppercase(self):
        result = parse_time_references('7 HOURS BACK')
        assert len(result) == 1
        assert result[0].tense == 'past'


# ============================================================================
# Group 14: Regression -- existing patterns unaffected
# ============================================================================
