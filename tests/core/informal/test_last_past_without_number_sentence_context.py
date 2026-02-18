#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for 'last X' and 'past X' without explicit cardinality."""

import pytest
from fast_parse_time import parse_time_references

class TestSentenceContext:
    """Tests for patterns within sentence context."""

    def test_last_week_in_sentence(self):
        """'last week' in a sentence should be extracted."""
        result = parse_time_references('show me data from last week')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_last_month_in_question(self):
        """'last month' in a question should be extracted."""
        result = parse_time_references('what happened last month')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_past_week_in_sentence(self):
        """'past week' in a sentence should be extracted."""
        result = parse_time_references('activity in the past week')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_last_year_in_sentence(self):
        """'last year' in a sentence should be extracted."""
        result = parse_time_references('compare with last year')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'
