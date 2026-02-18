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

class TestMultipleRelativeTimes:
    """Tests for multiple relative time expressions in one sentence."""

    def test_two_relative_times_in_sentence(self):
        """Two relative time references in one sentence should both be extracted."""
        result = parse_dates('data from 7 days ago and 3 days ago')
        assert result.has_dates is True
        assert len(result.relative_times) == 2

    def test_two_relative_times_cardinalities(self):
        """Both relative time cardinalities should be correct."""
        result = parse_dates('data from 7 days ago and 3 days ago')
        cardinalities = {rt.cardinality for rt in result.relative_times}
        assert 7 in cardinalities
        assert 3 in cardinalities
