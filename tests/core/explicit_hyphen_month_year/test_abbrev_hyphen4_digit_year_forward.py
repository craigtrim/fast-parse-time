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


class TestAbbrevHyphen4DigitYearForward:
    """MonthAbbr-YYYY patterns: Oct-2023, Jan-2000, Dec-1999, etc."""

    def test_jan_4digit(self):
        result = extract_explicit_dates('Jan-2023')
        assert len(result) >= 1

    def test_feb_4digit(self):
        result = extract_explicit_dates('Feb-2023')
        assert len(result) >= 1

    def test_mar_4digit(self):
        result = extract_explicit_dates('Mar-2023')
        assert len(result) >= 1

    def test_apr_4digit(self):
        result = extract_explicit_dates('Apr-2023')
        assert len(result) >= 1

    def test_may_4digit(self):
        result = extract_explicit_dates('May-2023')
        assert len(result) >= 1

    def test_jun_4digit(self):
        result = extract_explicit_dates('Jun-2023')
        assert len(result) >= 1

    def test_jul_4digit(self):
        result = extract_explicit_dates('Jul-2023')
        assert len(result) >= 1

    def test_aug_4digit(self):
        result = extract_explicit_dates('Aug-2023')
        assert len(result) >= 1

    def test_sep_4digit(self):
        result = extract_explicit_dates('Sep-2023')
        assert len(result) >= 1

    def test_oct_4digit(self):
        result = extract_explicit_dates('Oct-2023')
        assert len(result) >= 1

    def test_nov_4digit(self):
        result = extract_explicit_dates('Nov-2023')
        assert len(result) >= 1

    def test_dec_4digit(self):
        result = extract_explicit_dates('Dec-2023')
        assert len(result) >= 1


# ---------------------------------------------------------------------------
# 3. Full month name + hyphen + 2-digit year → MONTH_YEAR (12 tests)
# ---------------------------------------------------------------------------
