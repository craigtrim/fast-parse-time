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
