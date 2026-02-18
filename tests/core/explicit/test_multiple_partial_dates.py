#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for parse_dates_with_type function."""

import pytest
from fast_parse_time import parse_dates_with_type

class TestMultiplePartialDates:
    """Tests for multiple partial dates."""

    def test_multiple_month_day_dates(self):
        """Multiple MONTH_DAY partial dates should all be returned with no filter."""
        result = parse_dates_with_type('Mark 3/15 and 7/24 on the calendar')
        assert '3/15' in result
        assert '7/24' in result

    def test_partial_date_filter_multiple(self):
        """MONTH_DAY filter with multiple partial dates should return all matching."""
        result = parse_dates_with_type('Schedule 3/15 or 7/24', 'MONTH_DAY')
        assert len(result) == 2
