#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for get_date_range function."""

import pytest
from datetime import datetime
from fast_parse_time import get_date_range

class TestGetDateRangeMinutesBased:
    """Tests for minute-based date ranges."""

    def test_minutes_based_range_returns_tuple(self):
        """Two minute-based references should return a (start, end) tuple."""
        result = get_date_range('events from 30 minutes ago to 10 minutes ago')
        assert result is not None
        assert isinstance(result, tuple)

    def test_minutes_based_ordering(self):
        """Earlier minute reference should be the start of the range."""
        result = get_date_range('events from 30 minutes ago to 10 minutes ago')
        assert result is not None
        start, end = result
        assert start < end
