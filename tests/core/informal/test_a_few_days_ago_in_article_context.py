#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for indefinite articles (a/an) as cardinality."""

import pytest
from fast_parse_time import parse_time_references

class TestAFewDaysAgoInArticleContext:
    """Tests for 'a few days ago' which starts with the indefinite article 'a'."""

    def test_a_few_days_ago(self):
        """'a few days ago' should resolve to 3 days in the past."""
        result = parse_time_references('a few days ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_a_few_weeks_ago(self):
        """'a few weeks ago' should resolve to 3 weeks in the past."""
        result = parse_time_references('a few weeks ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'
