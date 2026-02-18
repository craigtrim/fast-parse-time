#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for written month name formats in explicit dates."""

import pytest
from fast_parse_time import extract_explicit_dates

class TestAllFullMonthNames:
    """Tests for all twelve full month names."""

    def test_april(self):
        """'April 10, 2024' should be parsed as an explicit date."""
        result = extract_explicit_dates('April 10, 2024')
        assert len(result) == 1
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_may(self):
        """'May 20, 2024' should be parsed as an explicit date."""
        result = extract_explicit_dates('May 20, 2024')
        assert len(result) == 1
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_june(self):
        """'June 5, 2024' should be parsed as an explicit date."""
        result = extract_explicit_dates('June 5, 2024')
        assert len(result) == 1
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_july(self):
        """'July 4, 2024' should be parsed as an explicit date."""
        result = extract_explicit_dates('July 4, 2024')
        assert len(result) == 1
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_august(self):
        """'August 15, 2024' should be parsed as an explicit date."""
        result = extract_explicit_dates('August 15, 2024')
        assert len(result) == 1
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_september(self):
        """'September 1, 2024' should be parsed as an explicit date."""
        result = extract_explicit_dates('September 1, 2024')
        assert len(result) == 1
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_october(self):
        """'October 31, 2024' should be parsed as an explicit date."""
        result = extract_explicit_dates('October 31, 2024')
        assert len(result) == 1
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_november(self):
        """'November 11, 2024' should be parsed as an explicit date."""
        result = extract_explicit_dates('November 11, 2024')
        assert len(result) == 1
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_december(self):
        """'December 25, 2024' should be parsed as an explicit date."""
        result = extract_explicit_dates('December 25, 2024')
        assert len(result) == 1
        assert 'FULL_EXPLICIT_DATE' in result.values()
