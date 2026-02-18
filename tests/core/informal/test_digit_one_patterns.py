#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for word-to-number conversion in relative time expressions."""

import pytest
from fast_parse_time import parse_time_references

class TestDigitOnePatterns:
    """Tests for digit '1 X ago' patterns."""

    def test_1_week_ago(self):
        """'1 week ago' should work."""
        result = parse_time_references('1 week ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_1_day_ago(self):
        """'1 day ago' should work."""
        result = parse_time_references('1 day ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_1_month_ago(self):
        """'1 month ago' should work."""
        result = parse_time_references('1 month ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_1_year_ago(self):
        """'1 year ago' should work."""
        result = parse_time_references('1 year ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'
