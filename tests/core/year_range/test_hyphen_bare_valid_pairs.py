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


class TestHyphenBareValidPairs(unittest.TestCase):
    """Bare YYYY-YYYY forms with valid in-range, ascending year pairs."""

    def test_2014_2015(self):
        self.assertTrue(_year_range('2014-2015'))

    def test_2000_2010(self):
        self.assertTrue(_year_range('2000-2010'))

    def test_1990_2000(self):
        self.assertTrue(_year_range('1990-2000'))

    def test_2010_2020(self):
        self.assertTrue(_year_range('2010-2020'))

    def test_2004_2008(self):
        self.assertTrue(_year_range('2004-2008'))

    def test_1960_1970(self):
        self.assertTrue(_year_range('1960-1970'))

    def test_1970_1980(self):
        self.assertTrue(_year_range('1970-1980'))

    def test_1980_1990(self):
        self.assertTrue(_year_range('1980-1990'))

    def test_1930_1940(self):
        self.assertTrue(_year_range('1930-1940'))

    def test_1940_1950(self):
        self.assertTrue(_year_range('1940-1950'))

    def test_1950_1960(self):
        self.assertTrue(_year_range('1950-1960'))

    def test_2020_2025(self):
        self.assertTrue(_year_range('2020-2025'))

    def test_2025_2030(self):
        self.assertTrue(_year_range('2025-2030'))

    def test_2030_2035(self):
        self.assertTrue(_year_range('2030-2035'))

    def test_1926_1927(self):
        self.assertTrue(_year_range('1926-1927'))

    def test_1927_1928(self):
        self.assertTrue(_year_range('1927-1928'))

    def test_2001_2002(self):
        self.assertTrue(_year_range('2001-2002'))

    def test_2003_2007(self):
        self.assertTrue(_year_range('2003-2007'))

    def test_2005_2015(self):
        self.assertTrue(_year_range('2005-2015'))

    def test_1955_1965(self):
        self.assertTrue(_year_range('1955-1965'))

    def test_1945_1955(self):
        self.assertTrue(_year_range('1945-1955'))

    def test_1935_1945(self):
        self.assertTrue(_year_range('1935-1945'))

    def test_2009_2011(self):
        self.assertTrue(_year_range('2009-2011'))

    def test_1998_2002(self):
        self.assertTrue(_year_range('1998-2002'))

    def test_2016_2024(self):
        self.assertTrue(_year_range('2016-2024'))

    def test_2024_2026(self):
        self.assertTrue(_year_range('2024-2026'))

    def test_1965_1975(self):
        self.assertTrue(_year_range('1965-1975'))

    def test_1975_1985(self):
        self.assertTrue(_year_range('1975-1985'))

    def test_1985_1995(self):
        self.assertTrue(_year_range('1985-1995'))

    def test_1995_2005(self):
        self.assertTrue(_year_range('1995-2005'))

    def test_2006_2016(self):
        self.assertTrue(_year_range('2006-2016'))

    def test_2007_2017(self):
        self.assertTrue(_year_range('2007-2017'))

    def test_2008_2018(self):
        self.assertTrue(_year_range('2008-2018'))

    def test_2011_2021(self):
        self.assertTrue(_year_range('2011-2021'))

    def test_2012_2022(self):
        self.assertTrue(_year_range('2012-2022'))

    def test_2013_2023(self):
        self.assertTrue(_year_range('2013-2023'))

    def test_2015_2025(self):
        self.assertTrue(_year_range('2015-2025'))

    def test_2017_2027(self):
        self.assertTrue(_year_range('2017-2027'))

    def test_1929_1933(self):
        self.assertTrue(_year_range('1929-1933'))

    def test_1939_1945(self):
        self.assertTrue(_year_range('1939-1945'))


# ============================================================================
# Class 2 — TestHyphenBareConsecutiveYears
# 20 tests: YYYY-YYYY where years differ by exactly 1
# ============================================================================
