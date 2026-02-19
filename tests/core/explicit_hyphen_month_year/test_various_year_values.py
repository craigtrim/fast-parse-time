#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
TDD tests for issue #21: abbreviated month-year format with hyphen delimiter.

Covers forward (MONTH_YEAR) and reversed (YEAR_MONTH) patterns for both
abbreviated and full month names, with 2-digit and 4-digit years.

Related GitHub Issue:
    #21 - Gap: abbreviated month-year format not supported (Oct-23, May-23)
    https://github.com/craigtrim/fast-parse-time/issues/21
"""

import pytest
from fast_parse_time import extract_explicit_dates


# ---------------------------------------------------------------------------
# 1. Abbreviated month + hyphen + 2-digit year → MONTH_YEAR (12 tests)
# ---------------------------------------------------------------------------


class TestVariousYearValues:
    """Confirm multiple distinct year values resolve correctly."""

    def test_year_2010(self):
        result = extract_explicit_dates('Oct-2010')
        assert len(result) >= 1

    def test_year_2015(self):
        result = extract_explicit_dates('Mar-2015')
        assert len(result) >= 1

    def test_year_2020(self):
        result = extract_explicit_dates('Jun-2020')
        assert len(result) >= 1

    def test_year_2025(self):
        result = extract_explicit_dates('Sep-2025')
        assert len(result) >= 1

    def test_year_2digit_10(self):
        result = extract_explicit_dates('Oct-10')
        assert len(result) >= 1

    def test_year_2digit_15(self):
        result = extract_explicit_dates('Mar-15')
        assert len(result) >= 1

    def test_year_2digit_20(self):
        result = extract_explicit_dates('Jun-20')
        assert len(result) >= 1

    def test_year_1995_reversed(self):
        result = extract_explicit_dates('1995-Oct')
        assert len(result) >= 1

    def test_year_2005_reversed(self):
        result = extract_explicit_dates('2005-Mar')
        assert len(result) >= 1

    def test_year_2digit_reversed(self):
        result = extract_explicit_dates('15-Jun')
        assert len(result) >= 1


# ---------------------------------------------------------------------------
# 22. Case-insensitive: lowercase full month names (12 tests)
# ---------------------------------------------------------------------------
