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


class TestDateTypeForwardIsMonthYear:
    """Forward MonthAbbr-YYYY patterns must return DateType MONTH_YEAR."""

    def test_jan_type(self):
        result = extract_explicit_dates('Jan-2023')
        assert 'MONTH_YEAR' in result.values()

    def test_feb_type(self):
        result = extract_explicit_dates('Feb-2023')
        assert 'MONTH_YEAR' in result.values()

    def test_mar_type(self):
        result = extract_explicit_dates('Mar-2023')
        assert 'MONTH_YEAR' in result.values()

    def test_apr_type(self):
        result = extract_explicit_dates('Apr-2023')
        assert 'MONTH_YEAR' in result.values()

    def test_may_type(self):
        result = extract_explicit_dates('May-2023')
        assert 'MONTH_YEAR' in result.values()

    def test_jun_type(self):
        result = extract_explicit_dates('Jun-2023')
        assert 'MONTH_YEAR' in result.values()

    def test_jul_type(self):
        result = extract_explicit_dates('Jul-2023')
        assert 'MONTH_YEAR' in result.values()

    def test_aug_type(self):
        result = extract_explicit_dates('Aug-2023')
        assert 'MONTH_YEAR' in result.values()

    def test_sep_type(self):
        result = extract_explicit_dates('Sep-2023')
        assert 'MONTH_YEAR' in result.values()

    def test_oct_type(self):
        result = extract_explicit_dates('Oct-2023')
        assert 'MONTH_YEAR' in result.values()

    def test_nov_type(self):
        result = extract_explicit_dates('Nov-2023')
        assert 'MONTH_YEAR' in result.values()

    def test_dec_type(self):
        result = extract_explicit_dates('Dec-2023')
        assert 'MONTH_YEAR' in result.values()


# ---------------------------------------------------------------------------
# 10. DateType verification: reversed formats → YEAR_MONTH (12 tests)
# ---------------------------------------------------------------------------
