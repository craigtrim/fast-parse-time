#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for written month name formats in explicit dates."""

import pytest
from fast_parse_time import extract_explicit_dates

class TestAbbreviatedMonths:
    """Tests for abbreviated month names."""

    def test_jan(self):
        """'Jan 15, 2024' should be parsed."""
        result = extract_explicit_dates('Jan 15, 2024')
        assert len(result) == 1

    def test_feb(self):
        """'Feb 15, 2024' should be parsed."""
        result = extract_explicit_dates('Feb 15, 2024')
        assert len(result) == 1

    def test_sept(self):
        """'Sept 15, 2024' should be parsed (alternative abbreviation)."""
        result = extract_explicit_dates('Sept 15, 2024')
        assert len(result) == 1

    def test_dec(self):
        """'Dec 25, 2024' should be parsed."""
        result = extract_explicit_dates('Dec 25, 2024')
        assert len(result) == 1
