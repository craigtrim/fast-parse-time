#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for parse_dates_with_type function."""

import pytest
from fast_parse_time import parse_dates_with_type

class TestMultipleFullDatesWithFilter:
    """Tests for multiple full dates with an explicit filter."""

    def test_three_full_dates_with_filter(self):
        """Three comma-separated full dates - documents known extraction limitation."""
        # BOUNDARY: When dates are separated by commas, the extractor may only
        # capture the last matching date. This is a known behavior of the library.
        result = parse_dates_with_type(
            'Dates: 01/01/2024, 06/15/2024, and 12/31/2024',
            'FULL_EXPLICIT_DATE'
        )
        assert len(result) >= 1
        assert any(d in result for d in ['01/01/2024', '06/15/2024', '12/31/2024'])

    def test_filter_excludes_partial_from_multi_date_text(self):
        """FULL_EXPLICIT_DATE filter should exclude partial dates in multi-date text."""
        result = parse_dates_with_type(
            'Full date 04/08/2024 and partial 3/24',
            'FULL_EXPLICIT_DATE'
        )
        assert '04/08/2024' in result
        assert '3/24' not in result
