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


class TestProseYearThrough(unittest.TestCase):
    """Preposition 'through' preceding a 4-digit year."""

    def test_through_2019_nonempty(self):
        self.assertTrue(extract_explicit_dates('through 2019'))

    def test_through_2019_type(self):
        self.assertTrue(_year_only('through 2019'))

    def test_through_2019_key(self):
        self.assertTrue(_has_key('through 2019', '2019'))

    def test_through_sentence(self):
        self.assertTrue(_year_only('the war lasted through 1945'))

    def test_through_sentence_key(self):
        result = extract_explicit_dates('the war lasted through 1945')
        self.assertIn('1945', result)

    def test_through_value(self):
        result = extract_explicit_dates('through 2019')
        self.assertEqual(result.get('2019'), 'YEAR_ONLY')

    def test_through_uppercase(self):
        self.assertTrue(_year_only('THROUGH 2019'))

    def test_through_2005(self):
        self.assertTrue(_year_only('through 2005'))

    def test_through_1990(self):
        self.assertTrue(_year_only('through 1990'))


# ============================================================================
# Part A — Preposition: "as of"  (multi-word)
# ============================================================================
