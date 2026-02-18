#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for indefinite articles (a/an) as cardinality."""

import pytest
from fast_parse_time import parse_time_references

class TestIndefiniteArticleA:
    """Tests for 'a X ago' patterns."""

    def test_a_week_ago(self):
        """'a week ago' should imply cardinality of 1."""
        result = parse_time_references('a week ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_a_day_ago(self):
        """'a day ago' should imply cardinality of 1."""
        result = parse_time_references('a day ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_a_month_ago(self):
        """'a month ago' should imply cardinality of 1."""
        result = parse_time_references('a month ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_a_year_ago(self):
        """'a year ago' should imply cardinality of 1."""
        result = parse_time_references('a year ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_a_minute_ago(self):
        """'a minute ago' should imply cardinality of 1."""
        result = parse_time_references('a minute ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_a_second_ago(self):
        """'a second ago' should imply cardinality of 1."""
        result = parse_time_references('a second ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'
