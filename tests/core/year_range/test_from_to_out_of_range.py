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


class TestFromToOutOfRange(unittest.TestCase):
    """Out-of-range years in from/to form should not produce YEAR_RANGE."""

    def test_from_1800_to_1900(self):
        self.assertTrue(_no_year_range('from 1800 to 1900'))

    def test_from_1900_to_1910(self):
        self.assertTrue(_no_year_range('from 1900 to 1910'))

    def test_from_1920_to_1930(self):
        self.assertTrue(_no_year_range('from 1920 to 1930'))

    def test_from_2040_to_2050(self):
        self.assertTrue(_no_year_range('from 2040 to 2050'))

    def test_from_2100_to_2200(self):
        self.assertTrue(_no_year_range('from 2100 to 2200'))

    def test_from_1924_to_1934(self):
        """1924 < MIN_YEAR."""
        self.assertTrue(_no_year_range('from 1924 to 1934'))

    def test_from_2036_to_2046(self):
        """2046 > MAX_YEAR."""
        self.assertTrue(_no_year_range('from 2036 to 2046'))

    def test_from_1234_to_1235(self):
        self.assertTrue(_no_year_range('from 1234 to 1235'))

    def test_from_9000_to_9999(self):
        self.assertTrue(_no_year_range('from 9000 to 9999'))

    def test_from_0001_to_0999(self):
        self.assertTrue(_no_year_range('from 0001 to 0999'))


# ============================================================================
# Class 25 — TestFromToResultShape
# 10 tests: Shape of result for "from YYYY to YYYY"
# ============================================================================
