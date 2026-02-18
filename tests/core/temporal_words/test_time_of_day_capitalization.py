#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for time-of-day references."""

import pytest
from fast_parse_time import parse_dates

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
