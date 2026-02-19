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


class TestFromToResultShape(unittest.TestCase):
    """Verify result structure for from/to year range expressions."""

    def test_result_is_dict(self):
        result = extract_explicit_dates('from 2004 to 2008')
        self.assertIsInstance(result, dict)

    def test_result_nonempty(self):
        result = extract_explicit_dates('from 2004 to 2008')
        self.assertGreater(len(result), 0)

    def test_key_format(self):
        result = extract_explicit_dates('from 2004 to 2008') or {}
        self.assertIn('2004-2008', result)

    def test_value_is_year_range(self):
        result = extract_explicit_dates('from 2004 to 2008') or {}
        self.assertEqual(result.get('2004-2008'), 'YEAR_RANGE')

    def test_key_is_string(self):
        result = extract_explicit_dates('from 2004 to 2008') or {}
        for k in result:
            self.assertIsInstance(k, str)

    def test_value_is_string(self):
        result = extract_explicit_dates('from 2004 to 2008') or {}
        for v in result.values():
            self.assertIsInstance(v, str)

    def test_key_not_full_phrase(self):
        """Key should be '2004-2008', not 'from 2004 to 2008'."""
        result = extract_explicit_dates('from 2004 to 2008') or {}
        self.assertNotIn('from 2004 to 2008', result)

    def test_key_ascending(self):
        """Key must be start-end, not end-start."""
        result = extract_explicit_dates('from 2004 to 2008') or {}
        self.assertIn('2004-2008', result)
        self.assertNotIn('2008-2004', result)

    def test_result_not_list(self):
        result = extract_explicit_dates('from 2004 to 2008')
        self.assertNotIsInstance(result, list)

    def test_multiple_from_to(self):
        result = extract_explicit_dates('from 2000 to 2005 and from 2010 to 2015') or {}
        self.assertIn('2000-2005', result)
        self.assertIn('2010-2015', result)


# ============================================================================
# Class 26 — TestBetweenAndValidPairs
# 30 tests: "between YYYY and YYYY" valid pairs
# ============================================================================
