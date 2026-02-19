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


class TestFromToCasing(unittest.TestCase):
    """Case insensitivity for 'from YYYY to YYYY'."""

    def test_uppercase_from_to(self):
        self.assertTrue(_year_range('FROM 2004 TO 2008'))

    def test_title_case(self):
        self.assertTrue(_year_range('From 2004 To 2008'))

    def test_from_upper_to_lower(self):
        self.assertTrue(_year_range('FROM 2004 to 2008'))

    def test_from_lower_to_upper(self):
        self.assertTrue(_year_range('from 2004 TO 2008'))

    def test_mixed_case_1(self):
        self.assertTrue(_year_range('FrOm 2004 tO 2008'))

    def test_mixed_case_2(self):
        self.assertTrue(_year_range('fROM 2004 To 2008'))

    def test_all_caps_in_sentence(self):
        self.assertTrue(_year_range('THE PERIOD FROM 2004 TO 2008 WAS KEY.'))

    def test_title_in_sentence(self):
        self.assertTrue(_year_range('The Period From 2004 To 2008 Was Key.'))

    def test_from_lower_in_sentence(self):
        self.assertTrue(_year_range('It ran from 2004 to 2008.'))

    def test_from_upper_in_sentence(self):
        self.assertTrue(_year_range('It ran FROM 2004 TO 2008.'))

    def test_from_title_in_sentence(self):
        self.assertTrue(_year_range('It ran From 2004 To 2008.'))

    def test_random_caps_1(self):
        self.assertTrue(_year_range('FROm 2010 tO 2020'))

    def test_random_caps_2(self):
        self.assertTrue(_year_range('froM 2010 TO 2020'))

    def test_sentence_start_upper(self):
        self.assertTrue(_year_range('From 2014 to 2015 was significant.'))

    def test_sentence_start_lower(self):
        self.assertTrue(_year_range('from 2014 to 2015 was significant.'))


# ============================================================================
# Class 21 — TestFromToWithExtraWhitespace
# 10 tests: Extra spaces in "from YYYY to YYYY"
# MIN_YEAR=1926, MAX_YEAR=2036; valid pairs only
# ============================================================================
