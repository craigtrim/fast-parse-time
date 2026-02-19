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


class TestResultCountForward:
    """Standalone hyphen-month-year tokens should yield exactly 1 result."""

    def test_count_jan_abbrev_2digit(self):
        result = extract_explicit_dates('Jan-23')
        assert len(result) == 1

    def test_count_feb_abbrev_4digit(self):
        result = extract_explicit_dates('Feb-2023')
        assert len(result) == 1

    def test_count_mar_full_2digit(self):
        result = extract_explicit_dates('March-23')
        assert len(result) == 1

    def test_count_apr_full_4digit(self):
        result = extract_explicit_dates('April-2023')
        assert len(result) == 1

    def test_count_may_abbrev_2digit(self):
        result = extract_explicit_dates('May-23')
        assert len(result) == 1

    def test_count_jun_abbrev_4digit(self):
        result = extract_explicit_dates('Jun-2023')
        assert len(result) == 1

    def test_count_jul_full_2digit(self):
        result = extract_explicit_dates('July-23')
        assert len(result) == 1

    def test_count_aug_full_4digit(self):
        result = extract_explicit_dates('August-2023')
        assert len(result) == 1

    def test_count_sep_abbrev_2digit(self):
        result = extract_explicit_dates('Sep-23')
        assert len(result) == 1

    def test_count_oct_abbrev_4digit(self):
        result = extract_explicit_dates('Oct-2023')
        assert len(result) == 1

    def test_count_nov_full_2digit(self):
        result = extract_explicit_dates('November-23')
        assert len(result) == 1

    def test_count_dec_full_4digit(self):
        result = extract_explicit_dates('December-2023')
        assert len(result) == 1


# ---------------------------------------------------------------------------
# 12. Result count: reversed formats return exactly 1 result (12 tests)
# ---------------------------------------------------------------------------
