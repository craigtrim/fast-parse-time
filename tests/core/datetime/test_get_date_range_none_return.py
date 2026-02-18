#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for get_date_range function."""

import pytest
from datetime import datetime
from fast_parse_time import get_date_range

class TestGetDateRangeNoneReturn:
    """Tests for cases where get_date_range returns None."""

    def test_single_reference_returns_none(self):
        """A single time reference should return None (need exactly 2)."""
        result = get_date_range('5 days ago')
        assert result is None

    def test_no_references_returns_none(self):
        """Text with no temporal references should return None."""
        result = get_date_range('Hello world')
        assert result is None

    def test_empty_string_returns_none(self):
        """Empty string should return None."""
        result = get_date_range('')
        assert result is None
