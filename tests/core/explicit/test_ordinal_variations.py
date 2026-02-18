#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for written month name formats in explicit dates."""

import pytest
from fast_parse_time import extract_explicit_dates

class TestOrdinalVariations:
    """Tests for different ordinal suffix variations."""

    def test_ordinal_1st(self):
        """'January 1st, 2024' should be parsed."""
        result = extract_explicit_dates('January 1st, 2024')
        assert len(result) == 1

    def test_ordinal_2nd(self):
        """'February 2nd, 2024' should be parsed."""
        result = extract_explicit_dates('February 2nd, 2024')
        assert len(result) == 1

    def test_ordinal_3rd(self):
        """'March 3rd, 2024' should be parsed."""
        result = extract_explicit_dates('March 3rd, 2024')
        assert len(result) == 1

    def test_ordinal_4th(self):
        """'April 4th, 2024' should be parsed."""
        result = extract_explicit_dates('April 4th, 2024')
        assert len(result) == 1
