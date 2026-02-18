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


class TestYesterdayPositionVariations:
    """Tests for 'yesterday' at different positions within a sentence."""

    def test_yesterday_at_end_of_sentence(self):
        """'yesterday' at the end of a sentence should be extracted."""
        result = parse_time_references('the meeting was held yesterday')
        assert len(result) == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_yesterday_at_start_of_sentence(self):
        """'yesterday' at the start of a sentence should be extracted."""
        result = parse_time_references('yesterday the system crashed')
        assert len(result) == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_yesterday_mid_sentence(self):
        """'yesterday' in the middle of a sentence should be extracted."""
        result = parse_time_references('we noticed yesterday that performance dropped')
        assert len(result) == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'


class TestTodayPositionVariations:
    """Tests for 'today' at different positions within a sentence."""

    def test_today_at_start_of_sentence(self):
        """'today' at the start of a sentence should be extracted."""
        result = parse_time_references('today is the deadline')
        assert len(result) == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'present'

    def test_today_at_end_of_sentence(self):
        """'today' at the end of a sentence should be extracted."""
        result = parse_time_references('we need to finish today')
        assert len(result) == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'present'


class TestTomorrowPositionVariations:
    """Tests for 'tomorrow' at different positions and combinations."""

    def test_tomorrow_at_start_of_sentence(self):
        """'tomorrow' at the start of a sentence should be extracted."""
        result = parse_time_references('tomorrow we deploy the fix')
        assert len(result) == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'future'

    def test_tomorrow_morning_frame_and_tense(self):
        """'tomorrow morning' should still return frame=day and tense=future."""
        result = parse_time_references('the call is tomorrow morning')
        assert len(result) >= 1
        tomorrow_refs = [r for r in result if r.frame == 'day' and r.tense == 'future']
        assert len(tomorrow_refs) >= 1

    def test_tomorrow_at_end_of_sentence(self):
        """'tomorrow' at the end of a sentence should be extracted."""
        result = parse_time_references('can we reschedule for tomorrow')
        assert len(result) == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'future'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
