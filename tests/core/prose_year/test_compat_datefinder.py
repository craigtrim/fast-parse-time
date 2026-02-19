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


class TestCompatDatefinder(unittest.TestCase):
    """Compatibility tests matching original datefinder behaviour from issue #24."""

    def test_year_in_sentence_2004(self):
        """'...title in 2004.' — primary compat case."""
        result = extract_explicit_dates('...title in 2004.')
        self.assertIn('2004', result)

    def test_year_in_sentence_2004_type(self):
        result = extract_explicit_dates('...title in 2004.')
        self.assertEqual(result.get('2004'), 'YEAR_ONLY')

    def test_year_in_sentence_2008(self):
        """'...traumatized on the sets in 2008.' — second compat case."""
        result = extract_explicit_dates('...traumatized on the sets in 2008.')
        self.assertIn('2008', result)

    def test_year_in_sentence_2008_type(self):
        result = extract_explicit_dates('...traumatized on the sets in 2008.')
        self.assertEqual(result.get('2008'), 'YEAR_ONLY')

    def test_year_range_compat(self):
        """YEAR_RANGE compatibility: 2014-2015."""
        result = extract_explicit_dates('2014-2015')
        self.assertEqual(result.get('2014-2015'), 'YEAR_RANGE')


# ============================================================================
# Extended coverage — misc multi-prep and combined scenarios
# ============================================================================
