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


class TestYearRangeFrom(unittest.TestCase):
    """'from YYYY to YYYY' prose form returns YEAR_RANGE."""

    def test_from_2004_to_2008_nonempty(self):
        self.assertTrue(extract_explicit_dates('from 2004 to 2008'))

    def test_from_2004_to_2008_type(self):
        self.assertTrue(_year_range('from 2004 to 2008'))

    def test_from_2004_to_2008_has_range_entry(self):
        result = extract_explicit_dates('from 2004 to 2008')
        self.assertTrue(any(v == 'YEAR_RANGE' for v in result.values()))

    def test_from_2000_to_2010(self):
        self.assertTrue(_year_range('from 2000 to 2010'))

    def test_from_1990_to_2000(self):
        self.assertTrue(_year_range('from 1990 to 2000'))

    def test_from_2010_to_2020(self):
        self.assertTrue(_year_range('from 2010 to 2020'))

    def test_in_sentence(self):
        self.assertTrue(_year_range('he worked there from 2005 to 2015'))

    def test_in_sentence_has_range(self):
        result = extract_explicit_dates('he worked there from 2005 to 2015')
        self.assertTrue(any(v == 'YEAR_RANGE' for v in result.values()))

    def test_uppercase_from(self):
        self.assertTrue(_year_range('FROM 2004 TO 2008'))

    def test_from_reversed_not_range(self):
        """'from 2008 to 2004' — inverted, should not be YEAR_RANGE."""
        result = extract_explicit_dates('from 2008 to 2004')
        self.assertNotIn('YEAR_RANGE', result.values())

    def test_result_is_dict(self):
        result = extract_explicit_dates('from 2004 to 2008')
        self.assertIsInstance(result, dict)

    def test_result_nonempty(self):
        result = extract_explicit_dates('from 2004 to 2008')
        self.assertTrue(len(result) >= 1)


# ============================================================================
# Part B — YEAR_RANGE: "between YYYY and YYYY"
# ============================================================================
