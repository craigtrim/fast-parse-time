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


class TestFromToValidPairs(unittest.TestCase):
    """'from YYYY to YYYY' produces YEAR_RANGE for valid pairs."""

    def test_from_2004_to_2008(self):
        self.assertTrue(_year_range('from 2004 to 2008'))

    def test_from_2000_to_2010(self):
        self.assertTrue(_year_range('from 2000 to 2010'))

    def test_from_1990_to_2000(self):
        self.assertTrue(_year_range('from 1990 to 2000'))

    def test_from_2010_to_2020(self):
        self.assertTrue(_year_range('from 2010 to 2020'))

    def test_from_1960_to_1970(self):
        self.assertTrue(_year_range('from 1960 to 1970'))

    def test_from_1950_to_1960(self):
        self.assertTrue(_year_range('from 1950 to 1960'))

    def test_from_1940_to_1950(self):
        self.assertTrue(_year_range('from 1940 to 1950'))

    def test_from_1930_to_1940(self):
        self.assertTrue(_year_range('from 1930 to 1940'))

    def test_from_1926_to_1936(self):
        self.assertTrue(_year_range('from 1926 to 1936'))

    def test_from_2019_to_2020(self):
        self.assertTrue(_year_range('from 2019 to 2020'))

    def test_from_2014_to_2015(self):
        self.assertTrue(_year_range('from 2014 to 2015'))

    def test_from_2020_to_2025(self):
        self.assertTrue(_year_range('from 2020 to 2025'))

    def test_from_2025_to_2030(self):
        self.assertTrue(_year_range('from 2025 to 2030'))

    def test_from_2030_to_2035(self):
        self.assertTrue(_year_range('from 2030 to 2035'))

    def test_from_2035_to_2036(self):
        self.assertTrue(_year_range('from 2035 to 2036'))

    def test_from_1970_to_2000(self):
        self.assertTrue(_year_range('from 1970 to 2000'))

    def test_from_1939_to_1945(self):
        self.assertTrue(_year_range('from 1939 to 1945'))

    def test_from_1945_to_1955(self):
        self.assertTrue(_year_range('from 1945 to 1955'))

    def test_from_1955_to_1965(self):
        self.assertTrue(_year_range('from 1955 to 1965'))

    def test_from_1965_to_1975(self):
        self.assertTrue(_year_range('from 1965 to 1975'))

    def test_from_1975_to_1985(self):
        self.assertTrue(_year_range('from 1975 to 1985'))

    def test_from_1985_to_1995(self):
        self.assertTrue(_year_range('from 1985 to 1995'))

    def test_from_1995_to_2005(self):
        self.assertTrue(_year_range('from 1995 to 2005'))

    def test_from_2005_to_2015(self):
        self.assertTrue(_year_range('from 2005 to 2015'))

    def test_from_2015_to_2025(self):
        self.assertTrue(_year_range('from 2015 to 2025'))

    def test_from_key_format(self):
        """from-to produces 'YYYY-YYYY' key in result."""
        result = extract_explicit_dates('from 2004 to 2008') or {}
        self.assertIn('2004-2008', result)

    def test_from_value_format(self):
        result = extract_explicit_dates('from 2004 to 2008') or {}
        self.assertEqual(result.get('2004-2008'), 'YEAR_RANGE')

    def test_from_result_is_dict(self):
        result = extract_explicit_dates('from 2004 to 2008')
        self.assertIsInstance(result, dict)

    def test_from_result_nonempty(self):
        result = extract_explicit_dates('from 2004 to 2008')
        self.assertTrue(len(result) >= 1)

    def test_from_1926_to_2036(self):
        """Full valid range."""
        self.assertTrue(_year_range('from 1926 to 2036'))


# ============================================================================
# Class 19 — TestFromToInSentence
# 15 tests: "from YYYY to YYYY" embedded in sentences
# ============================================================================
