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


class TestProseYearBefore(unittest.TestCase):
    """Preposition 'before' preceding a 4-digit year."""

    def test_before_2004_nonempty(self):
        self.assertTrue(extract_explicit_dates('before 2004'))

    def test_before_2004_type(self):
        self.assertTrue(_year_only('before 2004'))

    def test_before_2004_key(self):
        self.assertTrue(_has_key('before 2004', '2004'))

    def test_before_sentence(self):
        self.assertTrue(_year_only('it happened before 2010'))

    def test_before_sentence_key(self):
        result = extract_explicit_dates('it happened before 2010')
        self.assertIn('2010', result)

    def test_before_value(self):
        result = extract_explicit_dates('before 2004')
        self.assertEqual(result.get('2004'), 'YEAR_ONLY')

    def test_before_uppercase(self):
        self.assertTrue(_year_only('BEFORE 2004'))

    def test_before_2000(self):
        self.assertTrue(_year_only('before 2000'))

    def test_before_1990(self):
        self.assertTrue(_year_only('before 1990'))


# ============================================================================
# Part A — Preposition: "after"
# ============================================================================
