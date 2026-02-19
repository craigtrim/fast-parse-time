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


class TestAbbrevHyphen2DigitYearForward:
    """MonthAbbr-YY patterns: Oct-23, Jan-00, Dec-99, etc."""

    def test_jan_2digit(self):
        result = extract_explicit_dates('Jan-23')
        assert len(result) >= 1

    def test_feb_2digit(self):
        result = extract_explicit_dates('Feb-23')
        assert len(result) >= 1

    def test_mar_2digit(self):
        result = extract_explicit_dates('Mar-23')
        assert len(result) >= 1

    def test_apr_2digit(self):
        result = extract_explicit_dates('Apr-23')
        assert len(result) >= 1

    def test_may_2digit(self):
        result = extract_explicit_dates('May-23')
        assert len(result) >= 1

    def test_jun_2digit(self):
        result = extract_explicit_dates('Jun-23')
        assert len(result) >= 1

    def test_jul_2digit(self):
        result = extract_explicit_dates('Jul-23')
        assert len(result) >= 1

    def test_aug_2digit(self):
        result = extract_explicit_dates('Aug-23')
        assert len(result) >= 1

    def test_sep_2digit(self):
        result = extract_explicit_dates('Sep-23')
        assert len(result) >= 1

    def test_oct_2digit(self):
        result = extract_explicit_dates('Oct-23')
        assert len(result) >= 1

    def test_nov_2digit(self):
        result = extract_explicit_dates('Nov-23')
        assert len(result) >= 1

    def test_dec_2digit(self):
        result = extract_explicit_dates('Dec-23')
        assert len(result) >= 1


# ---------------------------------------------------------------------------
# 2. Abbreviated month + hyphen + 4-digit year → MONTH_YEAR (12 tests)
# ---------------------------------------------------------------------------
