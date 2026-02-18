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


class TestExtractPastReferences:
    """All three suffixes produce past-tense references."""

    def test_before_now_is_past(self):
        result = extract_past_references('5 minutes before now')
        assert len(result) == 1
        assert result[0].tense == 'past'

    def test_prior_is_past(self):
        result = extract_past_references('3 days prior')
        assert len(result) == 1
        assert result[0].tense == 'past'

    def test_back_is_past(self):
        result = extract_past_references('7 hours back')
        assert len(result) == 1
        assert result[0].tense == 'past'


# ============================================================================
# Group 10: extract_future_references returns nothing
# ============================================================================
