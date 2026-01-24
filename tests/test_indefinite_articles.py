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


class TestIndefiniteArticleAn:
    """Tests for 'an X ago' patterns."""

    def test_an_hour_ago(self):
        """'an hour ago' should imply cardinality of 1."""
        result = parse_time_references('an hour ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'


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


class TestCapitalizationVariations:
    """Tests for capitalization variations."""

    def test_a_week_ago_uppercase(self):
        """'A WEEK AGO' should work (case-insensitive)."""
        result = parse_time_references('A WEEK AGO')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_an_hour_ago_mixed_case(self):
        """'An Hour Ago' should work (case-insensitive)."""
        result = parse_time_references('An Hour Ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'


class TestBaselineComparison:
    """Baseline tests showing explicit number still works."""

    def test_1_week_ago_works(self):
        """Verify '1 week ago' still works (baseline)."""
        result = parse_time_references('1 week ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_one_hour_ago_works(self):
        """Verify 'one hour ago' still works (baseline)."""
        result = parse_time_references('one hour ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
