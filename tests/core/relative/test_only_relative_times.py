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

class TestOnlyRelativeTimes:
    """Tests for text containing only relative time references."""

    def test_only_relative_time_has_dates_is_true(self):
        """Text with only a relative time should have has_dates == True."""
        result = parse_dates('5 days ago')
        assert result.has_dates is True

    def test_only_relative_time_has_no_explicit_dates(self):
        """Text with only a relative time should have no explicit dates."""
        result = parse_dates('5 days ago')
        assert result.explicit_dates == []

    def test_only_relative_time_has_one_relative(self):
        """Text with one relative time should have one entry."""
        result = parse_dates('5 days ago')
        assert len(result.relative_times) == 1

    def test_relative_time_type(self):
        """Relative time should be a RelativeTime instance."""
        result = parse_dates('5 days ago')
        assert isinstance(result.relative_times[0], RelativeTime)

    def test_relative_time_cardinality(self):
        """Relative time cardinality should be correct."""
        result = parse_dates('5 days ago')
        assert result.relative_times[0].cardinality == 5

    def test_relative_time_frame(self):
        """Relative time frame should be correct."""
        result = parse_dates('5 days ago')
        assert result.relative_times[0].frame == 'day'

    def test_relative_time_tense(self):
        """Relative time tense should be correct."""
        result = parse_dates('5 days ago')
        assert result.relative_times[0].tense == 'past'
