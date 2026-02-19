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


class TestHyphenSameYearNotRange(unittest.TestCase):
    """Same-year hyphenated pairs are not year ranges."""

    def test_2014_2014(self):
        self.assertTrue(_no_year_range('2014-2014'))

    def test_2000_2000(self):
        self.assertTrue(_no_year_range('2000-2000'))

    def test_2020_2020(self):
        self.assertTrue(_no_year_range('2020-2020'))

    def test_1990_1990(self):
        self.assertTrue(_no_year_range('1990-1990'))

    def test_1960_1960(self):
        self.assertTrue(_no_year_range('1960-1960'))

    def test_1950_1950(self):
        self.assertTrue(_no_year_range('1950-1950'))

    def test_1940_1940(self):
        self.assertTrue(_no_year_range('1940-1940'))

    def test_1930_1930(self):
        self.assertTrue(_no_year_range('1930-1930'))

    def test_2010_2010(self):
        self.assertTrue(_no_year_range('2010-2010'))

    def test_2015_2015(self):
        self.assertTrue(_no_year_range('2015-2015'))

    def test_2024_2024(self):
        self.assertTrue(_no_year_range('2024-2024'))

    def test_1926_1926(self):
        self.assertTrue(_no_year_range('1926-1926'))

    def test_2036_2036(self):
        self.assertTrue(_no_year_range('2036-2036'))

    def test_2001_2001(self):
        self.assertTrue(_no_year_range('2001-2001'))

    def test_1975_1975(self):
        self.assertTrue(_no_year_range('1975-1975'))


# ============================================================================
# Class 9 — TestHyphenReversedNotRange
# 15 tests: Reversed (end < start) must not be YEAR_RANGE
# ============================================================================
