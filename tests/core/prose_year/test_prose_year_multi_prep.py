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


class TestProseYearMultiPrep(unittest.TestCase):
    """Multiple prepositions / years in single input."""

    def test_in_and_since(self):
        result = extract_explicit_dates('opened in 2000 and has been running since 2005')
        self.assertIn('2000', result)
        self.assertIn('2005', result)

    def test_before_and_after(self):
        result = extract_explicit_dates('projects before 2010 and after 2015')
        self.assertIn('2010', result)
        self.assertIn('2015', result)

    def test_until_and_from(self):
        result = extract_explicit_dates('from 2010 until 2020')
        self.assertIn('2010', result)
        self.assertIn('2020', result)

    def test_during_and_since(self):
        result = extract_explicit_dates('during 2020 and since 2021')
        self.assertIn('2020', result)
        self.assertIn('2021', result)

    def test_circa_and_around(self):
        result = extract_explicit_dates('circa 2000 or around 2010')
        self.assertIn('2000', result)
        self.assertIn('2010', result)

    def test_by_and_before(self):
        result = extract_explicit_dates('by 2025 before 2030')
        self.assertIn('2025', result)
        self.assertIn('2030', result)

    def test_prior_to_and_after(self):
        result = extract_explicit_dates('prior to 2010 or after 2015')
        self.assertIn('2010', result)
        self.assertIn('2015', result)

    def test_back_to_and_in(self):
        result = extract_explicit_dates('dating back to 1998 and in 2004')
        self.assertIn('1998', result)
        self.assertIn('2004', result)

    def test_as_of_and_until(self):
        result = extract_explicit_dates('as of 2020 until 2025')
        self.assertIn('2020', result)
        self.assertIn('2025', result)

    def test_all_types_same_year(self):
        """Same year appearing twice with different prepositions — key appears once."""
        result = extract_explicit_dates('in 2004 and after 2004')
        self.assertIn('2004', result)
        self.assertEqual(result.get('2004'), 'YEAR_ONLY')


# ============================================================================
# Additional single-preposition variety tests to reach 250+
# ============================================================================
