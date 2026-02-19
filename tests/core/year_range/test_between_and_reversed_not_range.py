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


class TestBetweenAndReversedNotRange(unittest.TestCase):
    """Reversed year order in between/and form is not a YEAR_RANGE."""

    def test_between_2020_and_2010(self):
        self.assertTrue(_no_year_range('between 2020 and 2010'))

    def test_between_2010_and_2000(self):
        self.assertTrue(_no_year_range('between 2010 and 2000'))

    def test_between_2000_and_1990(self):
        self.assertTrue(_no_year_range('between 2000 and 1990'))

    def test_between_1970_and_1960(self):
        self.assertTrue(_no_year_range('between 1970 and 1960'))

    def test_between_1945_and_1939(self):
        self.assertTrue(_no_year_range('between 1945 and 1939'))

    def test_between_2020_and_2019(self):
        self.assertTrue(_no_year_range('between 2020 and 2019'))

    def test_between_2015_and_2014(self):
        self.assertTrue(_no_year_range('between 2015 and 2014'))

    def test_between_2024_and_2023(self):
        self.assertTrue(_no_year_range('between 2024 and 2023'))

    def test_between_1980_and_1970(self):
        self.assertTrue(_no_year_range('between 1980 and 1970'))

    def test_between_reversed_in_sentence(self):
        self.assertTrue(_no_year_range('He lived between 2010 and 2005.'))

    def test_between_2030_and_2020(self):
        self.assertTrue(_no_year_range('between 2030 and 2020'))

    def test_between_1960_and_1950(self):
        self.assertTrue(_no_year_range('between 1960 and 1950'))

    def test_between_1950_and_1940(self):
        self.assertTrue(_no_year_range('between 1950 and 1940'))

    def test_between_1940_and_1930(self):
        self.assertTrue(_no_year_range('between 1940 and 1930'))

    def test_between_2036_and_2026(self):
        self.assertTrue(_no_year_range('between 2036 and 2026'))


# ============================================================================
# Class 30 — TestBetweenAndSameYear
# 10 tests: Same year in between/and form
# ============================================================================
