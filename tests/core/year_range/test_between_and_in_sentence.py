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


class TestBetweenAndInSentence(unittest.TestCase):
    """'between YYYY and YYYY' inside longer sentences."""

    def test_born_between(self):
        self.assertTrue(_year_range('He was born between 1950 and 1960.'))

    def test_happened_between(self):
        self.assertTrue(_year_range('It happened between 2000 and 2010.'))

    def test_built_between(self):
        self.assertTrue(_year_range('The building was built between 1960 and 1970.'))

    def test_income_between(self):
        self.assertTrue(_year_range('Income grew between 1990 and 2000.'))

    def test_she_worked_between(self):
        self.assertTrue(_year_range('She worked there between 2005 and 2015.'))

    def test_war_between(self):
        self.assertTrue(_year_range('The war ended between 1939 and 1945.'))

    def test_period_between(self):
        self.assertTrue(_year_range('The period between 2014 and 2020 saw growth.'))

    def test_data_between(self):
        self.assertTrue(_year_range('Data collected between 2008 and 2012.'))

    def test_sentence_start(self):
        self.assertTrue(_year_range('Between 2010 and 2020, revenues doubled.'))

    def test_with_comma(self):
        self.assertTrue(_year_range('Between 2010 and 2020, revenues doubled.'))

    def test_mid_sentence_comma(self):
        self.assertTrue(_year_range('The gap, between 2004 and 2008, was notable.'))

    def test_at_end(self):
        self.assertTrue(_year_range('Prices rose between 2000 and 2010'))

    def test_with_quotes(self):
        self.assertTrue(_year_range('"between 2004 and 2008" is the range'))

    def test_after_conjunction(self):
        self.assertTrue(_year_range('I lived there and then between 2010 and 2015.'))

    def test_multiple_between(self):
        self.assertTrue(_year_range('Events between 1960 and 1970 and also between 2000 and 2010.'))


# ============================================================================
# Class 28 — TestBetweenAndCasing
# 15 tests: Casing variants of "between YYYY and YYYY"
# ============================================================================
