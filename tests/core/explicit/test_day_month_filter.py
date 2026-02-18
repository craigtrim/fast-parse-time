#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for parse_dates_with_type function."""

import pytest
from fast_parse_time import parse_dates_with_type

class TestDayMonthFilter:
    """Tests for filtering by DAY_MONTH."""

    def test_filter_returns_day_month(self):
        """Filter by DAY_MONTH should return only clear day-month dates."""
        result = parse_dates_with_type('European date 31/03 and US date 3/24', 'DAY_MONTH')
        assert '31/03' in result

    def test_filter_excludes_others(self):
        """DAY_MONTH filter should exclude MONTH_DAY dates."""
        result = parse_dates_with_type('Dates: 29/2 and 3/24', 'DAY_MONTH')
        assert '29/2' in result
        assert '3/24' not in result
