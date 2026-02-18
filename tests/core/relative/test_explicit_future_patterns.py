#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for extract_future_references function."""

import pytest
from fast_parse_time import extract_future_references, RelativeTime

class TestExplicitFuturePatterns:
    """Tests for explicit future-tense patterns using digits."""

    def test_in_5_minutes(self):
        """'in 5 minutes' should resolve to cardinality 5, frame minute, tense future."""
        result = extract_future_references('in 5 minutes')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'minute'
        assert result[0].tense == 'future'

    def test_in_3_hours(self):
        """'in 3 hours' should resolve to cardinality 3, frame hour, tense future."""
        result = extract_future_references('in 3 hours')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'hour'
        assert result[0].tense == 'future'

    def test_7_days_from_now(self):
        """'7 days from now' should resolve to cardinality 7, frame day, tense future."""
        result = extract_future_references('7 days from now')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'day'
        assert result[0].tense == 'future'

    def test_2_weeks_from_now(self):
        """'2 weeks from now' should resolve to cardinality 2, frame week, tense future."""
        result = extract_future_references('2 weeks from now')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'week'
        assert result[0].tense == 'future'

    def test_in_6_months(self):
        """'in 6 months' should resolve to cardinality 6, frame month, tense future."""
        result = extract_future_references('in 6 months')
        assert len(result) == 1
        assert result[0].cardinality == 6
        assert result[0].frame == 'month'
        assert result[0].tense == 'future'

    def test_next_day(self):
        """'next day' should resolve to cardinality 1, frame day, tense future."""
        result = extract_future_references('next day')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'future'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
