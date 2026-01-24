#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for time-of-day references."""

import pytest
from fast_parse_time import parse_dates


class TestTimeOfDayReferences:
    """Tests for time-of-day references like 'this morning', 'tonight'."""

    def test_this_morning(self):
        """'this morning' should be recognized as temporal reference."""
        result = parse_dates('this morning')
        assert result.has_dates is True

    def test_tonight(self):
        """'tonight' should be recognized as temporal reference."""
        result = parse_dates('tonight')
        assert result.has_dates is True

    def test_this_afternoon(self):
        """'this afternoon' should be recognized as temporal reference."""
        result = parse_dates('this afternoon')
        assert result.has_dates is True

    def test_this_evening(self):
        """'this evening' should be recognized as temporal reference."""
        result = parse_dates('this evening')
        assert result.has_dates is True

    def test_last_night(self):
        """'last night' should be recognized as temporal reference."""
        result = parse_dates('last night')
        assert result.has_dates is True


class TestTimeOfDayInSentence:
    """Tests for time-of-day patterns within sentences."""

    def test_this_morning_in_sentence(self):
        """'this morning' in a sentence should be extracted."""
        result = parse_dates('I saw him this morning')
        assert result.has_dates is True

    def test_tonight_in_sentence(self):
        """'tonight' in a sentence should be extracted."""
        result = parse_dates("let's meet tonight")
        assert result.has_dates is True

    def test_this_afternoon_in_sentence(self):
        """'this afternoon' in a sentence should be extracted."""
        result = parse_dates('call me this afternoon')
        assert result.has_dates is True

    def test_last_night_in_sentence(self):
        """'last night' in a sentence should be extracted."""
        result = parse_dates('I worked late last night')
        assert result.has_dates is True


class TestTimeOfDayCapitalization:
    """Tests for capitalization variations."""

    def test_this_morning_uppercase(self):
        """'THIS MORNING' should work (case-insensitive)."""
        result = parse_dates('THIS MORNING')
        assert result.has_dates is True

    def test_tonight_mixed_case(self):
        """'Tonight' should work (case-insensitive)."""
        result = parse_dates('Tonight')
        assert result.has_dates is True

    def test_this_afternoon_uppercase(self):
        """'THIS AFTERNOON' should work (case-insensitive)."""
        result = parse_dates('THIS AFTERNOON')
        assert result.has_dates is True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
