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

class TestBothTypes:
    """Tests for text with both explicit dates and relative times."""

    def test_both_types_has_dates_is_true(self):
        """Text with both types should have has_dates == True."""
        result = parse_dates('Meeting on 04/08/2024 about issues from 5 days ago')
        assert result.has_dates is True

    def test_both_types_explicit_dates_count(self):
        """Should have one explicit date."""
        result = parse_dates('Meeting on 04/08/2024 about issues from 5 days ago')
        assert len(result.explicit_dates) == 1

    def test_both_types_relative_times_count(self):
        """Should have one relative time."""
        result = parse_dates('Meeting on 04/08/2024 about issues from 5 days ago')
        assert len(result.relative_times) == 1

    def test_both_types_explicit_date_value(self):
        """Explicit date text should be correct."""
        result = parse_dates('Meeting on 04/08/2024 about issues from 5 days ago')
        assert result.explicit_dates[0].text == '04/08/2024'

    def test_both_types_relative_time_values(self):
        """Relative time values should be correct."""
        result = parse_dates('Meeting on 04/08/2024 about issues from 5 days ago')
        rt = result.relative_times[0]
        assert rt.cardinality == 5
        assert rt.frame == 'day'
        assert rt.tense == 'past'
