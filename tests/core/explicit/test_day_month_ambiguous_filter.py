#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for parse_dates_with_type function."""

import pytest
from fast_parse_time import parse_dates_with_type

class TestDayMonthAmbiguousFilter:
    """Tests for filtering by DAY_MONTH_AMBIGUOUS."""

    def test_filter_returns_only_ambiguous(self):
        """Filter by DAY_MONTH_AMBIGUOUS should return only ambiguous dates."""
        result = parse_dates_with_type('Meeting 4/8 or 04/08/2024', 'DAY_MONTH_AMBIGUOUS')
        assert len(result) == 1
        assert '4/8' in result
        assert '04/08/2024' not in result

    def test_filter_type_value(self):
        """Ambiguous dates should have the DAY_MONTH_AMBIGUOUS type."""
        result = parse_dates_with_type('Appointment 4/8', 'DAY_MONTH_AMBIGUOUS')
        assert result.get('4/8') == 'DAY_MONTH_AMBIGUOUS'

    def test_filter_no_ambiguous_returns_empty(self):
        """No ambiguous dates in text should return empty dict."""
        result = parse_dates_with_type('Meeting on 04/08/2024', 'DAY_MONTH_AMBIGUOUS')
        assert result == {}
