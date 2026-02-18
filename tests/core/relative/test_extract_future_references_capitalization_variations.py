#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for extract_future_references function."""

import pytest
from fast_parse_time import extract_future_references, RelativeTime

class TestCapitalizationVariations:
    """Tests for capitalization variations."""

    def test_next_week_uppercase(self):
        """'NEXT WEEK' should work (case-insensitive)."""
        result = extract_future_references('NEXT WEEK')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'future'

    def test_next_month_mixed_case(self):
        """'Next Month' should work (case-insensitive)."""
        result = extract_future_references('Next Month')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'month'
        assert result[0].tense == 'future'
