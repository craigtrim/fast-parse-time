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


class TestProseYearResultShape(unittest.TestCase):
    """Result dict: bare year string as key, YEAR_ONLY as value."""

    def test_key_is_bare_year_not_preposition(self):
        result = extract_explicit_dates('in 2004')
        self.assertIn('2004', result)
        self.assertNotIn('in 2004', result)

    def test_key_is_bare_year_since(self):
        result = extract_explicit_dates('since 2019')
        self.assertIn('2019', result)
        self.assertNotIn('since 2019', result)

    def test_key_is_bare_year_by(self):
        result = extract_explicit_dates('by 2024')
        self.assertIn('2024', result)
        self.assertNotIn('by 2024', result)

    def test_key_is_bare_year_as_of(self):
        result = extract_explicit_dates('as of 2004')
        self.assertIn('2004', result)
        self.assertNotIn('as of 2004', result)

    def test_key_is_bare_year_prior_to(self):
        result = extract_explicit_dates('prior to 2010')
        self.assertIn('2010', result)
        self.assertNotIn('prior to 2010', result)

    def test_value_is_string_not_enum(self):
        result = extract_explicit_dates('in 2004')
        self.assertIsInstance(result.get('2004'), str)

    def test_result_is_dict(self):
        result = extract_explicit_dates('in 2004')
        self.assertIsInstance(result, dict)

    def test_result_not_none(self):
        result = extract_explicit_dates('in 2004')
        self.assertIsNotNone(result)

    def test_multiple_prepositions_both_years_present(self):
        """'in 2004 and before 2010' should yield both years."""
        result = extract_explicit_dates('the data spans in 2004 and before 2010')
        self.assertIn('2004', result)
        self.assertIn('2010', result)

    def test_multiple_prepositions_both_year_only(self):
        result = extract_explicit_dates('since 2010 until 2020')
        self.assertIn('2010', result)
        self.assertIn('2020', result)


# ============================================================================
# Part A — Boundary years
# ============================================================================
