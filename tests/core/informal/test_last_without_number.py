#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for 'last X' and 'past X' without explicit cardinality."""

import pytest
from fast_parse_time import parse_time_references

class TestLastWithoutNumber:
    """Tests for 'last' patterns without explicit number."""

    def test_last_week(self):
        """'last week' should imply cardinality of 1."""
        result = parse_time_references('last week')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_last_month(self):
        """'last month' should imply cardinality of 1."""
        result = parse_time_references('last month')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_last_day(self):
        """'last day' should imply cardinality of 1."""
        result = parse_time_references('last day')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_last_year(self):
        """'last year' should imply cardinality of 1."""
        result = parse_time_references('last year')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'
