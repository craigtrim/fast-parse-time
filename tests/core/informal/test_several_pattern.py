#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for informal time expressions."""

import pytest
from fast_parse_time import parse_time_references

class TestSeveralPattern:
    """Tests for 'several X ago' patterns."""

    def test_several_weeks_ago(self):
        """'several weeks ago' should resolve to 3 weeks."""
        result = parse_time_references('several weeks ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_several_days_ago(self):
        """'several days ago' should resolve to 3 days."""
        result = parse_time_references('several days ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_several_months_ago(self):
        """'several months ago' should resolve to 3 months."""
        result = parse_time_references('several months ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_several_years_ago(self):
        """'several years ago' should resolve to 3 years."""
        result = parse_time_references('several years ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'
