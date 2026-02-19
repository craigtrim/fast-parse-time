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


class TestHyphenWithSurroundingPunctuation(unittest.TestCase):
    """Surrounding punctuation should not prevent YEAR_RANGE detection."""

    def test_parens(self):
        self.assertTrue(_year_range('(2014-2015)'))

    def test_brackets(self):
        self.assertTrue(_year_range('[2014-2015]'))

    def test_curly(self):
        self.assertTrue(_year_range('{2014-2015}'))

    def test_quotes_double(self):
        self.assertTrue(_year_range('"2014-2015"'))

    def test_quotes_single(self):
        self.assertTrue(_year_range("'2014-2015'"))

    def test_trailing_period(self):
        self.assertTrue(_year_range('2014-2015.'))

    def test_trailing_comma(self):
        self.assertTrue(_year_range('2014-2015,'))

    def test_trailing_semicolon(self):
        self.assertTrue(_year_range('2014-2015;'))

    def test_trailing_colon(self):
        self.assertTrue(_year_range('2014-2015:'))

    def test_trailing_question(self):
        self.assertTrue(_year_range('2014-2015?'))

    def test_trailing_exclamation(self):
        self.assertTrue(_year_range('2014-2015!'))

    def test_parens_in_sentence(self):
        self.assertTrue(_year_range('The era (2014-2015) was notable.'))

    def test_brackets_in_sentence(self):
        self.assertTrue(_year_range('See [2014-2015] for data.'))

    def test_period_in_sentence(self):
        self.assertTrue(_year_range('We covered 2014-2015. Then 2016 came.'))

    def test_comma_in_sentence(self):
        self.assertTrue(_year_range('The years 2014-2015, were busy.'))

    def test_colon_in_sentence(self):
        self.assertTrue(_year_range('Revenue: 2014-2015, grew quickly.'))

    def test_slash_after(self):
        self.assertTrue(_year_range('Report 2014-2015/annual'))

    def test_angle_brackets(self):
        self.assertTrue(_year_range('<2014-2015>'))

    def test_parens_wrapped_sentence(self):
        self.assertTrue(_year_range('(see: 2014-2015)'))

    def test_mixed_punct(self):
        self.assertTrue(_year_range('[period: 2014-2015]'))


# ============================================================================
# Class 7 — TestHyphenBoundaryYears
# 20 tests: Years near MIN_YEAR (1926) and MAX_YEAR (2036)
# ============================================================================
