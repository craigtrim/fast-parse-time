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


class TestProseYearBoundary(unittest.TestCase):
    """Edge cases at year boundary limits."""

    def test_year_1950_valid(self):
        self.assertTrue(_year_only('in 1950'))

    def test_year_1927_valid(self):
        """Near MIN_YEAR (approx 1926)."""
        self.assertTrue(_year_only('in 1927'))

    def test_year_2035_valid(self):
        """Near MAX_YEAR (approx 2036)."""
        self.assertTrue(_year_only('in 2035'))

    def test_year_1800_invalid(self):
        """Before MIN_YEAR — should NOT be returned."""
        result = extract_explicit_dates('in 1800')
        self.assertNotIn('1800', result)

    def test_year_2100_invalid(self):
        """After MAX_YEAR — should NOT be returned."""
        result = extract_explicit_dates('in 2100')
        self.assertNotIn('2100', result)

    def test_year_1900_invalid(self):
        """1900 is below MIN_YEAR (≈1926) — should NOT be returned."""
        result = extract_explicit_dates('in 1900')
        self.assertNotIn('1900', result)

    def test_year_2040_invalid(self):
        """2040 is above MAX_YEAR (≈2036) — should NOT be returned."""
        result = extract_explicit_dates('in 2040')
        self.assertNotIn('2040', result)

    def test_boundary_year_1970(self):
        self.assertTrue(_year_only('in 1970'))

    def test_boundary_year_2010(self):
        self.assertTrue(_year_only('in 2010'))


# ============================================================================
# Part A — Negative / non-match cases (bare years without preposition)
# ============================================================================
