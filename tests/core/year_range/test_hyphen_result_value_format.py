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


class TestHyphenResultValueFormat(unittest.TestCase):
    """Verify the value in result dict is the string 'YEAR_RANGE'."""

    def test_value_2014_2015(self):
        result = extract_explicit_dates('2014-2015')
        self.assertEqual(result.get('2014-2015'), 'YEAR_RANGE')

    def test_value_2000_2010(self):
        result = extract_explicit_dates('2000-2010')
        self.assertEqual(result.get('2000-2010'), 'YEAR_RANGE')

    def test_value_1990_2000(self):
        result = extract_explicit_dates('1990-2000')
        self.assertEqual(result.get('1990-2000'), 'YEAR_RANGE')

    def test_value_2004_2008(self):
        result = extract_explicit_dates('2004-2008')
        self.assertEqual(result.get('2004-2008'), 'YEAR_RANGE')

    def test_value_is_string(self):
        result = extract_explicit_dates('2014-2015')
        self.assertIsInstance(result.get('2014-2015'), str)

    def test_value_not_enum(self):
        """Should be string 'YEAR_RANGE', not a DateType enum member."""
        result = extract_explicit_dates('2014-2015')
        self.assertEqual(result.get('2014-2015'), 'YEAR_RANGE')

    def test_value_exact_case(self):
        result = extract_explicit_dates('2014-2015')
        self.assertNotEqual(result.get('2014-2015'), 'year_range')

    def test_value_not_year_only(self):
        result = extract_explicit_dates('2014-2015')
        self.assertNotEqual(result.get('2014-2015'), 'YEAR_ONLY')

    def test_value_1939_1945(self):
        result = extract_explicit_dates('1939-1945')
        self.assertEqual(result.get('1939-1945'), 'YEAR_RANGE')

    def test_value_2019_2020(self):
        result = extract_explicit_dates('2019-2020')
        self.assertEqual(result.get('2019-2020'), 'YEAR_RANGE')

    def test_value_1926_1927(self):
        result = extract_explicit_dates('1926-1927')
        self.assertEqual(result.get('1926-1927'), 'YEAR_RANGE')

    def test_value_2035_2036(self):
        result = extract_explicit_dates('2035-2036')
        self.assertEqual(result.get('2035-2036'), 'YEAR_RANGE')

    def test_value_in_sentence(self):
        result = extract_explicit_dates('The era 2014-2015 was notable.')
        self.assertEqual(result.get('2014-2015'), 'YEAR_RANGE')

    def test_value_with_parens(self):
        result = extract_explicit_dates('(2014-2015)')
        self.assertEqual(result.get('2014-2015'), 'YEAR_RANGE')

    def test_value_trailing_period(self):
        result = extract_explicit_dates('2014-2015.')
        self.assertEqual(result.get('2014-2015'), 'YEAR_RANGE')


# ============================================================================
# Class 15 — TestHyphenResultIsDict
# 10 tests: Result must always be a dict or None, never raise
# ============================================================================
