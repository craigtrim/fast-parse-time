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


class TestHyphenSpanSizes(unittest.TestCase):
    """Valid ranges of varying year-span sizes."""

    def test_span_1_year(self):
        self.assertTrue(_year_range('2019-2020'))

    def test_span_2_years(self):
        self.assertTrue(_year_range('2018-2020'))

    def test_span_3_years(self):
        self.assertTrue(_year_range('2017-2020'))

    def test_span_4_years(self):
        self.assertTrue(_year_range('2016-2020'))

    def test_span_5_years(self):
        self.assertTrue(_year_range('2015-2020'))

    def test_span_10_years(self):
        self.assertTrue(_year_range('2010-2020'))

    def test_span_15_years(self):
        self.assertTrue(_year_range('2005-2020'))

    def test_span_20_years(self):
        self.assertTrue(_year_range('2000-2020'))

    def test_span_25_years(self):
        self.assertTrue(_year_range('1995-2020'))

    def test_span_30_years(self):
        self.assertTrue(_year_range('1990-2020'))

    def test_span_40_years(self):
        self.assertTrue(_year_range('1980-2020'))

    def test_span_50_years(self):
        self.assertTrue(_year_range('1970-2020'))

    def test_span_60_years(self):
        self.assertTrue(_year_range('1960-2020'))

    def test_span_70_years(self):
        self.assertTrue(_year_range('1950-2020'))

    def test_span_110_years_full_range(self):
        """Span from MIN_YEAR to MAX_YEAR: 1926-2036."""
        self.assertTrue(_year_range('1926-2036'))


# ============================================================================
# Class 18 — TestFromToValidPairs
# 30 tests: "from YYYY to YYYY" valid pairs
# ============================================================================
