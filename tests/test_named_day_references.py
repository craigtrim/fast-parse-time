#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for named day references like yesterday, tomorrow, today."""

import pytest
from fast_parse_time import parse_time_references


class TestYesterday:
    """Tests for 'yesterday' patterns."""

    def test_yesterday(self):
        """'yesterday' should resolve to 1 day in the past."""
        result = parse_time_references('yesterday')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_yesterday_in_sentence(self):
        """'yesterday' in a sentence should be extracted."""
        result = parse_time_references('I saw this yesterday')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_yesterday_uppercase(self):
        """'YESTERDAY' should work (case-insensitive)."""
        result = parse_time_references('YESTERDAY')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'


class TestTomorrow:
    """Tests for 'tomorrow' patterns."""

    def test_tomorrow(self):
        """'tomorrow' should resolve to 1 day in the future."""
        result = parse_time_references('tomorrow')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'future'

    def test_tomorrow_in_sentence(self):
        """'tomorrow' in a sentence should be extracted."""
        result = parse_time_references("let's meet tomorrow")
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'future'

    def test_tomorrow_mixed_case(self):
        """'Tomorrow' should work (case-insensitive)."""
        result = parse_time_references('Tomorrow')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'future'


class TestToday:
    """Tests for 'today' patterns."""

    def test_today(self):
        """'today' should resolve to 0 days."""
        result = parse_time_references('today')
        assert len(result) == 1
        assert result[0].cardinality == 0
        assert result[0].frame == 'day'

    def test_today_in_sentence(self):
        """'today' in a sentence should be extracted."""
        result = parse_time_references('what happened today')
        assert len(result) == 1
        assert result[0].cardinality == 0
        assert result[0].frame == 'day'

    def test_today_uppercase(self):
        """'TODAY' should work (case-insensitive)."""
        result = parse_time_references('TODAY')
        assert len(result) == 1
        assert result[0].cardinality == 0
        assert result[0].frame == 'day'


class TestTenseHandling:
    """Tests for tense handling."""

    def test_today_has_present_tense(self):
        """'today' should have present tense."""
        result = parse_time_references('today')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_yesterday_has_past_tense(self):
        """'yesterday' should have past tense."""
        result = parse_time_references('yesterday')
        assert len(result) == 1
        assert result[0].tense == 'past'

    def test_tomorrow_has_future_tense(self):
        """'tomorrow' should have future tense."""
        result = parse_time_references('tomorrow')
        assert len(result) == 1
        assert result[0].tense == 'future'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
