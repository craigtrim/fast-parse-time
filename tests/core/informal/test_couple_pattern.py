#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for informal time expressions."""

import pytest
from fast_parse_time import parse_time_references

class TestCouplePattern:
    """Tests for 'couple' patterns (using KB patterns)."""

    def test_last_couple_days(self):
        """'last couple days' should resolve to 2 days."""
        result = parse_time_references('last couple days')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_last_couple_of_weeks(self):
        """'last couple of weeks' should resolve to 2 weeks."""
        result = parse_time_references('last couple of weeks')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_couple_of_weeks_ago(self):
        """'couple of weeks ago' should resolve to 2 weeks."""
        result = parse_time_references('couple of weeks ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'
