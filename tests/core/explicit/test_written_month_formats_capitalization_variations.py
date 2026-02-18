#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for written month name formats in explicit dates."""

import pytest
from fast_parse_time import extract_explicit_dates

class TestCapitalizationVariations:
    """Tests for capitalization variations."""

    def test_uppercase(self):
        """'MARCH 15, 2024' should be parsed (case-insensitive)."""
        result = extract_explicit_dates('MARCH 15, 2024')
        assert len(result) == 1

    def test_lowercase(self):
        """'march 15, 2024' should be parsed (case-insensitive)."""
        result = extract_explicit_dates('march 15, 2024')
        assert len(result) == 1

    def test_mixed_case(self):
        """'mArCh 15, 2024' should be parsed (case-insensitive)."""
        result = extract_explicit_dates('mArCh 15, 2024')
        assert len(result) == 1
