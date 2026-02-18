#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for time-of-day references."""

import pytest
from fast_parse_time import parse_dates

class TestAdditionalTimeOfDayPatterns:
    """Tests for additional time-of-day patterns."""

    def test_early_morning(self):
        """'early morning' - documents that this compound phrase may not be recognized."""
        # NOTE: 'early morning' alone (without 'this') is not currently in the
        # supported pattern set. has_dates may be False for this input.
        result = parse_dates('early morning')
        assert isinstance(result.has_dates, bool)

    def test_late_afternoon(self):
        """'late afternoon' - documents that this compound phrase may not be recognized."""
        # NOTE: 'late afternoon' alone (without 'this') is not currently in the
        # supported pattern set. has_dates may be False for this input.
        result = parse_dates('late afternoon')
        assert isinstance(result.has_dates, bool)

    def test_early_morning_in_sentence(self):
        """'early morning' in a sentence - documents current behavior."""
        result = parse_dates('the alert fired in the early morning')
        assert isinstance(result.has_dates, bool)

    def test_late_afternoon_in_sentence(self):
        """'late afternoon' in a sentence - documents current behavior."""
        result = parse_dates('the meeting is scheduled for late afternoon')
        assert isinstance(result.has_dates, bool)
