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


class TestBetweenAndCasing(unittest.TestCase):
    """Case insensitivity for 'between YYYY and YYYY'."""

    def test_uppercase(self):
        self.assertTrue(_year_range('BETWEEN 2010 AND 2020'))

    def test_title_case(self):
        self.assertTrue(_year_range('Between 2010 And 2020'))

    def test_between_upper_and_lower(self):
        self.assertTrue(_year_range('BETWEEN 2010 and 2020'))

    def test_between_lower_and_upper(self):
        self.assertTrue(_year_range('between 2010 AND 2020'))

    def test_mixed_case_1(self):
        self.assertTrue(_year_range('BeTwEeN 2010 AnD 2020'))

    def test_mixed_case_2(self):
        self.assertTrue(_year_range('bEtWeEn 2010 aND 2020'))

    def test_all_caps_in_sentence(self):
        self.assertTrue(_year_range('BORN BETWEEN 2010 AND 2020.'))

    def test_title_in_sentence(self):
        self.assertTrue(_year_range('Born Between 2010 And 2020.'))

    def test_lower_in_sentence(self):
        self.assertTrue(_year_range('born between 2010 and 2020.'))

    def test_upper_in_sentence(self):
        self.assertTrue(_year_range('born BETWEEN 2010 AND 2020.'))

    def test_random_caps_1(self):
        self.assertTrue(_year_range('BETween 2004 aNd 2008'))

    def test_random_caps_2(self):
        self.assertTrue(_year_range('betWEEN 2004 AND 2008'))

    def test_sentence_start_upper(self):
        self.assertTrue(_year_range('Between 2014 and 2015 was notable.'))

    def test_sentence_start_lower(self):
        self.assertTrue(_year_range('between 2014 and 2015 was notable.'))

    def test_sentence_start_all_caps(self):
        self.assertTrue(_year_range('BETWEEN 2014 AND 2015 was notable.'))


# ============================================================================
# Class 29 — TestBetweenAndReversedNotRange
# 15 tests: Reversed years in between/and form
# ============================================================================
