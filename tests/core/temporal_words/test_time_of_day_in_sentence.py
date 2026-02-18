#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for time-of-day references."""

import pytest
from fast_parse_time import parse_dates

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
