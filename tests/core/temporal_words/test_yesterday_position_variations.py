#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for named day references like yesterday, tomorrow, today."""

import pytest
from fast_parse_time import parse_time_references

class TestYesterdayPositionVariations:
    """Tests for 'yesterday' at different positions within a sentence."""

    def test_yesterday_at_end_of_sentence(self):
        """'yesterday' at the end of a sentence should be extracted."""
        result = parse_time_references('the meeting was held yesterday')
        assert len(result) == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_yesterday_at_start_of_sentence(self):
        """'yesterday' at the start of a sentence should be extracted."""
        result = parse_time_references('yesterday the system crashed')
        assert len(result) == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_yesterday_mid_sentence(self):
        """'yesterday' in the middle of a sentence should be extracted."""
        result = parse_time_references('we noticed yesterday that performance dropped')
        assert len(result) == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'
