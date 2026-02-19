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


class TestYearRangeBoundary(unittest.TestCase):
    """Boundary conditions for YEAR_RANGE."""

    def test_hyphen_range_in_valid_range(self):
        self.assertTrue(_year_range('1960-1970'))

    def test_hyphen_range_at_lower_boundary(self):
        """Years near MIN_YEAR."""
        self.assertTrue(_year_range('1930-1940'))

    def test_hyphen_range_at_upper_boundary(self):
        """Years near MAX_YEAR."""
        self.assertTrue(_year_range('2030-2035'))

    def test_hyphen_range_one_year_out_of_range(self):
        """If start year is out of range — no YEAR_RANGE expected."""
        result = extract_explicit_dates('1800-2010')
        self.assertNotIn('YEAR_RANGE', result.values())

    def test_from_range_valid(self):
        self.assertTrue(_year_range('from 1960 to 1970'))

    def test_between_range_valid(self):
        self.assertTrue(_year_range('between 1960 and 1970'))

    def test_large_span_hyphen(self):
        """50-year span."""
        self.assertTrue(_year_range('1970-2020'))

    def test_small_span_hyphen(self):
        """1-year span."""
        self.assertTrue(_year_range('2019-2020'))


# ============================================================================
# Part B — YEAR_RANGE: negative cases
# ============================================================================
