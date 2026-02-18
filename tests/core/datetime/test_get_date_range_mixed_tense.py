#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for get_date_range function."""

import pytest
from datetime import datetime
from fast_parse_time import get_date_range

class TestGetDateRangeMixedTense:
    """Tests for mixed tense (past and future) date ranges."""

    def test_past_and_future_returns_tuple(self):
        """One past and one future reference should form a valid range."""
        result = get_date_range('last week and next week')
        assert result is not None
        assert isinstance(result, tuple)

    def test_past_and_future_ordering(self):
        """Past should be the start, future should be the end."""
        result = get_date_range('last week and next week')
        assert result is not None
        start, end = result
        assert start < end
