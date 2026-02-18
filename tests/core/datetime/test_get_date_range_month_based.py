#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for get_date_range function."""

import pytest
from datetime import datetime
from fast_parse_time import get_date_range

class TestGetDateRangeMonthBased:
    """Tests for month-based date ranges."""

    def test_month_based_range_returns_tuple(self):
        """Two month-based references should return a (start, end) tuple."""
        result = get_date_range('data from 6 months ago to 1 month ago')
        assert result is not None
        assert isinstance(result, tuple)

    def test_month_based_ordering(self):
        """Earlier month reference should be the start of the range."""
        result = get_date_range('data from 6 months ago to 1 month ago')
        assert result is not None
        start, end = result
        assert start < end
