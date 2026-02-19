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


class TestProseYearDuring(unittest.TestCase):
    """Preposition 'during' preceding a 4-digit year."""

    def test_during_2020_nonempty(self):
        self.assertTrue(extract_explicit_dates('during 2020'))

    def test_during_2020_type(self):
        self.assertTrue(_year_only('during 2020'))

    def test_during_2020_key(self):
        self.assertTrue(_has_key('during 2020', '2020'))

    def test_during_sentence(self):
        self.assertTrue(_year_only('production halted during 2020'))

    def test_during_sentence_key(self):
        result = extract_explicit_dates('production halted during 2020')
        self.assertIn('2020', result)

    def test_during_value(self):
        result = extract_explicit_dates('during 2020')
        self.assertEqual(result.get('2020'), 'YEAR_ONLY')

    def test_during_uppercase(self):
        self.assertTrue(_year_only('DURING 2020'))

    def test_during_1945(self):
        self.assertTrue(_year_only('during 1945'))

    def test_during_2008(self):
        self.assertTrue(_year_only('during 2008'))


# ============================================================================
# Part A — Preposition: "circa"
# ============================================================================
