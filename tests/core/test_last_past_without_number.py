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


class TestLastHourMinuteSecond:
    """Tests for 'last hour', 'last minute', 'last second' patterns."""

    def test_last_hour(self):
        """'last hour' should imply cardinality of 1 and frame of hour."""
        result = parse_time_references('last hour')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_last_minute(self):
        """'last minute' should imply cardinality of 1 and frame of minute."""
        result = parse_time_references('last minute')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_last_second(self):
        """'last second' should imply cardinality of 1 and frame of second."""
        result = parse_time_references('last second')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'


class TestPastYearDayHour:
    """Tests for 'past year', 'past day', 'past hour' patterns."""

    def test_past_year(self):
        """'past year' should imply cardinality of 1 and frame of year."""
        result = parse_time_references('past year')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_past_day(self):
        """'past day' should imply cardinality of 1 and frame of day."""
        result = parse_time_references('past day')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_past_hour(self):
        """'past hour' should imply cardinality of 1 and frame of hour."""
        result = parse_time_references('past hour')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'


class TestMoreSentenceContext:
    """Additional sentence context tests."""

    def test_last_day_in_sentence(self):
        """'last day' embedded in a sentence should be extracted."""
        result = parse_time_references('activity in the last day')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_last_hour_in_sentence(self):
        """'last hour' embedded in a sentence should be extracted."""
        result = parse_time_references('alerts from the last hour')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_past_month_in_sentence(self):
        """'past month' embedded in a sentence should be extracted."""
        result = parse_time_references('sales trends over the past month')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'


class TestMoreCapitalizationVariants:
    """Additional capitalization variant tests."""

    def test_last_year_uppercase(self):
        """'LAST YEAR' should work (case-insensitive)."""
        result = parse_time_references('LAST YEAR')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_last_day_mixed_case(self):
        """'Last Day' should work (case-insensitive)."""
        result = parse_time_references('Last Day')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_past_year_title_case(self):
        """'Past Year' should work (case-insensitive)."""
        result = parse_time_references('Past Year')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
