#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for parse_dates_with_type function."""

import pytest
from fast_parse_time import parse_dates_with_type

class TestMonthDayFilter:
    """Tests for filtering by MONTH_DAY."""

    def test_filter_returns_only_month_day(self):
        """Filter by MONTH_DAY should exclude full dates."""
        result = parse_dates_with_type('Event 04/08/2024 or 3/24', 'MONTH_DAY')
        assert len(result) == 1
        assert '3/24' in result
        assert '04/08/2024' not in result

    def test_filter_no_matches_returns_empty(self):
        """Filtering for MONTH_DAY when only full dates exist should return empty."""
        result = parse_dates_with_type('Meeting on 04/08/2024', 'MONTH_DAY')
        assert result == {}
