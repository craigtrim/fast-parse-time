#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for RelativeTime dataclass methods."""

import pytest
from datetime import datetime, timedelta
from fast_parse_time import RelativeTime

class TestToDatetimeWithReference:
    """Tests for to_datetime() with a custom reference datetime."""

    def test_past_is_before_reference(self):
        """Past tense datetime should be before the reference."""
        ref = datetime(2025, 6, 15, 12, 0, 0)
        rt = RelativeTime(cardinality=5, frame='day', tense='past')
        result = rt.to_datetime(reference=ref)
        assert result < ref

    def test_future_is_after_reference(self):
        """Future tense datetime should be after the reference."""
        ref = datetime(2025, 6, 15, 12, 0, 0)
        rt = RelativeTime(cardinality=5, frame='day', tense='future')
        result = rt.to_datetime(reference=ref)
        assert result > ref

    def test_exact_past_calculation(self):
        """5 days past from a known reference should give exact result."""
        ref = datetime(2025, 6, 20, 0, 0, 0)
        rt = RelativeTime(cardinality=5, frame='day', tense='past')
        result = rt.to_datetime(reference=ref)
        assert result == datetime(2025, 6, 15, 0, 0, 0)

    def test_exact_future_calculation(self):
        """3 days future from a known reference should give exact result."""
        ref = datetime(2025, 6, 15, 0, 0, 0)
        rt = RelativeTime(cardinality=3, frame='day', tense='future')
        result = rt.to_datetime(reference=ref)
        assert result == datetime(2025, 6, 18, 0, 0, 0)

    def test_exact_week_calculation(self):
        """1 week past from a known reference should be 7 days earlier."""
        ref = datetime(2025, 6, 22, 0, 0, 0)
        rt = RelativeTime(cardinality=1, frame='week', tense='past')
        result = rt.to_datetime(reference=ref)
        assert result == datetime(2025, 6, 15, 0, 0, 0)

    def test_exact_hour_calculation(self):
        """2 hours past from a known reference should give exact result."""
        ref = datetime(2025, 6, 15, 10, 0, 0)
        rt = RelativeTime(cardinality=2, frame='hour', tense='past')
        result = rt.to_datetime(reference=ref)
        assert result == datetime(2025, 6, 15, 8, 0, 0)
