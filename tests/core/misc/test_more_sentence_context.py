#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for 'last X' and 'past X' without explicit cardinality."""

import pytest
from fast_parse_time import parse_time_references

class TestMoreSentenceContext:
    """Additional sentence context tests."""

    def test_last_day_in_sentence(self):
        """'last day' embedded in a sentence should be extracted."""
        result = parse_time_references('activity in the last day')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_last_hour_in_sentence(self):
        """'last hour' embedded in a sentence should be extracted."""
        result = parse_time_references('alerts from the last hour')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_past_month_in_sentence(self):
        """'past month' embedded in a sentence should be extracted."""
        result = parse_time_references('sales trends over the past month')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'
