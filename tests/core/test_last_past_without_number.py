#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for 'last X' and 'past X' without explicit cardinality."""

import pytest
from fast_parse_time import parse_time_references


class TestLastWithoutNumber:
    """Tests for 'last' patterns without explicit number."""

    def test_last_week(self):
        """'last week' should imply cardinality of 1."""
        result = parse_time_references('last week')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_last_month(self):
        """'last month' should imply cardinality of 1."""
        result = parse_time_references('last month')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_last_day(self):
        """'last day' should imply cardinality of 1."""
        result = parse_time_references('last day')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_last_year(self):
        """'last year' should imply cardinality of 1."""
        result = parse_time_references('last year')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'


class TestPastWithoutNumber:
    """Tests for 'past' patterns without explicit number."""

    def test_past_week(self):
        """'past week' should imply cardinality of 1."""
        result = parse_time_references('past week')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_past_month(self):
        """'past month' should imply cardinality of 1."""
        result = parse_time_references('past month')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'


class TestSentenceContext:
    """Tests for patterns within sentence context."""

    def test_last_week_in_sentence(self):
        """'last week' in a sentence should be extracted."""
        result = parse_time_references('show me data from last week')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_last_month_in_question(self):
        """'last month' in a question should be extracted."""
        result = parse_time_references('what happened last month')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_past_week_in_sentence(self):
        """'past week' in a sentence should be extracted."""
        result = parse_time_references('activity in the past week')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_last_year_in_sentence(self):
        """'last year' in a sentence should be extracted."""
        result = parse_time_references('compare with last year')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'


class TestCapitalizationVariations:
    """Tests for capitalization variations."""

    def test_last_week_uppercase(self):
        """'LAST WEEK' should work (case-insensitive)."""
        result = parse_time_references('LAST WEEK')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_last_month_mixed_case(self):
        """'Last Month' should work (case-insensitive)."""
        result = parse_time_references('Last Month')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_past_week_title_case(self):
        """'Past Week' should work (case-insensitive)."""
        result = parse_time_references('Past Week')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'


class TestBaselineComparison:
    """Baseline tests showing explicit number still works."""

    def test_last_1_week_works(self):
        """Verify 'last 1 week' still works (baseline)."""
        result = parse_time_references('last 1 week')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_next_week_works(self):
        """Verify 'next week' still works (shows symmetry)."""
        result = parse_time_references('next week')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'future'

    def test_last_2_weeks_works(self):
        """Verify 'last 2 weeks' still works."""
        result = parse_time_references('last 2 weeks')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'


class TestPossessiveForms:
    """Tests for possessive forms."""

    def test_last_weeks_possessive(self):
        """'last week's' should work."""
        result = parse_time_references("last week's data")
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_last_months_possessive(self):
        """'last month's' should work."""
        result = parse_time_references("last month's report")
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
