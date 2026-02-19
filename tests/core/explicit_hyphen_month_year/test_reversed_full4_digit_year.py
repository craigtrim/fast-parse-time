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


class TestReversedFull4DigitYear:
    """YYYY-FullMonth patterns: 2023-January, 2023-October, etc."""

    def test_2023_january(self):
        result = extract_explicit_dates('2023-January')
        assert len(result) >= 1

    def test_2023_february(self):
        result = extract_explicit_dates('2023-February')
        assert len(result) >= 1

    def test_2023_march(self):
        result = extract_explicit_dates('2023-March')
        assert len(result) >= 1

    def test_2023_april(self):
        result = extract_explicit_dates('2023-April')
        assert len(result) >= 1

    def test_2023_may(self):
        result = extract_explicit_dates('2023-May')
        assert len(result) >= 1

    def test_2023_june(self):
        result = extract_explicit_dates('2023-June')
        assert len(result) >= 1

    def test_2023_july(self):
        result = extract_explicit_dates('2023-July')
        assert len(result) >= 1

    def test_2023_august(self):
        result = extract_explicit_dates('2023-August')
        assert len(result) >= 1

    def test_2023_september(self):
        result = extract_explicit_dates('2023-September')
        assert len(result) >= 1

    def test_2023_october(self):
        result = extract_explicit_dates('2023-October')
        assert len(result) >= 1

    def test_2023_november(self):
        result = extract_explicit_dates('2023-November')
        assert len(result) >= 1

    def test_2023_december(self):
        result = extract_explicit_dates('2023-December')
        assert len(result) >= 1


# ---------------------------------------------------------------------------
# 9. DateType verification: forward formats → MONTH_YEAR (12 tests)
# ---------------------------------------------------------------------------
