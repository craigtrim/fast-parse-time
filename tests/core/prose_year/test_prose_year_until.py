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


class TestProseYearUntil(unittest.TestCase):
    """Preposition 'until' preceding a 4-digit year."""

    def test_until_2030_nonempty(self):
        self.assertTrue(extract_explicit_dates('until 2030'))

    def test_until_2030_type(self):
        self.assertTrue(_year_only('until 2030'))

    def test_until_2030_key(self):
        self.assertTrue(_has_key('until 2030', '2030'))

    def test_until_sentence(self):
        self.assertTrue(_year_only('the program ran until 2020'))

    def test_until_sentence_key(self):
        result = extract_explicit_dates('the program ran until 2020')
        self.assertIn('2020', result)

    def test_until_value(self):
        result = extract_explicit_dates('until 2030')
        self.assertEqual(result.get('2030'), 'YEAR_ONLY')

    def test_until_uppercase(self):
        self.assertTrue(_year_only('UNTIL 2030'))

    def test_until_2005(self):
        self.assertTrue(_year_only('until 2005'))

    def test_until_1999(self):
        self.assertTrue(_year_only('until 1999'))


# ============================================================================
# Part A — Preposition: "before"
# ============================================================================
