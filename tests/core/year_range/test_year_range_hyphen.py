#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
TDD tests for prose year extraction (preposition-preceded YEAR_ONLY and YEAR_RANGE).

Related GitHub Issue:
    #24 - Gap: year-only references not extracted from prose (in 2004, in 2008)
    https://github.com/craigtrim/fast-parse-time/issues/24

All tests are written BEFORE implementation (red phase).
"""

import unittest
from fast_parse_time.api import extract_explicit_dates


# ── helpers ─────────────────────────────────────────────────────────────────

def _year_only(text: str) -> bool:
    """Return True if at least one YEAR_ONLY entry exists in the result."""
    return 'YEAR_ONLY' in extract_explicit_dates(text).values()


def _year_range(text: str) -> bool:
    """Return True if at least one YEAR_RANGE entry exists in the result."""
    return 'YEAR_RANGE' in extract_explicit_dates(text).values()


def _has_key(text: str, key: str) -> bool:
    return key in extract_explicit_dates(text)


# ============================================================================
# Part A — Preposition: "in"
# ============================================================================


class TestYearRangeHyphen(unittest.TestCase):
    """YYYY-YYYY hyphen form should return YEAR_RANGE (existing bug fix)."""

    def test_2014_2015_nonempty(self):
        self.assertTrue(extract_explicit_dates('2014-2015'))

    def test_2014_2015_type(self):
        self.assertTrue(_year_range('2014-2015'))

    def test_2014_2015_key(self):
        self.assertTrue(_has_key('2014-2015', '2014-2015'))

    def test_2014_2015_value(self):
        result = extract_explicit_dates('2014-2015')
        self.assertEqual(result.get('2014-2015'), 'YEAR_RANGE')

    def test_2000_2010_range(self):
        self.assertTrue(_year_range('2000-2010'))

    def test_2000_2010_key(self):
        self.assertTrue(_has_key('2000-2010', '2000-2010'))

    def test_1990_2000_range(self):
        self.assertTrue(_year_range('1990-2000'))

    def test_2010_2020_range(self):
        self.assertTrue(_year_range('2010-2020'))

    def test_2020_2025_range(self):
        self.assertTrue(_year_range('2020-2025'))

    def test_2004_2008_range(self):
        self.assertTrue(_year_range('2004-2008'))

    def test_in_sentence(self):
        self.assertTrue(_year_range('the period 2014-2015 was significant'))

    def test_in_sentence_key(self):
        result = extract_explicit_dates('the period 2014-2015 was significant')
        self.assertIn('2014-2015', result)

    def test_monotonic_required_same_year_not_range(self):
        """2014-2014 is not a valid range (start == end)."""
        result = extract_explicit_dates('2014-2014')
        self.assertNotEqual(result.get('2014-2014'), 'YEAR_RANGE')

    def test_reversed_not_range(self):
        """2015-2014 (end < start) is not a valid range."""
        result = extract_explicit_dates('2015-2014')
        self.assertNotEqual(result.get('2015-2014'), 'YEAR_RANGE')

    def test_out_of_range_years_not_range(self):
        """1800-1900 — both out of MIN_YEAR — should not return YEAR_RANGE."""
        result = extract_explicit_dates('1800-1900')
        self.assertNotIn('YEAR_RANGE', result.values())

    def test_result_is_dict(self):
        result = extract_explicit_dates('2014-2015')
        self.assertIsInstance(result, dict)


# ============================================================================
# Part B — YEAR_RANGE: "from YYYY to YYYY"
# ============================================================================
