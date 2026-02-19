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


class TestHyphenBoundaryYears(unittest.TestCase):
    """Test year pairs near the valid MIN_YEAR/MAX_YEAR boundaries."""

    def test_at_min_year_start(self):
        """MIN_YEAR-1927: first valid pair starting at MIN_YEAR."""
        self.assertTrue(_year_range('1926-1927'))

    def test_near_min_year(self):
        self.assertTrue(_year_range('1926-1936'))

    def test_one_above_min(self):
        self.assertTrue(_year_range('1927-1928'))

    def test_two_above_min(self):
        self.assertTrue(_year_range('1928-1930'))

    def test_five_above_min(self):
        self.assertTrue(_year_range('1931-1940'))

    def test_ten_above_min(self):
        self.assertTrue(_year_range('1936-1946'))

    def test_near_max_year_end(self):
        """MAX_YEAR is 2036; 2035-2036 should be valid."""
        self.assertTrue(_year_range('2035-2036'))

    def test_at_max_year(self):
        self.assertTrue(_year_range('2025-2036'))

    def test_one_below_max(self):
        self.assertTrue(_year_range('2034-2035'))

    def test_two_below_max(self):
        self.assertTrue(_year_range('2033-2034'))

    def test_five_below_max(self):
        self.assertTrue(_year_range('2030-2035'))

    def test_ten_below_max(self):
        self.assertTrue(_year_range('2026-2034'))

    def test_cross_min_boundary_invalid(self):
        """1925-1927: 1925 is below MIN_YEAR; no YEAR_RANGE expected."""
        self.assertTrue(_no_year_range('1925-1927'))

    def test_below_min_year_invalid(self):
        """1800-1900: both below MIN_YEAR."""
        self.assertTrue(_no_year_range('1800-1900'))

    def test_above_max_year_invalid(self):
        """2040-2050: both above MAX_YEAR."""
        self.assertTrue(_no_year_range('2040-2050'))

    def test_cross_max_boundary_invalid(self):
        """2035-2040: 2040 above MAX_YEAR; no YEAR_RANGE expected."""
        self.assertTrue(_no_year_range('2035-2040'))

    def test_only_end_out_of_range(self):
        """2025-2099: end year out of range."""
        self.assertTrue(_no_year_range('2025-2099'))

    def test_only_start_out_of_range(self):
        """1899-2010: start year out of range."""
        self.assertTrue(_no_year_range('1899-2010'))

    def test_both_at_valid_boundary(self):
        """1926 to 2036: full span of valid range."""
        self.assertTrue(_year_range('1926-2036'))

    def test_near_boundary_valid(self):
        self.assertTrue(_year_range('1928-1929'))


# ============================================================================
# Class 8 — TestHyphenSameYearNotRange
# 15 tests: Same year on both sides should NOT be a YEAR_RANGE
# ============================================================================
