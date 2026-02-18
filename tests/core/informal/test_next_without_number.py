#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for extract_future_references function."""

import pytest
from fast_parse_time import extract_future_references, RelativeTime

class TestNextWithoutNumber:
    """Tests for 'next X' patterns (implied cardinality of 1)."""

    def test_next_week(self):
        """'next week' should resolve to 1 week in the future."""
        result = extract_future_references('next week')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'future'

    def test_next_month(self):
        """'next month' should resolve to 1 month in the future."""
        result = extract_future_references('next month')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'month'
        assert result[0].tense == 'future'

    def test_next_year(self):
        """'next year' should resolve to 1 year in the future."""
        result = extract_future_references('next year')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'year'
        assert result[0].tense == 'future'
