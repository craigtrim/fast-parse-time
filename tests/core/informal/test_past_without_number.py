#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for 'last X' and 'past X' without explicit cardinality."""

import pytest
from fast_parse_time import parse_time_references

class TestPastWithoutNumber:
    """Tests for 'past' patterns without explicit number."""

    def test_past_week(self):
        """'past week' should imply cardinality of 1."""
        result = parse_time_references('past week')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_past_month(self):
        """'past month' should imply cardinality of 1."""
        result = parse_time_references('past month')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'
