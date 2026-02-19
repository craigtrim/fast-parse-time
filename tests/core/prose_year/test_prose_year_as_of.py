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


class TestProseYearAsOf(unittest.TestCase):
    """Multi-word preposition 'as of' preceding a 4-digit year."""

    def test_as_of_2004_nonempty(self):
        self.assertTrue(extract_explicit_dates('as of 2004'))

    def test_as_of_2004_type(self):
        self.assertTrue(_year_only('as of 2004'))

    def test_as_of_2004_key(self):
        self.assertTrue(_has_key('as of 2004', '2004'))

    def test_as_of_sentence(self):
        self.assertTrue(_year_only('as of 2023, the regulation applies'))

    def test_as_of_sentence_key(self):
        result = extract_explicit_dates('as of 2023, the regulation applies')
        self.assertIn('2023', result)

    def test_as_of_value(self):
        result = extract_explicit_dates('as of 2004')
        self.assertEqual(result.get('2004'), 'YEAR_ONLY')

    def test_as_of_uppercase(self):
        self.assertTrue(_year_only('AS OF 2004'))

    def test_as_of_2010(self):
        self.assertTrue(_year_only('as of 2010'))

    def test_as_of_2020(self):
        self.assertTrue(_year_only('as of 2020'))


# ============================================================================
# Part A — Preposition: "back to"  (multi-word)
# ============================================================================
