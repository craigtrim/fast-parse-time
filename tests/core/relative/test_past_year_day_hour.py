#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for 'last X' and 'past X' without explicit cardinality."""

import pytest
from fast_parse_time import parse_time_references

class TestPastYearDayHour:
    """Tests for 'past year', 'past day', 'past hour' patterns."""

    def test_past_year(self):
        """'past year' should imply cardinality of 1 and frame of year."""
        result = parse_time_references('past year')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_past_day(self):
        """'past day' should imply cardinality of 1 and frame of day."""
        result = parse_time_references('past day')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_past_hour(self):
        """'past hour' should imply cardinality of 1 and frame of hour."""
        result = parse_time_references('past hour')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'
