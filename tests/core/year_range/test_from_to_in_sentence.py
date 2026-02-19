#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""TDD tests for year-range expression extraction.

620 test cases covering:
  - True positives: YYYY-YYYY bare, from/to, between/and forms
  - False positives: same year, reversed, out-of-range, non-year numbers
  - Edge cases: boundary years, punctuation, adjacency, multiple ranges
  - Crazy inputs: None, malformed, Unicode, HTML
  - Currently-unsupported forms (en dash, spaces, abbreviated year, etc.)

Related GitHub Issue:
    #40 - feat: Parse year-range expressions (e.g., 2014-2015)
    https://github.com/craigtrim/fast-parse-time/issues/40
"""

import unittest
import pytest

from fast_parse_time import extract_explicit_dates


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _year_range(text) -> bool:
    """Return True if at least one YEAR_RANGE entry exists in the result."""
    try:
        result = extract_explicit_dates(text)
        return result is not None and 'YEAR_RANGE' in result.values()
    except Exception:
        return False


def _no_year_range(text) -> bool:
    """Return True if no YEAR_RANGE entry exists (valid false-positive check)."""
    try:
        result = extract_explicit_dates(text)
        return result is None or 'YEAR_RANGE' not in result.values()
    except Exception:
        return True


def _range_key(text: str, key: str) -> bool:
    """Return True if the specific key maps to YEAR_RANGE."""
    try:
        result = extract_explicit_dates(text)
        return result is not None and result.get(key) == 'YEAR_RANGE'
    except Exception:
        return False


def _is_dict_or_none(text) -> bool:
    """Result must be a dict or None — never raise."""
    try:
        result = extract_explicit_dates(text)
        return result is None or isinstance(result, dict)
    except Exception:
        return False


# ============================================================================
# Class 1 — TestHyphenBareValidPairs
# 40 tests: valid YYYY-YYYY pairs, bare (no surrounding text)
# ============================================================================


class TestFromToInSentence(unittest.TestCase):
    """'from YYYY to YYYY' inside longer sentences."""

    def test_he_worked_2005_to_2015(self):
        self.assertTrue(_year_range('He worked there from 2005 to 2015.'))

    def test_the_project_ran(self):
        self.assertTrue(_year_range('The project ran from 2010 to 2015.'))

    def test_the_war_lasted(self):
        self.assertTrue(_year_range('The war lasted from 1939 to 1945.'))

    def test_revenue_grew(self):
        self.assertTrue(_year_range('Revenue grew from 2000 to 2010.'))

    def test_she_studied(self):
        self.assertTrue(_year_range('She studied from 2015 to 2019.'))

    def test_population_tripled(self):
        self.assertTrue(_year_range('Population tripled from 1960 to 1980.'))

    def test_the_policy(self):
        self.assertTrue(_year_range('The policy was in effect from 2004 to 2008.'))

    def test_records_go_back(self):
        self.assertTrue(_year_range('Records go back from 1930 to 1940.'))

    def test_he_led_the_team(self):
        self.assertTrue(_year_range('He led the team from 2014 to 2016.'))

    def test_the_boom(self):
        self.assertTrue(_year_range('The boom period, from 1990 to 2000, was extraordinary.'))

    def test_with_comma(self):
        self.assertTrue(_year_range('From 2004 to 2008, growth was strong.'))

    def test_after_conjunction(self):
        self.assertTrue(_year_range('Profits rose and then from 2010 to 2015 declined.'))

    def test_at_end(self):
        self.assertTrue(_year_range('The project ran from 2010 to 2015'))

    def test_with_quotes(self):
        self.assertTrue(_year_range('"from 2004 to 2008" is the relevant period'))

    def test_with_parens(self):
        self.assertTrue(_year_range('(from 2004 to 2008) is key'))


# ============================================================================
# Class 20 — TestFromToCasing
# 15 tests: Casing variants of "from YYYY to YYYY"
# ============================================================================
