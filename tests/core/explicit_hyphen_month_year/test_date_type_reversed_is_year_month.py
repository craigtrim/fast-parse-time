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


class TestDateTypeReversedIsYearMonth:
    """Reversed YYYY-MonthAbbr patterns must return DateType YEAR_MONTH."""

    def test_year_jan_type(self):
        result = extract_explicit_dates('2023-Jan')
        assert 'YEAR_MONTH' in result.values()

    def test_year_feb_type(self):
        result = extract_explicit_dates('2023-Feb')
        assert 'YEAR_MONTH' in result.values()

    def test_year_mar_type(self):
        result = extract_explicit_dates('2023-Mar')
        assert 'YEAR_MONTH' in result.values()

    def test_year_apr_type(self):
        result = extract_explicit_dates('2023-Apr')
        assert 'YEAR_MONTH' in result.values()

    def test_year_may_type(self):
        result = extract_explicit_dates('2023-May')
        assert 'YEAR_MONTH' in result.values()

    def test_year_jun_type(self):
        result = extract_explicit_dates('2023-Jun')
        assert 'YEAR_MONTH' in result.values()

    def test_year_jul_type(self):
        result = extract_explicit_dates('2023-Jul')
        assert 'YEAR_MONTH' in result.values()

    def test_year_aug_type(self):
        result = extract_explicit_dates('2023-Aug')
        assert 'YEAR_MONTH' in result.values()

    def test_year_sep_type(self):
        result = extract_explicit_dates('2023-Sep')
        assert 'YEAR_MONTH' in result.values()

    def test_year_oct_type(self):
        result = extract_explicit_dates('2023-Oct')
        assert 'YEAR_MONTH' in result.values()

    def test_year_nov_type(self):
        result = extract_explicit_dates('2023-Nov')
        assert 'YEAR_MONTH' in result.values()

    def test_year_dec_type(self):
        result = extract_explicit_dates('2023-Dec')
        assert 'YEAR_MONTH' in result.values()


# ---------------------------------------------------------------------------
# 11. Result count: forward formats return exactly 1 result (12 tests)
# ---------------------------------------------------------------------------
