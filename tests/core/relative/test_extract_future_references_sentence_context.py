#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for extract_future_references function."""

import pytest
from fast_parse_time import extract_future_references, RelativeTime

class TestSentenceContext:
    """Tests for patterns in sentence context."""

    def test_next_week_in_sentence(self):
        """'next week' in a sentence should be extracted."""
        result = extract_future_references('please schedule a review for next week')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'future'

    def test_next_month_in_sentence(self):
        """'next month' in a sentence should be extracted."""
        result = extract_future_references("let's revisit this next month")
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'month'
        assert result[0].tense == 'future'
