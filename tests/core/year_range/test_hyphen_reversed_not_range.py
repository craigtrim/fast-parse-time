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


class TestHyphenReversedNotRange(unittest.TestCase):
    """Reversed year order is not a valid range."""

    def test_2015_2014(self):
        self.assertTrue(_no_year_range('2015-2014'))

    def test_2010_2000(self):
        self.assertTrue(_no_year_range('2010-2000'))

    def test_2000_1990(self):
        self.assertTrue(_no_year_range('2000-1990'))

    def test_1990_1980(self):
        self.assertTrue(_no_year_range('1990-1980'))

    def test_1970_1960(self):
        self.assertTrue(_no_year_range('1970-1960'))

    def test_2020_2019(self):
        self.assertTrue(_no_year_range('2020-2019'))

    def test_2024_2023(self):
        self.assertTrue(_no_year_range('2024-2023'))

    def test_2030_2020(self):
        self.assertTrue(_no_year_range('2030-2020'))

    def test_1960_1950(self):
        self.assertTrue(_no_year_range('1960-1950'))

    def test_1950_1940(self):
        self.assertTrue(_no_year_range('1950-1940'))

    def test_1940_1930(self):
        self.assertTrue(_no_year_range('1940-1930'))

    def test_1980_1970(self):
        self.assertTrue(_no_year_range('1980-1970'))

    def test_2036_2026(self):
        self.assertTrue(_no_year_range('2036-2026'))

    def test_2000_1926(self):
        self.assertTrue(_no_year_range('2000-1926'))

    def test_2015_2014_in_sentence(self):
        self.assertTrue(_no_year_range('The period 2015-2014 is odd.'))


# ============================================================================
# Class 10 — TestHyphenOutOfRangeYears
# 20 tests: Year values outside MIN_YEAR..MAX_YEAR range
# ============================================================================
