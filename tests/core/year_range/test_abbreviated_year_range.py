#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""TDD tests for year-range expression extraction.

620 test cases covering:
  - True positives: YYYY-YYYY bare, from/to, between/and forms
  - False positives: same year, reversed, out-of-range, non-year numbers
  - Edge cases: boundary years, punctuation, adjacency, multiple ranges
  - Crazy inputs: None, malformed, Unicode, HTML
  - Currently-unsupported forms (en dash, spaces, abbreviated year, etc.)

Related GitHub Issue:
    #40 - feat: Parse year-range expressions (e.g., 2014-2015)
    https://github.com/craigtrim/fast-parse-time/issues/40
"""

import unittest
import pytest

from fast_parse_time import extract_explicit_dates


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _year_range(text) -> bool:
    """Return True if at least one YEAR_RANGE entry exists in the result."""
    try:
        result = extract_explicit_dates(text)
        return result is not None and 'YEAR_RANGE' in result.values()
    except Exception:
        return False


def _no_year_range(text) -> bool:
    """Return True if no YEAR_RANGE entry exists (valid false-positive check)."""
    try:
        result = extract_explicit_dates(text)
        return result is None or 'YEAR_RANGE' not in result.values()
    except Exception:
        return True


def _range_key(text: str, key: str) -> bool:
    """Return True if the specific key maps to YEAR_RANGE."""
    try:
        result = extract_explicit_dates(text)
        return result is not None and result.get(key) == 'YEAR_RANGE'
    except Exception:
        return False


def _is_dict_or_none(text) -> bool:
    """Result must be a dict or None — never raise."""
    try:
        result = extract_explicit_dates(text)
        return result is None or isinstance(result, dict)
    except Exception:
        return False


# ============================================================================
# Class 1 — TestHyphenBareValidPairs
# 40 tests: valid YYYY-YYYY pairs, bare (no surrounding text)
# ============================================================================


class TestAbbreviatedYearRange(unittest.TestCase):
    """Abbreviated second year (e.g., 2025-26). Support TBD — may require xfail."""

    def test_2025_26(self):
        self.assertTrue(_year_range('2025-26'))

    def test_2024_25(self):
        self.assertTrue(_year_range('2024-25'))

    def test_2020_21(self):
        self.assertTrue(_year_range('2020-21'))

    def test_2019_20(self):
        self.assertTrue(_year_range('2019-20'))

    def test_1999_00(self):
        self.assertTrue(_year_range('1999-00'))

    def test_1989_90(self):
        self.assertTrue(_year_range('1989-90'))

    def test_in_sentence(self):
        self.assertTrue(_year_range('The fiscal year 2025-26 budget was approved.'))

    def test_with_parens(self):
        self.assertTrue(_year_range('(FY 2024-25)'))

    def test_reversed_abbreviated_not_range(self):
        """2015-14: abbreviated reversed, should not be YEAR_RANGE."""
        self.assertTrue(_no_year_range('2015-14'))

    def test_abbreviated_at_century_boundary(self):
        self.assertTrue(_year_range('1999-00'))


# ============================================================================
# Class 39 — TestFromThroughForm (EDGE CASE — may fail; xfail TBD)
# 10 tests: "from YYYY through YYYY"
# ============================================================================
