#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for indefinite articles (a/an) as cardinality."""

import pytest
from fast_parse_time import parse_time_references

class TestCapitalizationVariations:
    """Tests for capitalization variations."""

    def test_a_week_ago_uppercase(self):
        """'A WEEK AGO' should work (case-insensitive)."""
        result = parse_time_references('A WEEK AGO')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_an_hour_ago_mixed_case(self):
        """'An Hour Ago' should work (case-insensitive)."""
        result = parse_time_references('An Hour Ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'
