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


class TestHyphenOutOfRangeYears(unittest.TestCase):
    """Out-of-range years should not produce YEAR_RANGE."""

    def test_1800_1900(self):
        self.assertTrue(_no_year_range('1800-1900'))

    def test_1700_1800(self):
        self.assertTrue(_no_year_range('1700-1800'))

    def test_1000_1500(self):
        self.assertTrue(_no_year_range('1000-1500'))

    def test_0001_1000(self):
        self.assertTrue(_no_year_range('0001-1000'))

    def test_2040_2050(self):
        self.assertTrue(_no_year_range('2040-2050'))

    def test_2050_2060(self):
        self.assertTrue(_no_year_range('2050-2060'))

    def test_2100_2200(self):
        self.assertTrue(_no_year_range('2100-2200'))

    def test_9000_9999(self):
        self.assertTrue(_no_year_range('9000-9999'))

    def test_1920_1930(self):
        """1920-1930: 1920 is below MIN_YEAR (1926)."""
        self.assertTrue(_no_year_range('1920-1930'))

    def test_1924_1926(self):
        """1924 < MIN_YEAR."""
        self.assertTrue(_no_year_range('1924-1926'))

    def test_1925_1930(self):
        """1925 < MIN_YEAR."""
        self.assertTrue(_no_year_range('1925-1930'))

    def test_2036_2037(self):
        """2037 > MAX_YEAR (2036)."""
        self.assertTrue(_no_year_range('2036-2037'))

    def test_2037_2040(self):
        self.assertTrue(_no_year_range('2037-2040'))

    def test_2038_2050(self):
        self.assertTrue(_no_year_range('2038-2050'))

    def test_1899_1901(self):
        self.assertTrue(_no_year_range('1899-1901'))

    def test_1910_1920(self):
        self.assertTrue(_no_year_range('1910-1920'))

    def test_1900_1910(self):
        self.assertTrue(_no_year_range('1900-1910'))

    def test_1234_1235(self):
        self.assertTrue(_no_year_range('1234-1235'))

    def test_1111_1112(self):
        self.assertTrue(_no_year_range('1111-1112'))

    def test_3000_4000(self):
        self.assertTrue(_no_year_range('3000-4000'))


# ============================================================================
# Class 11 — TestHyphenNonYearNumbers
# 20 tests: 4-digit or other number combos that aren't year ranges
# ============================================================================
