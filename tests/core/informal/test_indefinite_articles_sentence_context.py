#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for indefinite articles (a/an) as cardinality."""

import pytest
from fast_parse_time import parse_time_references

class TestSentenceContext:
    """Tests for patterns within sentence context."""

    def test_a_week_ago_in_sentence(self):
        """'a week ago' in a sentence should be extracted."""
        result = parse_time_references('I saw this a week ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_a_day_ago_in_sentence(self):
        """'a day ago' in a sentence should be extracted."""
        result = parse_time_references('the event happened a day ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_an_hour_ago_in_sentence(self):
        """'an hour ago' in a sentence should be extracted."""
        result = parse_time_references('she called an hour ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'
