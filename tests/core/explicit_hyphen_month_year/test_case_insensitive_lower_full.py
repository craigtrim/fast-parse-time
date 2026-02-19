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


class TestCaseInsensitiveLowerFull:
    """All-lowercase full month names with hyphen."""

    def test_lower_january(self):
        result = extract_explicit_dates('january-2023')
        assert len(result) >= 1

    def test_lower_february(self):
        result = extract_explicit_dates('february-23')
        assert len(result) >= 1

    def test_lower_march(self):
        result = extract_explicit_dates('march-2023')
        assert len(result) >= 1

    def test_lower_april(self):
        result = extract_explicit_dates('april-23')
        assert len(result) >= 1

    def test_lower_may(self):
        result = extract_explicit_dates('may-2023')
        assert len(result) >= 1

    def test_lower_june(self):
        result = extract_explicit_dates('june-23')
        assert len(result) >= 1

    def test_lower_july(self):
        result = extract_explicit_dates('july-2023')
        assert len(result) >= 1

    def test_lower_august(self):
        result = extract_explicit_dates('august-23')
        assert len(result) >= 1

    def test_lower_september(self):
        result = extract_explicit_dates('september-2023')
        assert len(result) >= 1

    def test_lower_october(self):
        result = extract_explicit_dates('october-23')
        assert len(result) >= 1

    def test_lower_november(self):
        result = extract_explicit_dates('november-2023')
        assert len(result) >= 1

    def test_lower_december(self):
        result = extract_explicit_dates('december-23')
        assert len(result) >= 1


# ---------------------------------------------------------------------------
# 23. Extracted text key matches input token (12 tests)
# ---------------------------------------------------------------------------
