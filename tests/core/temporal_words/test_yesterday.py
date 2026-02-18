#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for named day references like yesterday, tomorrow, today."""

import pytest
from fast_parse_time import parse_time_references

class TestYesterday:
    """Tests for 'yesterday' patterns."""

    def test_yesterday(self):
        """'yesterday' should resolve to 1 day in the past."""
        result = parse_time_references('yesterday')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_yesterday_in_sentence(self):
        """'yesterday' in a sentence should be extracted."""
        result = parse_time_references('I saw this yesterday')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_yesterday_uppercase(self):
        """'YESTERDAY' should work (case-insensitive)."""
        result = parse_time_references('YESTERDAY')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'
