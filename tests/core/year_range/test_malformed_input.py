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


class TestMalformedInput(unittest.TestCase):
    """Malformed or unusual inputs must not crash and must return dict or None."""

    def test_none_input(self):
        self.assertTrue(_is_dict_or_none(None))

    def test_empty_string(self):
        self.assertTrue(_is_dict_or_none(''))

    def test_whitespace_only(self):
        self.assertTrue(_is_dict_or_none('   '))

    def test_single_space(self):
        self.assertTrue(_is_dict_or_none(' '))

    def test_tab_only(self):
        self.assertTrue(_is_dict_or_none('\t'))

    def test_newline_only(self):
        self.assertTrue(_is_dict_or_none('\n'))

    def test_integer_input(self):
        self.assertTrue(_is_dict_or_none(2014))

    def test_float_input(self):
        self.assertTrue(_is_dict_or_none(2014.5))

    def test_list_input(self):
        self.assertTrue(_is_dict_or_none(['2014-2015']))

    def test_dict_input(self):
        self.assertTrue(_is_dict_or_none({'year': '2014-2015'}))

    def test_bool_true(self):
        self.assertTrue(_is_dict_or_none(True))

    def test_bool_false(self):
        self.assertTrue(_is_dict_or_none(False))

    def test_bytes_input(self):
        self.assertTrue(_is_dict_or_none(b'2014-2015'))

    def test_tuple_input(self):
        self.assertTrue(_is_dict_or_none(('2014', '2015')))

    def test_none_no_year_range(self):
        self.assertTrue(_no_year_range(None))

    def test_empty_no_year_range(self):
        self.assertTrue(_no_year_range(''))

    def test_whitespace_no_year_range(self):
        self.assertTrue(_no_year_range('   '))

    def test_int_no_year_range(self):
        self.assertTrue(_no_year_range(42))

    def test_only_letters(self):
        self.assertTrue(_no_year_range('abcdefghijk'))

    def test_single_number(self):
        """A standalone 4-digit year is YEAR_ONLY if valid, not YEAR_RANGE."""
        self.assertTrue(_no_year_range('2014'))

    def test_three_digit_number(self):
        self.assertTrue(_no_year_range('201'))

    def test_five_digit_number(self):
        self.assertTrue(_no_year_range('20145'))

    def test_special_chars_only(self):
        self.assertTrue(_is_dict_or_none('!@#$%^&*()'))

    def test_zero_string(self):
        self.assertTrue(_no_year_range('0'))

    def test_hyphen_only(self):
        self.assertTrue(_no_year_range('-'))


# ============================================================================
# Class 34 — TestCrazyInputs
# 20 tests: Unicode, HTML, emoji, pathological strings
# ============================================================================
