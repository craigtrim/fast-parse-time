#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Edge case tests for parse_dates and related functions."""

import pytest
from fast_parse_time import (
    parse_dates,
    has_temporal_info,
    ParseResult,
    ExplicitDate,
    RelativeTime,
)

class TestMoreHasTemporalInfoVariants:
    """Additional has_temporal_info variant tests."""

    def test_tomorrow_is_true(self):
        """'tomorrow' should return True."""
        assert has_temporal_info('tomorrow') is True

    def test_next_week_is_true(self):
        """'next week' should return True."""
        assert has_temporal_info('next week') is True

    def test_numeric_date_is_true(self):
        """A numeric date string should return True."""
        assert has_temporal_info('04/08/2024') is True

    def test_random_words_is_false(self):
        """Sentence with no temporal references should return False."""
        assert has_temporal_info('the quick brown fox') is False


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
