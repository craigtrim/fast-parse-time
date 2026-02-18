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

class TestWhitespaceAndNoDateStrings:
    """Tests for whitespace-only and numbers-only strings."""

    def test_whitespace_only_string(self):
        """Whitespace-only string should return a ParseResult with no dates."""
        result = parse_dates('   ')
        assert isinstance(result, ParseResult)
        assert result.has_dates is False

    def test_whitespace_only_has_temporal_info_false(self):
        """Whitespace-only string should return False from has_temporal_info."""
        assert has_temporal_info('   ') is False

    def test_numbers_only_no_dates(self):
        """String with only numbers (no date format) should have no dates."""
        result = parse_dates('42 100 999')
        assert result.has_dates is False

    def test_numbers_only_has_temporal_info_false(self):
        """String with only unstructured numbers should return False."""
        assert has_temporal_info('42 100 999') is False
