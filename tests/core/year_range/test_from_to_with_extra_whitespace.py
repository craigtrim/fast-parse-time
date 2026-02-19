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


class TestFromToWithExtraWhitespace(unittest.TestCase):
    """Extra whitespace between tokens in 'from YYYY to YYYY'."""

    def test_double_space_from(self):
        """'from  2004 to 2008': two spaces after 'from'."""
        self.assertTrue(_year_range('from  2004 to 2008'))

    def test_double_space_to(self):
        """'from 2004 to  2008': two spaces after 'to'."""
        self.assertTrue(_year_range('from 2004 to  2008'))

    def test_double_space_both(self):
        self.assertTrue(_year_range('from  2004  to  2008'))

    def test_tab_after_from(self):
        self.assertTrue(_year_range('from\t2004 to 2008'))

    def test_tab_after_to(self):
        self.assertTrue(_year_range('from 2004 to\t2008'))

    def test_tab_both(self):
        self.assertTrue(_year_range('from\t2004\tto\t2008'))

    def test_newline_after_from(self):
        self.assertTrue(_year_range('from\n2004 to 2008'))

    def test_newline_after_to(self):
        self.assertTrue(_year_range('from 2004 to\n2008'))

    def test_triple_space_from(self):
        self.assertTrue(_year_range('from   2004 to 2008'))

    def test_mixed_whitespace(self):
        self.assertTrue(_year_range('from \t 2004 to \t 2008'))


# ============================================================================
# Class 22 — TestFromToReversedNotRange
# 15 tests: "from YYYY to YYYY" with reversed years not a range
# ============================================================================
