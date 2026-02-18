#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for parse_dates_with_type function."""

import pytest
from fast_parse_time import parse_dates_with_type

class TestFullExplicitDateFilter:
    """Tests for filtering by FULL_EXPLICIT_DATE."""

    def test_filter_returns_only_full_dates(self):
        """Filter by FULL_EXPLICIT_DATE should exclude partial dates."""
        result = parse_dates_with_type('Event 04/08/2024 or maybe 3/24', 'FULL_EXPLICIT_DATE')
        assert len(result) == 1
        assert '04/08/2024' in result
        assert '3/24' not in result

    def test_filter_correct_type_value(self):
        """Filtered results should have the correct type value."""
        result = parse_dates_with_type('Born on 04/08/2024', 'FULL_EXPLICIT_DATE')
        assert result['04/08/2024'] == 'FULL_EXPLICIT_DATE'

    def test_filter_no_matches_returns_empty(self):
        """Filtering for FULL_EXPLICIT_DATE when only partial dates exist should return empty."""
        result = parse_dates_with_type('Appointment on 3/24', 'FULL_EXPLICIT_DATE')
        assert result == {}

    def test_multiple_full_dates(self):
        """All matching full dates should be returned."""
        result = parse_dates_with_type('Holidays: 12/25/2023 and 01/01/2024', 'FULL_EXPLICIT_DATE')
        assert len(result) == 2
        assert '12/25/2023' in result
        assert '01/01/2024' in result
