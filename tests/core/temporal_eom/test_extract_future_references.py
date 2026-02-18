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


class TestExtractFutureReferences:
    """eod/eom/eoy are classified as future references."""

    def test_eod_is_future(self):
        result = extract_future_references('eod')
        assert len(result) == 1
        assert result[0].frame == 'day'

    def test_eom_is_future(self):
        result = extract_future_references('eom')
        assert len(result) == 1
        assert result[0].frame == 'month'

    def test_eoy_is_future(self):
        result = extract_future_references('eoy')
        assert len(result) == 1
        assert result[0].frame == 'year'

    def test_eod_in_phrase_is_future(self):
        result = extract_future_references('meeting eod')
        assert len(result) == 1

    def test_eom_in_phrase_is_future(self):
        result = extract_future_references('meeting eom')
        assert len(result) == 1

    def test_eoy_in_phrase_is_future(self):
        result = extract_future_references('meeting eoy')
        assert len(result) == 1


# ============================================================================
# Group 12: extract_past_references returns nothing for eod/eom/eoy
# ============================================================================
