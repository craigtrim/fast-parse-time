#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for get_date_range function."""

import pytest
from datetime import datetime
from fast_parse_time import get_date_range

class TestGetDateRangeBasic:
    """Tests for basic get_date_range behavior."""

    def test_two_past_references_returns_tuple(self):
        """Two past references should return a (start, end) tuple."""
        result = get_date_range('show data from 7 days ago and 3 days ago')
        assert result is not None
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_two_past_references_ordering(self):
        """Returned tuple should be (earlier, later) regardless of text order."""
        result = get_date_range('show data from 7 days ago and 3 days ago')
        assert result is not None
        start, end = result
        assert start < end

    def test_start_is_datetime(self):
        """Start of range should be a datetime object."""
        result = get_date_range('from 7 days ago to 3 days ago')
        assert result is not None
        start, _ = result
        assert isinstance(start, datetime)

    def test_end_is_datetime(self):
        """End of range should be a datetime object."""
        result = get_date_range('from 7 days ago to 3 days ago')
        assert result is not None
        _, end = result
        assert isinstance(end, datetime)
