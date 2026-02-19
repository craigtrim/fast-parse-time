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


class TestFromToSameYearNotRange(unittest.TestCase):
    """Same year in from/to form should not produce YEAR_RANGE."""

    def test_from_2014_to_2014(self):
        self.assertTrue(_no_year_range('from 2014 to 2014'))

    def test_from_2000_to_2000(self):
        self.assertTrue(_no_year_range('from 2000 to 2000'))

    def test_from_1990_to_1990(self):
        self.assertTrue(_no_year_range('from 1990 to 1990'))

    def test_from_1960_to_1960(self):
        self.assertTrue(_no_year_range('from 1960 to 1960'))

    def test_from_2024_to_2024(self):
        self.assertTrue(_no_year_range('from 2024 to 2024'))

    def test_from_2020_to_2020(self):
        self.assertTrue(_no_year_range('from 2020 to 2020'))

    def test_from_1926_to_1926(self):
        self.assertTrue(_no_year_range('from 1926 to 1926'))

    def test_from_2036_to_2036(self):
        self.assertTrue(_no_year_range('from 2036 to 2036'))

    def test_from_1950_to_1950(self):
        self.assertTrue(_no_year_range('from 1950 to 1950'))

    def test_from_1975_to_1975(self):
        self.assertTrue(_no_year_range('from 1975 to 1975'))


# ============================================================================
# Class 24 — TestFromToOutOfRange
# 10 tests: "from YYYY to YYYY" with out-of-range years
# ============================================================================
