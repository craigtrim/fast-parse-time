#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for get_date_range function."""

import pytest
from datetime import datetime
from fast_parse_time import get_date_range

class TestGetDateRangeHoursBased:
    """Tests for hour-based date ranges."""

    def test_hours_based_range_returns_tuple(self):
        """Two hour-based references should return a (start, end) tuple."""
        result = get_date_range('logs from 2 hours ago and 1 hour ago')
        assert result is not None
        assert isinstance(result, tuple)

    def test_hours_based_range_ordering(self):
        """Earlier hour reference should be the start of the range."""
        result = get_date_range('logs from 2 hours ago and 1 hour ago')
        assert result is not None
        start, end = result
        assert start < end
