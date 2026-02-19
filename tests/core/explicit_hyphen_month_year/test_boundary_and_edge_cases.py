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


class TestBoundaryAndEdgeCases:
    """Edge cases around year boundaries and single-digit elements."""

    def test_year_2000_abbrev(self):
        """Earliest plausible 2-digit year → 2000."""
        result = extract_explicit_dates('Jan-00')
        assert len(result) >= 1

    def test_year_2099_abbrev(self):
        """Latest plausible 2-digit year → 2099."""
        result = extract_explicit_dates('Dec-99')
        assert len(result) >= 1

    def test_year_1990_4digit(self):
        """Historical 4-digit year within MIN_YEAR range."""
        result = extract_explicit_dates('Oct-1990')
        assert len(result) >= 1

    def test_year_2030_4digit(self):
        """Near-future 4-digit year within MAX_YEAR range."""
        result = extract_explicit_dates('Mar-2030')
        assert len(result) >= 1

    def test_reversed_year_2000(self):
        result = extract_explicit_dates('00-Jan')
        assert len(result) >= 1

    def test_reversed_year_1990(self):
        result = extract_explicit_dates('1990-Oct')
        assert len(result) >= 1

    def test_mixed_case_forward(self):
        """Mixed case like 'oCt-2023' should still match."""
        result = extract_explicit_dates('oCt-2023')
        assert len(result) >= 1

    def test_mixed_case_reversed(self):
        """Mixed case in reversed format."""
        result = extract_explicit_dates('2023-oCt')
        assert len(result) >= 1

    def test_full_month_lower_forward(self):
        result = extract_explicit_dates('march-2023')
        assert len(result) >= 1

    def test_full_month_upper_forward(self):
        result = extract_explicit_dates('MARCH-2023')
        assert len(result) >= 1


# ---------------------------------------------------------------------------
# 19. Non-match cases: should return empty or None (10 tests)
# ---------------------------------------------------------------------------
