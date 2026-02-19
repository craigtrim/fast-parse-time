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


class TestFullMonthHyphen4DigitYearForward:
    """FullMonth-YYYY patterns: March-2023, January-2000, December-1999, etc."""

    def test_january_4digit(self):
        result = extract_explicit_dates('January-2023')
        assert len(result) >= 1

    def test_february_4digit(self):
        result = extract_explicit_dates('February-2023')
        assert len(result) >= 1

    def test_march_4digit(self):
        result = extract_explicit_dates('March-2023')
        assert len(result) >= 1

    def test_april_4digit(self):
        result = extract_explicit_dates('April-2023')
        assert len(result) >= 1

    def test_may_4digit(self):
        result = extract_explicit_dates('May-2023')
        assert len(result) >= 1

    def test_june_4digit(self):
        result = extract_explicit_dates('June-2023')
        assert len(result) >= 1

    def test_july_4digit(self):
        result = extract_explicit_dates('July-2023')
        assert len(result) >= 1

    def test_august_4digit(self):
        result = extract_explicit_dates('August-2023')
        assert len(result) >= 1

    def test_september_4digit(self):
        result = extract_explicit_dates('September-2023')
        assert len(result) >= 1

    def test_october_4digit(self):
        result = extract_explicit_dates('October-2023')
        assert len(result) >= 1

    def test_november_4digit(self):
        result = extract_explicit_dates('November-2023')
        assert len(result) >= 1

    def test_december_4digit(self):
        result = extract_explicit_dates('December-2023')
        assert len(result) >= 1


# ---------------------------------------------------------------------------
# 5. Reversed: 2-digit year + hyphen + abbreviated month → YEAR_MONTH (12 tests)
# ---------------------------------------------------------------------------
