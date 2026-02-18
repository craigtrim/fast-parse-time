#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for named day references like yesterday, tomorrow, today."""

import pytest
from fast_parse_time import parse_time_references

class TestTodayPositionVariations:
    """Tests for 'today' at different positions within a sentence."""

    def test_today_at_start_of_sentence(self):
        """'today' at the start of a sentence should be extracted."""
        result = parse_time_references('today is the deadline')
        assert len(result) == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'present'

    def test_today_at_end_of_sentence(self):
        """'today' at the end of a sentence should be extracted."""
        result = parse_time_references('we need to finish today')
        assert len(result) == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'present'
