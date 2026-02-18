#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for indefinite articles (a/an) as cardinality."""

import pytest
from fast_parse_time import parse_time_references

class TestIndefiniteArticleFuturePatterns:
    """Tests for 'a X from now' and 'an X from now' patterns (future tense)."""

    def test_a_week_from_now(self):
        """'a week from now' should imply cardinality of 1, frame week, tense future."""
        result = parse_time_references('a week from now')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'future'

    def test_an_hour_from_now(self):
        """'an hour from now' should imply cardinality of 1, frame hour, tense future."""
        result = parse_time_references('an hour from now')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'future'
