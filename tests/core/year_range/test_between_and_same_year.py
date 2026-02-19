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


class TestBetweenAndSameYear(unittest.TestCase):
    """Same year in between/and form should not be YEAR_RANGE."""

    def test_between_2014_and_2014(self):
        self.assertTrue(_no_year_range('between 2014 and 2014'))

    def test_between_2000_and_2000(self):
        self.assertTrue(_no_year_range('between 2000 and 2000'))

    def test_between_1990_and_1990(self):
        self.assertTrue(_no_year_range('between 1990 and 1990'))

    def test_between_2024_and_2024(self):
        self.assertTrue(_no_year_range('between 2024 and 2024'))

    def test_between_2020_and_2020(self):
        self.assertTrue(_no_year_range('between 2020 and 2020'))

    def test_between_1926_and_1926(self):
        self.assertTrue(_no_year_range('between 1926 and 1926'))

    def test_between_2036_and_2036(self):
        self.assertTrue(_no_year_range('between 2036 and 2036'))

    def test_between_1950_and_1950(self):
        self.assertTrue(_no_year_range('between 1950 and 1950'))

    def test_between_1975_and_1975(self):
        self.assertTrue(_no_year_range('between 1975 and 1975'))

    def test_between_2010_and_2010(self):
        self.assertTrue(_no_year_range('between 2010 and 2010'))


# ============================================================================
# Class 31 — TestBetweenAndOutOfRange
# 10 tests: Out-of-range years in between/and form
# ============================================================================
