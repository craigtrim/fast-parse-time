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


class TestYearRangeNegative(unittest.TestCase):
    """Cases that should NOT produce YEAR_RANGE."""

    def test_hyphen_month_year_not_year_range(self):
        """'Oct-2023' should be MONTH_YEAR not YEAR_RANGE (issue #21 handles this)."""
        result = extract_explicit_dates('Oct-2023')
        self.assertNotEqual(result.get('Oct-2023'), 'YEAR_RANGE')

    def test_full_date_not_year_range(self):
        """A full date like '2024-03-15' should not become YEAR_RANGE."""
        result = extract_explicit_dates('2024-03-15')
        self.assertNotIn('YEAR_RANGE', result.values())

    def test_plain_text_no_range(self):
        """No years in text — no YEAR_RANGE."""
        result = extract_explicit_dates('hello world')
        self.assertNotIn('YEAR_RANGE', result.values())

    def test_single_year_no_range(self):
        """Single year is not a range."""
        result = extract_explicit_dates('2015')
        self.assertNotIn('YEAR_RANGE', result.values())


# ============================================================================
# Part B — YEAR_RANGE: in sentences
# ============================================================================
