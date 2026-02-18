#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for word-to-number conversion in relative time expressions."""

import pytest
from fast_parse_time import parse_time_references

class TestSentenceContext:
    """Tests for word numbers in sentence context."""

    def test_one_week_ago_in_sentence(self):
        """'one week ago' in a sentence should be extracted."""
        result = parse_time_references('I saw this one week ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_one_day_ago_in_sentence(self):
        """'one day ago' in a sentence should be extracted."""
        result = parse_time_references('the event happened one day ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'
