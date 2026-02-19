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


class TestProseYearSince(unittest.TestCase):
    """Preposition 'since' preceding a 4-digit year."""

    def test_since_2019_nonempty(self):
        self.assertTrue(extract_explicit_dates('since 2019'))

    def test_since_2019_type(self):
        self.assertTrue(_year_only('since 2019'))

    def test_since_2019_key(self):
        self.assertTrue(_has_key('since 2019', '2019'))

    def test_since_1990_key(self):
        self.assertTrue(_has_key('since 1990', '1990'))

    def test_since_sentence(self):
        self.assertTrue(_year_only('we have been open since 2005'))

    def test_since_sentence_key(self):
        result = extract_explicit_dates('we have been open since 2005')
        self.assertIn('2005', result)

    def test_since_value(self):
        result = extract_explicit_dates('since 2019')
        self.assertEqual(result.get('2019'), 'YEAR_ONLY')

    def test_since_uppercase(self):
        self.assertTrue(_year_only('SINCE 2019'))

    def test_since_2000(self):
        self.assertTrue(_year_only('since 2000'))

    def test_since_1970(self):
        self.assertTrue(_year_only('since 1970'))


# ============================================================================
# Part A — Preposition: "by"
# ============================================================================
