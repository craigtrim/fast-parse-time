#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for written month name formats in explicit dates."""

import pytest
from fast_parse_time import extract_explicit_dates

class TestDateWithoutComma:
    """Tests for dates with no comma between month+day and year."""

    def test_no_comma_month_day_year(self):
        """Date without comma between day and year should still parse."""
        result = extract_explicit_dates('March 15 2024')
        assert len(result) == 1

    def test_no_comma_abbreviated(self):
        """Abbreviated month date without comma should still parse."""
        result = extract_explicit_dates('Jan 1 2024')
        assert len(result) == 1
