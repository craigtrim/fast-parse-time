#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for 'last X' and 'past X' without explicit cardinality."""

import pytest
from fast_parse_time import parse_time_references

class TestCapitalizationVariations:
    """Tests for capitalization variations."""

    def test_last_week_uppercase(self):
        """'LAST WEEK' should work (case-insensitive)."""
        result = parse_time_references('LAST WEEK')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_last_month_mixed_case(self):
        """'Last Month' should work (case-insensitive)."""
        result = parse_time_references('Last Month')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_past_week_title_case(self):
        """'Past Week' should work (case-insensitive)."""
        result = parse_time_references('Past Week')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'
