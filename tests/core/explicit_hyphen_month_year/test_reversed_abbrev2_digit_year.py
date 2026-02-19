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


class TestReversedAbbrev2DigitYear:
    """YY-MonthAbbr patterns: 23-Jan, 23-Oct, etc."""

    def test_23_jan(self):
        result = extract_explicit_dates('23-Jan')
        assert len(result) >= 1

    def test_23_feb(self):
        result = extract_explicit_dates('23-Feb')
        assert len(result) >= 1

    def test_23_mar(self):
        result = extract_explicit_dates('23-Mar')
        assert len(result) >= 1

    def test_23_apr(self):
        result = extract_explicit_dates('23-Apr')
        assert len(result) >= 1

    def test_23_may(self):
        result = extract_explicit_dates('23-May')
        assert len(result) >= 1

    def test_23_jun(self):
        result = extract_explicit_dates('23-Jun')
        assert len(result) >= 1

    def test_23_jul(self):
        result = extract_explicit_dates('23-Jul')
        assert len(result) >= 1

    def test_23_aug(self):
        result = extract_explicit_dates('23-Aug')
        assert len(result) >= 1

    def test_23_sep(self):
        result = extract_explicit_dates('23-Sep')
        assert len(result) >= 1

    def test_23_oct(self):
        result = extract_explicit_dates('23-Oct')
        assert len(result) >= 1

    def test_23_nov(self):
        result = extract_explicit_dates('23-Nov')
        assert len(result) >= 1

    def test_23_dec(self):
        result = extract_explicit_dates('23-Dec')
        assert len(result) >= 1


# ---------------------------------------------------------------------------
# 6. Reversed: 4-digit year + hyphen + abbreviated month → YEAR_MONTH (12 tests)
# ---------------------------------------------------------------------------
