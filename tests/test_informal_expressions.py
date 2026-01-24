#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for informal time expressions."""

import pytest
from fast_parse_time import parse_time_references


class TestHalfAnHour:
    """Tests for 'half an hour' patterns."""

    def test_half_an_hour_ago(self):
        """'half an hour ago' should resolve to 30 minutes."""
        result = parse_time_references('half an hour ago')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_half_an_hour_from_now(self):
        """'half an hour from now' should resolve to 30 minutes."""
        result = parse_time_references('half an hour from now')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'minute'
        assert result[0].tense == 'future'

    def test_half_a_day_ago(self):
        """'half a day ago' should resolve to 12 hours."""
        result = parse_time_references('half a day ago')
        assert len(result) == 1
        assert result[0].cardinality == 12
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'


class TestSeveralPattern:
    """Tests for 'several X ago' patterns."""

    def test_several_weeks_ago(self):
        """'several weeks ago' should resolve to 3 weeks."""
        result = parse_time_references('several weeks ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_several_days_ago(self):
        """'several days ago' should resolve to 3 days."""
        result = parse_time_references('several days ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_several_months_ago(self):
        """'several months ago' should resolve to 3 months."""
        result = parse_time_references('several months ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_several_years_ago(self):
        """'several years ago' should resolve to 3 years."""
        result = parse_time_references('several years ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'


class TestFewPattern:
    """Tests for 'few X ago' patterns."""

    def test_few_days_ago(self):
        """'a few days ago' should resolve to 3 days."""
        result = parse_time_references('a few days ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_few_weeks_ago(self):
        """'a few weeks ago' should resolve to 3 weeks."""
        result = parse_time_references('a few weeks ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'


class TestCouplePattern:
    """Tests for 'couple' patterns (using KB patterns)."""

    def test_last_couple_days(self):
        """'last couple days' should resolve to 2 days."""
        result = parse_time_references('last couple days')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_last_couple_of_weeks(self):
        """'last couple of weeks' should resolve to 2 weeks."""
        result = parse_time_references('last couple of weeks')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_couple_of_weeks_ago(self):
        """'couple of weeks ago' should resolve to 2 weeks."""
        result = parse_time_references('couple of weeks ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'


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


class TestCapitalizationVariations:
    """Tests for capitalization variations."""

    def test_half_an_hour_uppercase(self):
        """'HALF AN HOUR AGO' should work (case-insensitive)."""
        result = parse_time_references('HALF AN HOUR AGO')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_several_weeks_mixed_case(self):
        """'Several Weeks Ago' should work (case-insensitive)."""
        result = parse_time_references('Several Weeks Ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
