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


class TestCaseInsensitiveLowerAbbrev:
    """All-lowercase abbreviated month-year tokens should match."""

    def test_lower_jan(self):
        result = extract_explicit_dates('jan-23')
        assert len(result) >= 1

    def test_lower_feb(self):
        result = extract_explicit_dates('feb-2023')
        assert len(result) >= 1

    def test_lower_mar(self):
        result = extract_explicit_dates('mar-23')
        assert len(result) >= 1

    def test_lower_apr(self):
        result = extract_explicit_dates('apr-2023')
        assert len(result) >= 1

    def test_lower_may(self):
        result = extract_explicit_dates('may-23')
        assert len(result) >= 1

    def test_lower_jun(self):
        result = extract_explicit_dates('jun-2023')
        assert len(result) >= 1

    def test_lower_jul(self):
        result = extract_explicit_dates('jul-23')
        assert len(result) >= 1

    def test_lower_aug(self):
        result = extract_explicit_dates('aug-2023')
        assert len(result) >= 1

    def test_lower_sep(self):
        result = extract_explicit_dates('sep-23')
        assert len(result) >= 1

    def test_lower_oct(self):
        result = extract_explicit_dates('oct-23')
        assert len(result) >= 1

    def test_lower_nov(self):
        result = extract_explicit_dates('nov-2023')
        assert len(result) >= 1

    def test_lower_dec(self):
        result = extract_explicit_dates('dec-23')
        assert len(result) >= 1


# ---------------------------------------------------------------------------
# 14. Case-insensitive: uppercase abbreviated months (12 tests)
# ---------------------------------------------------------------------------
