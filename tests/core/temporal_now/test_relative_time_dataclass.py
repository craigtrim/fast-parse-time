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
# Group 1: Bare 'now' -- basic attribute checks
# ============================================================================


class TestRelativeTimeDataclass:
    """RelativeTime instances built for now/right now support all methods."""

    def test_now_to_timedelta_type(self):
        rt = RelativeTime(cardinality=0, frame='second', tense='present')
        assert isinstance(rt.to_timedelta(), timedelta)

    def test_now_to_timedelta_zero(self):
        rt = RelativeTime(cardinality=0, frame='second', tense='present')
        assert rt.to_timedelta() == timedelta(0)

    def test_right_now_cardinality_zero(self):
        rt = RelativeTime(cardinality=0, frame='second', tense='present')
        assert rt.cardinality == 0

    def test_right_now_frame_second(self):
        rt = RelativeTime(cardinality=0, frame='second', tense='present')
        assert rt.frame == 'second'

    def test_right_now_tense_present(self):
        rt = RelativeTime(cardinality=0, frame='second', tense='present')
        assert rt.tense == 'present'


# ============================================================================
# Group 15: Regression -- existing patterns unaffected
# ============================================================================
