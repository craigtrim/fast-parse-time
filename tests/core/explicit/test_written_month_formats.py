#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for written month name formats in explicit dates."""

import pytest
from fast_parse_time import extract_explicit_dates

class TestWrittenMonthFormats:
    """Tests for basic written month formats."""

    def test_month_day_year(self):
        """'March 15, 2024' should be parsed as explicit date."""
        result = extract_explicit_dates('March 15, 2024')
        assert result is not None
        assert len(result) == 1
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_day_month_year(self):
        """'15 March 2024' should be parsed as explicit date."""
        result = extract_explicit_dates('15 March 2024')
        assert result is not None
        assert len(result) == 1
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_abbreviated_month(self):
        """'Mar 15, 2024' should be parsed as explicit date."""
        result = extract_explicit_dates('Mar 15, 2024')
        assert result is not None
        assert len(result) == 1
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_ordinal_day(self):
        """'January 1st, 2024' should be parsed as explicit date."""
        result = extract_explicit_dates('January 1st, 2024')
        assert result is not None
        assert len(result) == 1
        assert 'FULL_EXPLICIT_DATE' in result.values()
