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


class TestHyphenMultipleRanges(unittest.TestCase):
    """Multiple year ranges in a single text."""

    def test_two_ranges_both_detected(self):
        result = extract_explicit_dates('The periods 2000-2010 and 2014-2015 both matter.')
        self.assertIn('2000-2010', result or {})
        self.assertIn('2014-2015', result or {})

    def test_two_ranges_year_range_present(self):
        self.assertTrue(_year_range('The periods 2000-2010 and 2014-2015 both matter.'))

    def test_three_ranges(self):
        result = extract_explicit_dates('1990-2000, 2000-2010, and 2010-2020 were all important.')
        values = list((result or {}).values())
        self.assertGreaterEqual(values.count('YEAR_RANGE'), 1)

    def test_adjacent_ranges_no_overlap(self):
        result = extract_explicit_dates('2000-2005 and 2005-2010')
        self.assertIn('2000-2005', result or {})
        self.assertIn('2005-2010', result or {})

    def test_two_ranges_result_size(self):
        result = extract_explicit_dates('2000-2010 and 2014-2015') or {}
        year_range_count = sum(1 for v in result.values() if v == 'YEAR_RANGE')
        self.assertGreaterEqual(year_range_count, 2)

    def test_range_and_year_only(self):
        """One YEAR_RANGE and one YEAR_ONLY in same text."""
        result = extract_explicit_dates('In 2024 the period 2014-2015 was recalled.') or {}
        self.assertIn('YEAR_RANGE', result.values())
        self.assertIn('YEAR_ONLY', result.values())

    def test_two_ranges_different_spans(self):
        self.assertTrue(_year_range('1939-1945 and 2001-2010 are notable.'))

    def test_overlapping_year_ranges(self):
        """2000-2010 and 2005-2015 share 2005-2010."""
        result = extract_explicit_dates('The overlapping spans 2000-2010 and 2005-2015.') or {}
        self.assertIn('2000-2010', result)
        self.assertIn('2005-2015', result)

    def test_range_after_standalone_year(self):
        result = extract_explicit_dates('In 2020, the range 2014-2018 was reviewed.') or {}
        self.assertIn('YEAR_RANGE', result.values())

    def test_range_and_written_date(self):
        self.assertTrue(_year_range('March 2020 and the period 2014-2015.'))

    def test_two_invalid_one_valid(self):
        """1800-1900 invalid, 2014-2015 valid: only second should match."""
        result = extract_explicit_dates('From 1800-1900 and now 2014-2015.') or {}
        self.assertNotIn('1800-1900', result)
        self.assertIn('2014-2015', result)

    def test_same_range_twice(self):
        result = extract_explicit_dates('2014-2015 and again 2014-2015.') or {}
        self.assertIn('2014-2015', result)

    def test_four_ranges(self):
        text = '1960-1970, 1970-1980, 1980-1990, 1990-2000'
        self.assertTrue(_year_range(text))

    def test_range_in_list(self):
        text = '- 2000-2005\n- 2005-2010\n- 2010-2015'
        self.assertTrue(_year_range(text))

    def test_range_in_parenthetical(self):
        self.assertTrue(_year_range('Revenue (2014-2015) and costs (2016-2017) both rose.'))


# ============================================================================
# Class 17 — TestHyphenSpanSizes
# 15 tests: Various span sizes from 1 to 100 years
# ============================================================================
