#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for word-to-number conversion in relative time expressions."""

import pytest
from fast_parse_time import parse_time_references

class TestOnePatternVariations:
    """Tests for 'one X ago' pattern variations."""

    def test_one_month_ago(self):
        """'one month ago' should work."""
        result = parse_time_references('one month ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_one_year_ago(self):
        """'one year ago' should work."""
        result = parse_time_references('one year ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_one_hour_ago(self):
        """'one hour ago' should work."""
        result = parse_time_references('one hour ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_one_minute_ago(self):
        """'one minute ago' should work."""
        result = parse_time_references('one minute ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_one_second_ago(self):
        """'one second ago' should work."""
        result = parse_time_references('one second ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'
