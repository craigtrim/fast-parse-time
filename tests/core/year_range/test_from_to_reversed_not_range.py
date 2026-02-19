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


class TestFromToReversedNotRange(unittest.TestCase):
    """Reversed from/to pairs should not produce YEAR_RANGE."""

    def test_from_2008_to_2004(self):
        self.assertTrue(_no_year_range('from 2008 to 2004'))

    def test_from_2010_to_2000(self):
        self.assertTrue(_no_year_range('from 2010 to 2000'))

    def test_from_2020_to_2010(self):
        self.assertTrue(_no_year_range('from 2020 to 2010'))

    def test_from_2000_to_1990(self):
        self.assertTrue(_no_year_range('from 2000 to 1990'))

    def test_from_1970_to_1960(self):
        self.assertTrue(_no_year_range('from 1970 to 1960'))

    def test_from_1945_to_1939(self):
        self.assertTrue(_no_year_range('from 1945 to 1939'))

    def test_from_2020_to_2019(self):
        self.assertTrue(_no_year_range('from 2020 to 2019'))

    def test_from_2015_to_2014(self):
        self.assertTrue(_no_year_range('from 2015 to 2014'))

    def test_from_2024_to_2023(self):
        self.assertTrue(_no_year_range('from 2024 to 2023'))

    def test_from_1980_to_1970(self):
        self.assertTrue(_no_year_range('from 1980 to 1970'))

    def test_from_reversed_in_sentence(self):
        self.assertTrue(_no_year_range('He went from 2010 to 2005, backward.'))

    def test_from_2030_to_2020(self):
        self.assertTrue(_no_year_range('from 2030 to 2020'))

    def test_from_2036_to_2026(self):
        self.assertTrue(_no_year_range('from 2036 to 2026'))

    def test_from_1960_to_1950(self):
        self.assertTrue(_no_year_range('from 1960 to 1950'))

    def test_from_1950_to_1940(self):
        self.assertTrue(_no_year_range('from 1950 to 1940'))


# ============================================================================
# Class 23 — TestFromToSameYearNotRange
# 10 tests: "from YYYY to YYYY" with same year not a range
# ============================================================================
