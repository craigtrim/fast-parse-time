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


class TestHyphenBareConsecutiveYears(unittest.TestCase):
    """Consecutive-year pairs: the smallest valid range."""

    def test_2019_2020(self):
        self.assertTrue(_year_range('2019-2020'))

    def test_2020_2021(self):
        self.assertTrue(_year_range('2020-2021'))

    def test_2021_2022(self):
        self.assertTrue(_year_range('2021-2022'))

    def test_2022_2023(self):
        self.assertTrue(_year_range('2022-2023'))

    def test_2023_2024(self):
        self.assertTrue(_year_range('2023-2024'))

    def test_2018_2019(self):
        self.assertTrue(_year_range('2018-2019'))

    def test_2017_2018(self):
        self.assertTrue(_year_range('2017-2018'))

    def test_2016_2017(self):
        self.assertTrue(_year_range('2016-2017'))

    def test_2015_2016(self):
        self.assertTrue(_year_range('2015-2016'))

    def test_2014_2015_consecutive(self):
        self.assertTrue(_year_range('2014-2015'))

    def test_1999_2000(self):
        self.assertTrue(_year_range('1999-2000'))

    def test_1989_1990(self):
        self.assertTrue(_year_range('1989-1990'))

    def test_1979_1980(self):
        self.assertTrue(_year_range('1979-1980'))

    def test_1969_1970(self):
        self.assertTrue(_year_range('1969-1970'))

    def test_1959_1960(self):
        self.assertTrue(_year_range('1959-1960'))

    def test_1949_1950(self):
        self.assertTrue(_year_range('1949-1950'))

    def test_1939_1940(self):
        self.assertTrue(_year_range('1939-1940'))

    def test_1929_1930(self):
        self.assertTrue(_year_range('1929-1930'))

    def test_2035_2036(self):
        self.assertTrue(_year_range('2035-2036'))

    def test_2034_2035(self):
        self.assertTrue(_year_range('2034-2035'))


# ============================================================================
# Class 3 — TestHyphenInSentenceStart
# 15 tests: Year range at the start of a sentence
# ============================================================================
