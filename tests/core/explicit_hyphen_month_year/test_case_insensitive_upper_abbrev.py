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


class TestCaseInsensitiveUpperAbbrev:
    """All-uppercase abbreviated month-year tokens should match."""

    def test_upper_jan(self):
        result = extract_explicit_dates('JAN-23')
        assert len(result) >= 1

    def test_upper_feb(self):
        result = extract_explicit_dates('FEB-2023')
        assert len(result) >= 1

    def test_upper_mar(self):
        result = extract_explicit_dates('MAR-23')
        assert len(result) >= 1

    def test_upper_apr(self):
        result = extract_explicit_dates('APR-2023')
        assert len(result) >= 1

    def test_upper_may(self):
        result = extract_explicit_dates('MAY-23')
        assert len(result) >= 1

    def test_upper_jun(self):
        result = extract_explicit_dates('JUN-2023')
        assert len(result) >= 1

    def test_upper_jul(self):
        result = extract_explicit_dates('JUL-23')
        assert len(result) >= 1

    def test_upper_aug(self):
        result = extract_explicit_dates('AUG-2023')
        assert len(result) >= 1

    def test_upper_sep(self):
        result = extract_explicit_dates('SEP-23')
        assert len(result) >= 1

    def test_upper_oct(self):
        result = extract_explicit_dates('OCT-23')
        assert len(result) >= 1

    def test_upper_nov(self):
        result = extract_explicit_dates('NOV-2023')
        assert len(result) >= 1

    def test_upper_dec(self):
        result = extract_explicit_dates('DEC-23')
        assert len(result) >= 1


# ---------------------------------------------------------------------------
# 15. Sentence-embedded: forward formats in prose (12 tests)
# ---------------------------------------------------------------------------
