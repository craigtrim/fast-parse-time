#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for time-of-day references."""

import pytest
from fast_parse_time import parse_dates

class TestMoreSentenceVariations:
    """More sentence variations for existing time-of-day patterns."""

    def test_this_morning_question(self):
        """'this morning' in a question should be extracted."""
        result = parse_dates('what happened this morning')
        assert result.has_dates is True

    def test_tonight_future_context(self):
        """'tonight' in a future context should be extracted."""
        result = parse_dates('can we review tonight')
        assert result.has_dates is True

    def test_last_night_question(self):
        """'last night' in a question should be extracted."""
        result = parse_dates('did you see what happened last night')
        assert result.has_dates is True

    def test_this_evening_question(self):
        """'this evening' in a question should be extracted."""
        result = parse_dates('are you free this evening')
        assert result.has_dates is True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
