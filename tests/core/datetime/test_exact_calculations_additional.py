#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for RelativeTime dataclass methods."""

import pytest
from datetime import datetime, timedelta
from fast_parse_time import RelativeTime

class TestExactCalculationsAdditional:
    """Additional exact calculation tests for various frames."""

    def test_exact_month_calculation(self):
        """3 months past from a known reference should be 90 days earlier."""
        ref = datetime(2025, 9, 1, 0, 0, 0)
        rt = RelativeTime(cardinality=3, frame='month', tense='past')
        result = rt.to_datetime(reference=ref)
        assert result == datetime(2025, 6, 3, 0, 0, 0)

    def test_exact_year_calculation(self):
        """1 year past from a known reference should be 365 days earlier."""
        ref = datetime(2025, 6, 15, 0, 0, 0)
        rt = RelativeTime(cardinality=1, frame='year', tense='past')
        result = rt.to_datetime(reference=ref)
        assert result == datetime(2024, 6, 15, 0, 0, 0)

    def test_exact_minute_calculation(self):
        """30 minutes past from a known reference should give exact result."""
        ref = datetime(2025, 6, 15, 10, 30, 0)
        rt = RelativeTime(cardinality=30, frame='minute', tense='past')
        result = rt.to_datetime(reference=ref)
        assert result == datetime(2025, 6, 15, 10, 0, 0)
