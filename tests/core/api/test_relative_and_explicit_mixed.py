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

class TestRelativeAndExplicitMixed:
    """Tests for a relative time and explicit date in the same sentence."""

    def test_relative_and_explicit_has_dates(self):
        """Sentence with both a relative time and an explicit date should have_dates True."""
        result = parse_dates('set deadline 04/15/2024 based on data from 30 days ago')
        assert result.has_dates is True

    def test_relative_and_explicit_both_extracted(self):
        """Both the explicit date and relative time should be extracted."""
        result = parse_dates('set deadline 04/15/2024 based on data from 30 days ago')
        assert len(result.explicit_dates) >= 1
        assert len(result.relative_times) >= 1
