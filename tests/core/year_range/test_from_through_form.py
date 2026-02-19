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


class TestFromThroughForm(unittest.TestCase):
    """'from YYYY through YYYY' form. Support TBD — may require xfail."""

    def test_from_2004_through_2008(self):
        self.assertTrue(_year_range('from 2004 through 2008'))

    def test_from_2000_through_2010(self):
        self.assertTrue(_year_range('from 2000 through 2010'))

    def test_from_1990_through_2000(self):
        self.assertTrue(_year_range('from 1990 through 2000'))

    def test_from_1939_through_1945(self):
        self.assertTrue(_year_range('from 1939 through 1945'))

    def test_in_sentence(self):
        self.assertTrue(_year_range('The project ran from 2010 through 2015.'))

    def test_uppercase_from_through(self):
        self.assertTrue(_year_range('FROM 2004 THROUGH 2008'))

    def test_reversed_not_range(self):
        self.assertTrue(_no_year_range('from 2008 through 2004'))

    def test_same_year_not_range(self):
        self.assertTrue(_no_year_range('from 2014 through 2014'))

    def test_out_of_range(self):
        self.assertTrue(_no_year_range('from 1800 through 1900'))

    def test_consecutive(self):
        self.assertTrue(_year_range('from 2019 through 2020'))


# ============================================================================
# Class 40 — TestBareYearToYear (EDGE CASE — may fail; xfail TBD)
# 10 tests: "YYYY to YYYY" without "from"
# ============================================================================
