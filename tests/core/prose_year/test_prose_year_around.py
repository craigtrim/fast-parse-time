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


class TestProseYearAround(unittest.TestCase):
    """Preposition 'around' preceding a 4-digit year."""

    def test_around_2019_nonempty(self):
        self.assertTrue(extract_explicit_dates('around 2019'))

    def test_around_2019_type(self):
        self.assertTrue(_year_only('around 2019'))

    def test_around_2019_key(self):
        self.assertTrue(_has_key('around 2019', '2019'))

    def test_around_sentence(self):
        self.assertTrue(_year_only('the trend started around 2012'))

    def test_around_sentence_key(self):
        result = extract_explicit_dates('the trend started around 2012')
        self.assertIn('2012', result)

    def test_around_value(self):
        result = extract_explicit_dates('around 2019')
        self.assertEqual(result.get('2019'), 'YEAR_ONLY')

    def test_around_uppercase(self):
        self.assertTrue(_year_only('AROUND 2019'))

    def test_around_2000(self):
        self.assertTrue(_year_only('around 2000'))

    def test_around_1985(self):
        self.assertTrue(_year_only('around 1985'))


# ============================================================================
# Part A — Preposition: "from"
# ============================================================================
