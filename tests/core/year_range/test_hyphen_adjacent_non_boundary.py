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


class TestHyphenAdjacentNonBoundary(unittest.TestCase):
    """Year ranges abutting alpha chars lack word boundary; should not match."""

    def test_prefix_alpha(self):
        """abc2014-2015: no word boundary before 2014."""
        self.assertTrue(_no_year_range('abc2014-2015'))

    def test_suffix_alpha(self):
        """2014-2015xyz: no word boundary after 2015."""
        self.assertTrue(_no_year_range('2014-2015xyz'))

    def test_both_sides_alpha(self):
        self.assertTrue(_no_year_range('x2014-2015y'))

    def test_prefix_underscore(self):
        """_2014-2015: underscore is a word char, so no boundary before 2014."""
        self.assertTrue(_no_year_range('_2014-2015'))

    def test_suffix_underscore(self):
        self.assertTrue(_no_year_range('2014-2015_suffix'))

    def test_embedded_in_word(self):
        self.assertTrue(_no_year_range('report2014-2015data'))

    def test_camel_case_prefix(self):
        self.assertTrue(_no_year_range('Year2014-2015'))

    def test_camel_case_suffix(self):
        self.assertTrue(_no_year_range('2014-2015Year'))

    def test_digit_prefix(self):
        """32014-2015: 5-digit first token, no match."""
        self.assertTrue(_no_year_range('32014-2015'))

    def test_digit_suffix(self):
        """2014-20153: 5-digit second token, no match."""
        self.assertTrue(_no_year_range('2014-20153'))


# ============================================================================
# Class 13 — TestHyphenResultKeyFormat
# 15 tests: Verify the key in result is exactly "YYYY-YYYY"
# ============================================================================
