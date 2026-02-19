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


class TestFullMonthHyphen2DigitYearForward:
    """FullMonth-YY patterns: March-23, January-00, December-99, etc."""

    def test_january_2digit(self):
        result = extract_explicit_dates('January-23')
        assert len(result) >= 1

    def test_february_2digit(self):
        result = extract_explicit_dates('February-23')
        assert len(result) >= 1

    def test_march_2digit(self):
        result = extract_explicit_dates('March-23')
        assert len(result) >= 1

    def test_april_2digit(self):
        result = extract_explicit_dates('April-23')
        assert len(result) >= 1

    def test_may_2digit(self):
        result = extract_explicit_dates('May-23')
        assert len(result) >= 1

    def test_june_2digit(self):
        result = extract_explicit_dates('June-23')
        assert len(result) >= 1

    def test_july_2digit(self):
        result = extract_explicit_dates('July-23')
        assert len(result) >= 1

    def test_august_2digit(self):
        result = extract_explicit_dates('August-23')
        assert len(result) >= 1

    def test_september_2digit(self):
        result = extract_explicit_dates('September-23')
        assert len(result) >= 1

    def test_october_2digit(self):
        result = extract_explicit_dates('October-23')
        assert len(result) >= 1

    def test_november_2digit(self):
        result = extract_explicit_dates('November-23')
        assert len(result) >= 1

    def test_december_2digit(self):
        result = extract_explicit_dates('December-23')
        assert len(result) >= 1


# ---------------------------------------------------------------------------
# 4. Full month name + hyphen + 4-digit year → MONTH_YEAR (12 tests)
# ---------------------------------------------------------------------------
