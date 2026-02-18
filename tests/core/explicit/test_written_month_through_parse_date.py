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

class TestWrittenMonthThroughParseDate:
    """Tests for written month formats going through parse_dates."""

    def test_written_month_extracted(self):
        """Written month date should be in explicit_dates."""
        result = parse_dates('Meeting on March 15, 2024')
        assert len(result.explicit_dates) >= 1

    def test_written_month_has_dates(self):
        """Written month date should set has_dates True."""
        result = parse_dates('Meeting on March 15, 2024')
        assert result.has_dates is True

    def test_written_month_type(self):
        """Written month date should be classified as FULL_EXPLICIT_DATE."""
        result = parse_dates('Meeting on March 15, 2024')
        assert any(ed.date_type == 'FULL_EXPLICIT_DATE' for ed in result.explicit_dates)
