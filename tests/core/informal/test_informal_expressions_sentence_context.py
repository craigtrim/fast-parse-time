#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for informal time expressions."""

import pytest
from fast_parse_time import parse_time_references

class TestSentenceContext:
    """Tests for patterns within sentence context."""

    def test_half_an_hour_in_sentence(self):
        """'half an hour ago' in a sentence should be extracted."""
        result = parse_time_references('I called her half an hour ago')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_several_weeks_in_sentence(self):
        """'several weeks ago' in a sentence should be extracted."""
        result = parse_time_references('this happened several weeks ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'
