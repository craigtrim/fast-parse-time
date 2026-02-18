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

class TestEmptyAndNoContent:
    """Tests for empty string and text with no temporal content."""

    def test_empty_string_returns_parse_result(self):
        """Empty string should return a ParseResult, not None or raise."""
        result = parse_dates('')
        assert isinstance(result, ParseResult)

    def test_empty_string_has_no_explicit_dates(self):
        """Empty string should yield no explicit dates."""
        result = parse_dates('')
        assert result.explicit_dates == []

    def test_empty_string_has_no_relative_times(self):
        """Empty string should yield no relative times."""
        result = parse_dates('')
        assert result.relative_times == []

    def test_empty_string_has_dates_is_false(self):
        """Empty string should have has_dates == False."""
        result = parse_dates('')
        assert result.has_dates is False

    def test_no_temporal_text_returns_parse_result(self):
        """Text with no dates should return a ParseResult."""
        result = parse_dates('Hello world, this is just text')
        assert isinstance(result, ParseResult)

    def test_no_temporal_text_has_no_dates(self):
        """Text with no dates should have empty lists."""
        result = parse_dates('Hello world, this is just text')
        assert result.explicit_dates == []
        assert result.relative_times == []

    def test_no_temporal_text_has_dates_is_false(self):
        """Text with no dates should have has_dates == False."""
        result = parse_dates('Hello world, this is just text')
        assert result.has_dates is False
