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


class TestProseYearBy(unittest.TestCase):
    """Preposition 'by' preceding a 4-digit year."""

    def test_by_2024_nonempty(self):
        self.assertTrue(extract_explicit_dates('by 2024'))

    def test_by_2024_type(self):
        self.assertTrue(_year_only('by 2024'))

    def test_by_2024_key(self):
        self.assertTrue(_has_key('by 2024', '2024'))

    def test_by_2030_key(self):
        self.assertTrue(_has_key('by 2030', '2030'))

    def test_by_sentence(self):
        self.assertTrue(_year_only('complete the project by 2025'))

    def test_by_sentence_key(self):
        result = extract_explicit_dates('complete the project by 2025')
        self.assertIn('2025', result)

    def test_by_value(self):
        result = extract_explicit_dates('by 2024')
        self.assertEqual(result.get('2024'), 'YEAR_ONLY')

    def test_by_uppercase(self):
        self.assertTrue(_year_only('BY 2024'))

    def test_by_2010(self):
        self.assertTrue(_year_only('by 2010'))


# ============================================================================
# Part A — Preposition: "until"
# ============================================================================
