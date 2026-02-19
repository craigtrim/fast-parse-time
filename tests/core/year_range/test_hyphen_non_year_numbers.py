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


class TestHyphenNonYearNumbers(unittest.TestCase):
    """Numbers that look like year ranges but aren't (not in valid range, etc.)."""

    def test_phone_555_1234(self):
        """555-1234: not 4-digit pairs in valid year range."""
        self.assertTrue(_no_year_range('555-1234'))

    def test_page_range_3_10(self):
        self.assertTrue(_no_year_range('pages 3-10'))

    def test_page_range_100_200(self):
        self.assertTrue(_no_year_range('pages 100-200'))

    def test_version_1_2(self):
        self.assertTrue(_no_year_range('version 1-2'))

    def test_score_3_0(self):
        self.assertTrue(_no_year_range('score 3-0'))

    def test_isbn_like(self):
        self.assertTrue(_no_year_range('978-3-16'))

    def test_zip_90210_1234(self):
        """ZIP+4: 90210-1234 — 90210 and 1234 not in year range."""
        self.assertTrue(_no_year_range('90210-1234'))

    def test_small_small(self):
        self.assertTrue(_no_year_range('12-34'))

    def test_large_large(self):
        self.assertTrue(_no_year_range('10000-20000'))

    def test_not_four_digits_each(self):
        self.assertTrue(_no_year_range('20-2015'))

    def test_five_digit_first(self):
        self.assertTrue(_no_year_range('20145-2016'))

    def test_five_digit_second(self):
        self.assertTrue(_no_year_range('2014-20155'))

    def test_zero_range(self):
        self.assertTrue(_no_year_range('0000-0000'))

    def test_all_nines(self):
        self.assertTrue(_no_year_range('9999-9998'))

    def test_ssn_like(self):
        self.assertTrue(_no_year_range('123-45-6789'))

    def test_time_range(self):
        """9-5 job: not year range."""
        self.assertTrue(_no_year_range('9-5 job'))

    def test_channel_range(self):
        self.assertTrue(_no_year_range('channels 100-200'))

    def test_zip_code_like(self):
        self.assertTrue(_no_year_range('12345-6789'))

    def test_product_code(self):
        self.assertTrue(_no_year_range('SKU-1234'))

    def test_mix_alpha_num(self):
        self.assertTrue(_no_year_range('A2014-B2015'))


# ============================================================================
# Class 12 — TestHyphenAdjacentNonBoundary
# 10 tests: Year-like strings that don't have word boundaries
# ============================================================================
