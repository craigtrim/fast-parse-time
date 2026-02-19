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


class TestReversedFull2DigitYear:
    """YY-FullMonth patterns: 23-January, 23-October, etc."""

    def test_23_january(self):
        result = extract_explicit_dates('23-January')
        assert len(result) >= 1

    def test_23_february(self):
        result = extract_explicit_dates('23-February')
        assert len(result) >= 1

    def test_23_march(self):
        result = extract_explicit_dates('23-March')
        assert len(result) >= 1

    def test_23_april(self):
        result = extract_explicit_dates('23-April')
        assert len(result) >= 1

    def test_23_may(self):
        result = extract_explicit_dates('23-May')
        assert len(result) >= 1

    def test_23_june(self):
        result = extract_explicit_dates('23-June')
        assert len(result) >= 1

    def test_23_july(self):
        result = extract_explicit_dates('23-July')
        assert len(result) >= 1

    def test_23_august(self):
        result = extract_explicit_dates('23-August')
        assert len(result) >= 1

    def test_23_september(self):
        result = extract_explicit_dates('23-September')
        assert len(result) >= 1

    def test_23_october(self):
        result = extract_explicit_dates('23-October')
        assert len(result) >= 1

    def test_23_november(self):
        result = extract_explicit_dates('23-November')
        assert len(result) >= 1

    def test_23_december(self):
        result = extract_explicit_dates('23-December')
        assert len(result) >= 1


# ---------------------------------------------------------------------------
# 8. Reversed: 4-digit year + hyphen + full month name → YEAR_MONTH (12 tests)
# ---------------------------------------------------------------------------
