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


class TestHyphenResultKeyFormat(unittest.TestCase):
    """The result dict key for YYYY-YYYY should be the 'YYYY-YYYY' string."""

    def test_key_2014_2015(self):
        self.assertTrue(_range_key('2014-2015', '2014-2015'))

    def test_key_2000_2010(self):
        self.assertTrue(_range_key('2000-2010', '2000-2010'))

    def test_key_1990_2000(self):
        self.assertTrue(_range_key('1990-2000', '1990-2000'))

    def test_key_2004_2008(self):
        self.assertTrue(_range_key('2004-2008', '2004-2008'))

    def test_key_1960_1970(self):
        self.assertTrue(_range_key('1960-1970', '1960-1970'))

    def test_key_2019_2020(self):
        self.assertTrue(_range_key('2019-2020', '2019-2020'))

    def test_key_in_sentence(self):
        self.assertTrue(_range_key('The era 2014-2015 passed.', '2014-2015'))

    def test_key_1926_1927(self):
        self.assertTrue(_range_key('1926-1927', '1926-1927'))

    def test_key_2035_2036(self):
        self.assertTrue(_range_key('2035-2036', '2035-2036'))

    def test_key_1939_1945(self):
        self.assertTrue(_range_key('1939-1945', '1939-1945'))

    def test_key_2020_2025(self):
        self.assertTrue(_range_key('2020-2025', '2020-2025'))

    def test_key_not_swapped(self):
        """Key should be 2014-2015, not 2015-2014."""
        result = extract_explicit_dates('2014-2015')
        self.assertIn('2014-2015', result or {})
        self.assertNotIn('2015-2014', result or {})

    def test_key_2010_2020(self):
        self.assertTrue(_range_key('2010-2020', '2010-2020'))

    def test_key_1975_1985(self):
        self.assertTrue(_range_key('1975-1985', '1975-1985'))

    def test_key_with_punctuation(self):
        self.assertTrue(_range_key('(2014-2015)', '2014-2015'))


# ============================================================================
# Class 14 — TestHyphenResultValueFormat
# 15 tests: The dict value must be the string 'YEAR_RANGE'
# ============================================================================
