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


class TestProseYearFrom(unittest.TestCase):
    """Preposition 'from' preceding a single 4-digit year (no 'to' clause)."""

    def test_from_2019_nonempty(self):
        self.assertTrue(extract_explicit_dates('from 2019'))

    def test_from_2019_nonempty_contains_year_only(self):
        """Result should contain a YEAR_ONLY entry (at minimum)."""
        result = extract_explicit_dates('from 2019')
        self.assertTrue(any(v in ('YEAR_ONLY', 'YEAR_RANGE') for v in result.values()))

    def test_from_2019_key(self):
        self.assertTrue(_has_key('from 2019', '2019'))

    def test_from_sentence(self):
        result = extract_explicit_dates('data available from 2015')
        self.assertTrue(result)

    def test_from_sentence_key(self):
        result = extract_explicit_dates('data available from 2015')
        self.assertIn('2015', result)

    def test_from_uppercase(self):
        result = extract_explicit_dates('FROM 2019')
        self.assertTrue(result)

    def test_from_2000(self):
        self.assertTrue(extract_explicit_dates('from 2000'))

    def test_from_1998(self):
        self.assertTrue(extract_explicit_dates('from 1998'))


# ============================================================================
# Part A — Preposition: "through"
# ============================================================================
