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


class TestRelativeTimeDataclass:
    """RelativeTime instances created for eod/eom/eoy support all methods."""

    def test_eod_to_timedelta(self):
        rt = RelativeTime(cardinality=0, frame='day', tense='future')
        delta = rt.to_timedelta()
        assert isinstance(delta, timedelta)

    def test_eom_to_timedelta(self):
        rt = RelativeTime(cardinality=0, frame='month', tense='future')
        delta = rt.to_timedelta()
        assert isinstance(delta, timedelta)

    def test_eoy_to_timedelta(self):
        rt = RelativeTime(cardinality=0, frame='year', tense='future')
        delta = rt.to_timedelta()
        assert isinstance(delta, timedelta)

    def test_eod_cardinality_zero(self):
        rt = RelativeTime(cardinality=0, frame='day', tense='future')
        assert rt.cardinality == 0

    def test_eom_cardinality_zero(self):
        rt = RelativeTime(cardinality=0, frame='month', tense='future')
        assert rt.cardinality == 0

    def test_eoy_cardinality_zero(self):
        rt = RelativeTime(cardinality=0, frame='year', tense='future')
        assert rt.cardinality == 0


# ============================================================================
# Group 18: Regression -- existing patterns unaffected
# ============================================================================
