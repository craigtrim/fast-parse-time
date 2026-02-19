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


class TestProseYearCirca(unittest.TestCase):
    """Preposition 'circa' preceding a 4-digit year."""

    def test_circa_2004_nonempty(self):
        self.assertTrue(extract_explicit_dates('circa 2004'))

    def test_circa_2004_type(self):
        self.assertTrue(_year_only('circa 2004'))

    def test_circa_2004_key(self):
        self.assertTrue(_has_key('circa 2004', '2004'))

    def test_circa_sentence(self):
        self.assertTrue(_year_only('the artifact dates to circa 1950'))

    def test_circa_sentence_key(self):
        result = extract_explicit_dates('the artifact dates to circa 1950')
        self.assertIn('1950', result)

    def test_circa_value(self):
        result = extract_explicit_dates('circa 2004')
        self.assertEqual(result.get('2004'), 'YEAR_ONLY')

    def test_circa_uppercase(self):
        self.assertTrue(_year_only('CIRCA 2004'))

    def test_circa_abbreviation_c_dot(self):
        """'c. 2004' is out of scope — should not require support."""
        pass  # intentionally excluded per issue spec

    def test_circa_1970(self):
        self.assertTrue(_year_only('circa 1970'))

    def test_circa_2019(self):
        self.assertTrue(_year_only('circa 2019'))


# ============================================================================
# Part A — Preposition: "around"
# ============================================================================
