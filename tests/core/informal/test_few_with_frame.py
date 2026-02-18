#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for informal time expressions."""

import pytest
from fast_parse_time import parse_time_references

class TestFewWithFrame:
    """Tests for 'few X ago' with additional frames."""

    def test_few_hours_ago(self):
        """'a few hours ago' should resolve to 3 hours."""
        result = parse_time_references('a few hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_few_months_ago(self):
        """'a few months ago' should resolve to 3 months."""
        result = parse_time_references('a few months ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_few_years_ago(self):
        """'a few years ago' should resolve to 3 years."""
        result = parse_time_references('a few years ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'
