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


class TestResultCountReversed:
    """Reversed standalone tokens should yield exactly 1 result."""

    def test_count_2digit_jan(self):
        result = extract_explicit_dates('23-Jan')
        assert len(result) == 1

    def test_count_4digit_feb(self):
        result = extract_explicit_dates('2023-Feb')
        assert len(result) == 1

    def test_count_2digit_march(self):
        result = extract_explicit_dates('23-March')
        assert len(result) == 1

    def test_count_4digit_april(self):
        result = extract_explicit_dates('2023-April')
        assert len(result) == 1

    def test_count_2digit_may(self):
        result = extract_explicit_dates('23-May')
        assert len(result) == 1

    def test_count_4digit_jun(self):
        result = extract_explicit_dates('2023-Jun')
        assert len(result) == 1

    def test_count_2digit_july(self):
        result = extract_explicit_dates('23-July')
        assert len(result) == 1

    def test_count_4digit_aug(self):
        result = extract_explicit_dates('2023-Aug')
        assert len(result) == 1

    def test_count_2digit_sep(self):
        result = extract_explicit_dates('23-Sep')
        assert len(result) == 1

    def test_count_4digit_oct(self):
        result = extract_explicit_dates('2023-Oct')
        assert len(result) == 1

    def test_count_2digit_november(self):
        result = extract_explicit_dates('23-November')
        assert len(result) == 1

    def test_count_4digit_dec(self):
        result = extract_explicit_dates('2023-Dec')
        assert len(result) == 1


# ---------------------------------------------------------------------------
# 13. Case-insensitive: lowercase abbreviated months (12 tests)
# ---------------------------------------------------------------------------
