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

class TestHasTemporalInfo:
    """Tests for has_temporal_info function edge cases."""

    def test_empty_string_is_false(self):
        """Empty string should return False."""
        assert has_temporal_info('') is False

    def test_plain_text_is_false(self):
        """Plain text without dates should return False."""
        assert has_temporal_info('Just a regular sentence about stuff') is False

    def test_explicit_date_is_true(self):
        """Text with explicit date should return True."""
        assert has_temporal_info('Meeting on 04/08/2024') is True

    def test_relative_time_is_true(self):
        """Text with relative time should return True."""
        assert has_temporal_info('5 days ago') is True

    def test_yesterday_is_true(self):
        """'yesterday' should return True."""
        assert has_temporal_info('I saw this yesterday') is True

    def test_last_week_is_true(self):
        """'last week' should return True."""
        assert has_temporal_info('show data from last week') is True

    def test_written_month_is_true(self):
        """Written month date should return True."""
        assert has_temporal_info('Meeting on March 15, 2024') is True

    def test_numbers_only_is_false(self):
        """Text with numbers but no dates should return False."""
        assert has_temporal_info('The answer is 42') is False
