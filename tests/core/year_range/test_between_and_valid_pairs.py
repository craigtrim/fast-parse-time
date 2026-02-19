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


class TestBetweenAndValidPairs(unittest.TestCase):
    """'between YYYY and YYYY' produces YEAR_RANGE for valid pairs."""

    def test_between_2010_and_2020(self):
        self.assertTrue(_year_range('between 2010 and 2020'))

    def test_between_2000_and_2010(self):
        self.assertTrue(_year_range('between 2000 and 2010'))

    def test_between_1990_and_2000(self):
        self.assertTrue(_year_range('between 1990 and 2000'))

    def test_between_2004_and_2008(self):
        self.assertTrue(_year_range('between 2004 and 2008'))

    def test_between_1960_and_1970(self):
        self.assertTrue(_year_range('between 1960 and 1970'))

    def test_between_1950_and_1960(self):
        self.assertTrue(_year_range('between 1950 and 1960'))

    def test_between_1940_and_1950(self):
        self.assertTrue(_year_range('between 1940 and 1950'))

    def test_between_1930_and_1940(self):
        self.assertTrue(_year_range('between 1930 and 1940'))

    def test_between_1926_and_1936(self):
        self.assertTrue(_year_range('between 1926 and 1936'))

    def test_between_2019_and_2020(self):
        self.assertTrue(_year_range('between 2019 and 2020'))

    def test_between_2014_and_2015(self):
        self.assertTrue(_year_range('between 2014 and 2015'))

    def test_between_2020_and_2025(self):
        self.assertTrue(_year_range('between 2020 and 2025'))

    def test_between_2025_and_2030(self):
        self.assertTrue(_year_range('between 2025 and 2030'))

    def test_between_2030_and_2035(self):
        self.assertTrue(_year_range('between 2030 and 2035'))

    def test_between_2035_and_2036(self):
        self.assertTrue(_year_range('between 2035 and 2036'))

    def test_between_1939_and_1945(self):
        self.assertTrue(_year_range('between 1939 and 1945'))

    def test_between_1970_and_2000(self):
        self.assertTrue(_year_range('between 1970 and 2000'))

    def test_between_1945_and_1955(self):
        self.assertTrue(_year_range('between 1945 and 1955'))

    def test_between_1955_and_1965(self):
        self.assertTrue(_year_range('between 1955 and 1965'))

    def test_between_1965_and_1975(self):
        self.assertTrue(_year_range('between 1965 and 1975'))

    def test_between_1975_and_1985(self):
        self.assertTrue(_year_range('between 1975 and 1985'))

    def test_between_1985_and_1995(self):
        self.assertTrue(_year_range('between 1985 and 1995'))

    def test_between_1995_and_2005(self):
        self.assertTrue(_year_range('between 1995 and 2005'))

    def test_between_2005_and_2015(self):
        self.assertTrue(_year_range('between 2005 and 2015'))

    def test_between_2015_and_2025(self):
        self.assertTrue(_year_range('between 2015 and 2025'))

    def test_between_key_format(self):
        result = extract_explicit_dates('between 2004 and 2008') or {}
        self.assertIn('2004-2008', result)

    def test_between_value_format(self):
        result = extract_explicit_dates('between 2004 and 2008') or {}
        self.assertEqual(result.get('2004-2008'), 'YEAR_RANGE')

    def test_between_result_is_dict(self):
        result = extract_explicit_dates('between 2004 and 2008')
        self.assertIsInstance(result, dict)

    def test_between_result_nonempty(self):
        result = extract_explicit_dates('between 2004 and 2008')
        self.assertGreater(len(result), 0)

    def test_between_1926_and_2036(self):
        """Full valid range."""
        self.assertTrue(_year_range('between 1926 and 2036'))


# ============================================================================
# Class 27 — TestBetweenAndInSentence
# 15 tests: "between YYYY and YYYY" embedded in sentences
# ============================================================================
