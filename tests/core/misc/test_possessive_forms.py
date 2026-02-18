#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for 'last X' and 'past X' without explicit cardinality."""

import pytest
from fast_parse_time import parse_time_references

class TestPossessiveForms:
    """Tests for possessive forms."""

    def test_last_weeks_possessive(self):
        """'last week's' should work."""
        result = parse_time_references("last week's data")
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_last_months_possessive(self):
        """'last month's' should work."""
        result = parse_time_references("last month's report")
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'
