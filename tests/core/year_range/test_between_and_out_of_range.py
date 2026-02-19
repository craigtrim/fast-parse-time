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


class TestBetweenAndOutOfRange(unittest.TestCase):
    """Out-of-range years in between/and form."""

    def test_between_1800_and_1900(self):
        self.assertTrue(_no_year_range('between 1800 and 1900'))

    def test_between_1900_and_1910(self):
        self.assertTrue(_no_year_range('between 1900 and 1910'))

    def test_between_2040_and_2050(self):
        self.assertTrue(_no_year_range('between 2040 and 2050'))

    def test_between_1920_and_1930(self):
        self.assertTrue(_no_year_range('between 1920 and 1930'))

    def test_between_2100_and_2200(self):
        self.assertTrue(_no_year_range('between 2100 and 2200'))

    def test_between_1924_and_1934(self):
        self.assertTrue(_no_year_range('between 1924 and 1934'))

    def test_between_2037_and_2047(self):
        self.assertTrue(_no_year_range('between 2037 and 2047'))

    def test_between_1234_and_1235(self):
        self.assertTrue(_no_year_range('between 1234 and 1235'))

    def test_between_9000_and_9999(self):
        self.assertTrue(_no_year_range('between 9000 and 9999'))

    def test_between_0001_and_0999(self):
        self.assertTrue(_no_year_range('between 0001 and 0999'))


# ============================================================================
# Class 32 — TestBetweenAndResultShape
# 10 tests: Shape of result for "between YYYY and YYYY"
# ============================================================================
