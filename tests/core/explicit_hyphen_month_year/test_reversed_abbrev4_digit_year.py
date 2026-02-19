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


class TestReversedAbbrev4DigitYear:
    """YYYY-MonthAbbr patterns: 2023-Jan, 2023-Oct, etc."""

    def test_2023_jan(self):
        result = extract_explicit_dates('2023-Jan')
        assert len(result) >= 1

    def test_2023_feb(self):
        result = extract_explicit_dates('2023-Feb')
        assert len(result) >= 1

    def test_2023_mar(self):
        result = extract_explicit_dates('2023-Mar')
        assert len(result) >= 1

    def test_2023_apr(self):
        result = extract_explicit_dates('2023-Apr')
        assert len(result) >= 1

    def test_2023_may(self):
        result = extract_explicit_dates('2023-May')
        assert len(result) >= 1

    def test_2023_jun(self):
        result = extract_explicit_dates('2023-Jun')
        assert len(result) >= 1

    def test_2023_jul(self):
        result = extract_explicit_dates('2023-Jul')
        assert len(result) >= 1

    def test_2023_aug(self):
        result = extract_explicit_dates('2023-Aug')
        assert len(result) >= 1

    def test_2023_sep(self):
        result = extract_explicit_dates('2023-Sep')
        assert len(result) >= 1

    def test_2023_oct(self):
        result = extract_explicit_dates('2023-Oct')
        assert len(result) >= 1

    def test_2023_nov(self):
        result = extract_explicit_dates('2023-Nov')
        assert len(result) >= 1

    def test_2023_dec(self):
        result = extract_explicit_dates('2023-Dec')
        assert len(result) >= 1


# ---------------------------------------------------------------------------
# 7. Reversed: 2-digit year + hyphen + full month name → YEAR_MONTH (12 tests)
# ---------------------------------------------------------------------------
