#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for word-to-number conversion in relative time expressions."""

import pytest
from fast_parse_time import parse_time_references

class TestWordNumberConversion:
    """Tests for basic word number patterns."""

    def test_two_days_ago(self):
        """Word number 'two' should convert to 2."""
        result = parse_time_references('two days ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_three_months_ago(self):
        """Word number 'three' should convert to 3."""
        result = parse_time_references('three months ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_five_hours_ago(self):
        """Word number 'five' should convert to 5."""
        result = parse_time_references('five hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_one_week_ago(self):
        """Word number 'one' should convert to 1."""
        result = parse_time_references('one week ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_one_day_ago(self):
        """Word number 'one' should convert to 1."""
        result = parse_time_references('one day ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'
