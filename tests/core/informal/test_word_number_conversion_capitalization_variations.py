#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for word-to-number conversion in relative time expressions."""

import pytest
from fast_parse_time import parse_time_references

class TestCapitalizationVariations:
    """Tests for capitalization variations."""

    def test_one_week_ago_uppercase(self):
        """'ONE WEEK AGO' should work (case-insensitive)."""
        result = parse_time_references('ONE WEEK AGO')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_one_day_ago_mixed_case(self):
        """'One Day Ago' should work (case-insensitive)."""
        result = parse_time_references('One Day Ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'
