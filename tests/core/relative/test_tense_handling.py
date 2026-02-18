#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for named day references like yesterday, tomorrow, today."""

import pytest
from fast_parse_time import parse_time_references

class TestTenseHandling:
    """Tests for tense handling."""

    def test_today_has_present_tense(self):
        """'today' should have present tense."""
        result = parse_time_references('today')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_yesterday_has_past_tense(self):
        """'yesterday' should have past tense."""
        result = parse_time_references('yesterday')
        assert len(result) == 1
        assert result[0].tense == 'past'

    def test_tomorrow_has_future_tense(self):
        """'tomorrow' should have future tense."""
        result = parse_time_references('tomorrow')
        assert len(result) == 1
        assert result[0].tense == 'future'
