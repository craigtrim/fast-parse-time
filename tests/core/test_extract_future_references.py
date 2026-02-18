#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for extract_future_references function."""

import pytest
from fast_parse_time import extract_future_references, RelativeTime


class TestNextWithoutNumber:
    """Tests for 'next X' patterns (implied cardinality of 1)."""

    def test_next_week(self):
        """'next week' should resolve to 1 week in the future."""
        result = extract_future_references('next week')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'future'

    def test_next_month(self):
        """'next month' should resolve to 1 month in the future."""
        result = extract_future_references('next month')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'month'
        assert result[0].tense == 'future'

    def test_next_year(self):
        """'next year' should resolve to 1 year in the future."""
        result = extract_future_references('next year')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'year'
        assert result[0].tense == 'future'


class TestTomorrow:
    """Tests for 'tomorrow' as a future reference."""

    def test_tomorrow(self):
        """'tomorrow' should be returned as a future reference."""
        result = extract_future_references('tomorrow')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'future'

    def test_tomorrow_in_sentence(self):
        """'tomorrow' in a sentence should be extracted."""
        result = extract_future_references("let's meet tomorrow")
        assert len(result) == 1
        assert result[0].tense == 'future'


class TestFromNowPatterns:
    """Tests for 'X from now' patterns."""

    def test_half_an_hour_from_now(self):
        """'half an hour from now' should resolve to 30 minutes in the future."""
        result = extract_future_references('half an hour from now')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'minute'
        assert result[0].tense == 'future'


class TestReturnType:
    """Tests for correct return types."""

    def test_returns_list(self):
        """Function should always return a list."""
        result = extract_future_references('next week')
        assert isinstance(result, list)

    def test_returns_relative_time_objects(self):
        """Items in list should be RelativeTime instances."""
        result = extract_future_references('next week')
        assert len(result) == 1
        assert isinstance(result[0], RelativeTime)

    def test_empty_on_no_temporal(self):
        """Text with no temporal info should return empty list."""
        result = extract_future_references('Hello world')
        assert result == []

    def test_empty_on_empty_string(self):
        """Empty string should return empty list."""
        result = extract_future_references('')
        assert result == []


class TestFilteringBehavior:
    """Tests that only future references are returned (past excluded)."""

    def test_excludes_past_references(self):
        """Past references should not appear in future results."""
        result = extract_future_references('5 days ago')
        assert result == []

    def test_excludes_yesterday(self):
        """'yesterday' (past) should be excluded."""
        result = extract_future_references('yesterday')
        assert result == []

    def test_mixed_only_returns_future(self):
        """Mixed past/future text should only return future references."""
        result = extract_future_references('show data from last week and next week')
        assert len(result) == 1
        assert result[0].tense == 'future'
        assert result[0].frame == 'week'


class TestSentenceContext:
    """Tests for patterns in sentence context."""

    def test_next_week_in_sentence(self):
        """'next week' in a sentence should be extracted."""
        result = extract_future_references('please schedule a review for next week')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'future'

    def test_next_month_in_sentence(self):
        """'next month' in a sentence should be extracted."""
        result = extract_future_references("let's revisit this next month")
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'month'
        assert result[0].tense == 'future'


class TestCapitalizationVariations:
    """Tests for capitalization variations."""

    def test_next_week_uppercase(self):
        """'NEXT WEEK' should work (case-insensitive)."""
        result = extract_future_references('NEXT WEEK')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'future'

    def test_next_month_mixed_case(self):
        """'Next Month' should work (case-insensitive)."""
        result = extract_future_references('Next Month')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'month'
        assert result[0].tense == 'future'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
