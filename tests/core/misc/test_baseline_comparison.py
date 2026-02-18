#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for 'last X' and 'past X' without explicit cardinality."""

import pytest
from fast_parse_time import parse_time_references

class TestBaselineComparison:
    """Baseline tests showing explicit number still works."""

    def test_last_1_week_works(self):
        """Verify 'last 1 week' still works (baseline)."""
        result = parse_time_references('last 1 week')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_next_week_works(self):
        """Verify 'next week' still works (shows symmetry)."""
        result = parse_time_references('next week')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'future'

    def test_last_2_weeks_works(self):
        """Verify 'last 2 weeks' still works."""
        result = parse_time_references('last 2 weeks')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'
