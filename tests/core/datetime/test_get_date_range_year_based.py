#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for get_date_range function."""

import pytest
from datetime import datetime
from fast_parse_time import get_date_range

class TestGetDateRangeYearBased:
    """Tests for year-based date ranges."""

    def test_year_based_range_returns_tuple(self):
        """Two year-based references should return a (start, end) tuple."""
        result = get_date_range('history from 2 years ago to last year')
        assert result is not None
        assert isinstance(result, tuple)

    def test_year_based_ordering(self):
        """Earlier year reference should be the start of the range."""
        result = get_date_range('history from 2 years ago to last year')
        assert result is not None
        start, end = result
        assert start < end
