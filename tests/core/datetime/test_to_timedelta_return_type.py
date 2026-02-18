#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for RelativeTime dataclass methods."""

import pytest
from datetime import datetime, timedelta
from fast_parse_time import RelativeTime

class TestToTimedeltaReturnType:
    """Tests for to_timedelta() return type."""

    def test_returns_timedelta(self):
        """to_timedelta() should return a timedelta object."""
        rt = RelativeTime(cardinality=5, frame='day', tense='past')
        assert isinstance(rt.to_timedelta(), timedelta)

    def test_returns_negative_for_past(self):
        """to_timedelta() for past tense should return negative timedelta."""
        rt = RelativeTime(cardinality=5, frame='day', tense='past')
        delta = rt.to_timedelta()
        assert delta.total_seconds() < 0

    def test_returns_positive_for_future(self):
        """to_timedelta() for future tense should return positive timedelta."""
        rt = RelativeTime(cardinality=5, frame='day', tense='future')
        delta = rt.to_timedelta()
        assert delta.total_seconds() > 0
