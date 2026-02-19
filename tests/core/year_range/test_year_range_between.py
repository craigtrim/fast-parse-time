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


class TestYearRangeBetween(unittest.TestCase):
    """'between YYYY and YYYY' prose form returns YEAR_RANGE."""

    def test_between_2010_and_2020_nonempty(self):
        self.assertTrue(extract_explicit_dates('between 2010 and 2020'))

    def test_between_2010_and_2020_type(self):
        self.assertTrue(_year_range('between 2010 and 2020'))

    def test_between_2010_and_2020_has_range_entry(self):
        result = extract_explicit_dates('between 2010 and 2020')
        self.assertTrue(any(v == 'YEAR_RANGE' for v in result.values()))

    def test_between_2000_and_2010(self):
        self.assertTrue(_year_range('between 2000 and 2010'))

    def test_between_1990_and_2000(self):
        self.assertTrue(_year_range('between 1990 and 2000'))

    def test_between_2004_and_2008(self):
        self.assertTrue(_year_range('between 2004 and 2008'))

    def test_in_sentence(self):
        self.assertTrue(_year_range('born between 1950 and 1960'))

    def test_in_sentence_has_range(self):
        result = extract_explicit_dates('born between 1950 and 1960')
        self.assertTrue(any(v == 'YEAR_RANGE' for v in result.values()))

    def test_uppercase_between(self):
        self.assertTrue(_year_range('BETWEEN 2010 AND 2020'))

    def test_between_reversed_not_range(self):
        """'between 2020 and 2010' — inverted."""
        result = extract_explicit_dates('between 2020 and 2010')
        self.assertNotIn('YEAR_RANGE', result.values())

    def test_result_is_dict(self):
        result = extract_explicit_dates('between 2010 and 2020')
        self.assertIsInstance(result, dict)

    def test_result_nonempty(self):
        result = extract_explicit_dates('between 2010 and 2020')
        self.assertTrue(len(result) >= 1)


# ============================================================================
# Part B — YEAR_RANGE boundary and negative
# ============================================================================
