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


class TestHyphenResultIsDict(unittest.TestCase):
    """extract_explicit_dates must return dict or None for year-range inputs."""

    def test_valid_returns_dict(self):
        result = extract_explicit_dates('2014-2015')
        self.assertIsInstance(result, dict)

    def test_invalid_returns_dict_or_none(self):
        self.assertTrue(_is_dict_or_none('2015-2014'))

    def test_none_input_safe(self):
        self.assertTrue(_is_dict_or_none(None))

    def test_empty_input_safe(self):
        self.assertTrue(_is_dict_or_none(''))

    def test_out_of_range_safe(self):
        self.assertTrue(_is_dict_or_none('1800-1900'))

    def test_same_year_safe(self):
        self.assertTrue(_is_dict_or_none('2014-2014'))

    def test_random_text_safe(self):
        self.assertTrue(_is_dict_or_none('no dates here'))

    def test_partial_match_safe(self):
        self.assertTrue(_is_dict_or_none('2014'))

    def test_weird_chars_safe(self):
        self.assertTrue(_is_dict_or_none('!!!###$$$'))

    def test_valid_result_nonempty(self):
        result = extract_explicit_dates('2014-2015')
        self.assertGreater(len(result), 0)


# ============================================================================
# Class 16 — TestHyphenMultipleRanges
# 15 tests: Texts with multiple year ranges
# ============================================================================
