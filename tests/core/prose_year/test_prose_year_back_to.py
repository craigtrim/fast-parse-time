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


class TestProseYearBackTo(unittest.TestCase):
    """Multi-word preposition 'back to' preceding a 4-digit year."""

    def test_back_to_1998_nonempty(self):
        self.assertTrue(extract_explicit_dates('back to 1998'))

    def test_back_to_1998_type(self):
        self.assertTrue(_year_only('back to 1998'))

    def test_back_to_1998_key(self):
        self.assertTrue(_has_key('back to 1998', '1998'))

    def test_dating_back_to_1998(self):
        """Extended form: 'dating back to 1998'."""
        self.assertTrue(_year_only('dating back to 1998'))

    def test_dating_back_to_1998_key(self):
        result = extract_explicit_dates('dating back to 1998')
        self.assertIn('1998', result)

    def test_back_to_sentence(self):
        self.assertTrue(_year_only('the tradition goes back to 1950'))

    def test_back_to_sentence_key(self):
        result = extract_explicit_dates('the tradition goes back to 1950')
        self.assertIn('1950', result)

    def test_back_to_value(self):
        result = extract_explicit_dates('back to 1998')
        self.assertEqual(result.get('1998'), 'YEAR_ONLY')

    def test_back_to_uppercase(self):
        self.assertTrue(_year_only('BACK TO 1998'))

    def test_back_to_2000(self):
        self.assertTrue(_year_only('back to 2000'))


# ============================================================================
# Part A — Preposition: "prior to"  (multi-word)
# ============================================================================
