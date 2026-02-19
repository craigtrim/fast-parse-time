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


class TestSeptAlternativeAbbrev:
    """'Sept' (4-letter) is a valid alternative to 'Sep'."""

    def test_sept_2digit_forward(self):
        result = extract_explicit_dates('Sept-23')
        assert len(result) >= 1

    def test_sept_4digit_forward(self):
        result = extract_explicit_dates('Sept-2023')
        assert len(result) >= 1

    def test_2digit_sept_reversed(self):
        result = extract_explicit_dates('23-Sept')
        assert len(result) >= 1

    def test_4digit_sept_reversed(self):
        result = extract_explicit_dates('2023-Sept')
        assert len(result) >= 1

    def test_sept_sentence_forward(self):
        result = extract_explicit_dates('Report from Sept-2023 quarter')
        assert len(result) >= 1

    def test_sept_sentence_reversed(self):
        result = extract_explicit_dates('Filed under 2023-Sept archive')
        assert len(result) >= 1


# ---------------------------------------------------------------------------
# 18. Boundary and edge cases (10 tests)
# ---------------------------------------------------------------------------
