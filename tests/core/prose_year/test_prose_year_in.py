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


class TestProseYearIn(unittest.TestCase):
    """Preposition 'in' preceding a 4-digit year."""

    def test_in_2004_nonempty(self):
        self.assertTrue(extract_explicit_dates('in 2004'))

    def test_in_2004_year_only_type(self):
        self.assertTrue(_year_only('in 2004'))

    def test_in_2004_key(self):
        self.assertTrue(_has_key('in 2004', '2004'))

    def test_in_2008_nonempty(self):
        self.assertTrue(extract_explicit_dates('in 2008'))

    def test_in_2008_year_only_type(self):
        self.assertTrue(_year_only('in 2008'))

    def test_in_2008_key(self):
        self.assertTrue(_has_key('in 2008', '2008'))

    def test_in_2019_nonempty(self):
        self.assertTrue(extract_explicit_dates('in 2019'))

    def test_in_2019_key(self):
        self.assertTrue(_has_key('in 2019', '2019'))

    def test_in_1998_nonempty(self):
        self.assertTrue(extract_explicit_dates('in 1998'))

    def test_in_1998_key(self):
        self.assertTrue(_has_key('in 1998', '1998'))

    def test_in_sentence_1(self):
        """'...title in 2004.' — compat datefinder test."""
        self.assertTrue(_year_only('the film had its title in 2004.'))

    def test_in_sentence_2(self):
        """'...traumatized on the sets in 2008.' — compat datefinder test."""
        self.assertTrue(_year_only('traumatized on the sets in 2008.'))

    def test_in_sentence_3(self):
        self.assertTrue(_year_only('the company was founded in 2004'))

    def test_in_sentence_key(self):
        result = extract_explicit_dates('the company was founded in 2004')
        self.assertIn('2004', result)

    def test_in_sentence_type(self):
        result = extract_explicit_dates('the company was founded in 2004')
        self.assertEqual(result.get('2004'), 'YEAR_ONLY')

    def test_in_2024_future_year(self):
        self.assertTrue(_year_only('in 2024'))

    def test_in_2030_near_max(self):
        self.assertTrue(_year_only('in 2030'))

    def test_in_uppercase_IN(self):
        """Case-insensitive: 'IN 2004'."""
        self.assertTrue(_year_only('IN 2004'))

    def test_in_mixed_case(self):
        """Case-insensitive: 'In 2004'."""
        self.assertTrue(_year_only('In 2004'))

    def test_in_result_count_minimum(self):
        result = extract_explicit_dates('in 2004')
        self.assertGreaterEqual(len(result), 1)

    def test_in_year_only_value(self):
        result = extract_explicit_dates('in 2004')
        self.assertEqual(result.get('2004'), 'YEAR_ONLY')


# ============================================================================
# Part A — Preposition: "since"
# ============================================================================
