#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for named day references like yesterday, tomorrow, today."""

import pytest
from fast_parse_time import parse_time_references

class TestToday:
    """Tests for 'today' patterns."""

    def test_today(self):
        """'today' should resolve to 0 days."""
        result = parse_time_references('today')
        assert len(result) == 1
        assert result[0].cardinality == 0
        assert result[0].frame == 'day'

    def test_today_in_sentence(self):
        """'today' in a sentence should be extracted."""
        result = parse_time_references('what happened today')
        assert len(result) == 1
        assert result[0].cardinality == 0
        assert result[0].frame == 'day'

    def test_today_uppercase(self):
        """'TODAY' should work (case-insensitive)."""
        result = parse_time_references('TODAY')
        assert len(result) == 1
        assert result[0].cardinality == 0
        assert result[0].frame == 'day'
