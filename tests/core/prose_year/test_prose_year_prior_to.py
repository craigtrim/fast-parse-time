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


class TestProseYearPriorTo(unittest.TestCase):
    """Multi-word preposition 'prior to' preceding a 4-digit year."""

    def test_prior_to_2010_nonempty(self):
        self.assertTrue(extract_explicit_dates('prior to 2010'))

    def test_prior_to_2010_type(self):
        self.assertTrue(_year_only('prior to 2010'))

    def test_prior_to_2010_key(self):
        self.assertTrue(_has_key('prior to 2010', '2010'))

    def test_prior_to_sentence(self):
        self.assertTrue(_year_only('events prior to 2010 are excluded'))

    def test_prior_to_sentence_key(self):
        result = extract_explicit_dates('events prior to 2010 are excluded')
        self.assertIn('2010', result)

    def test_prior_to_value(self):
        result = extract_explicit_dates('prior to 2010')
        self.assertEqual(result.get('2010'), 'YEAR_ONLY')

    def test_prior_to_uppercase(self):
        self.assertTrue(_year_only('PRIOR TO 2010'))

    def test_prior_to_2000(self):
        self.assertTrue(_year_only('prior to 2000'))

    def test_prior_to_1990(self):
        self.assertTrue(_year_only('prior to 1990'))


# ============================================================================
# Part A — Result shape / key format
# ============================================================================
