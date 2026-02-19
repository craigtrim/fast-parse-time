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


class TestHyphenInSentenceEnd(unittest.TestCase):
    """Year range appears at the end of a sentence."""

    def test_ref_2014_2015(self):
        self.assertTrue(_year_range('See the data for 2014-2015'))

    def test_covers_2000_2010(self):
        self.assertTrue(_year_range('The study covers 2000-2010'))

    def test_relevant_1990_2000(self):
        self.assertTrue(_year_range('Data is most relevant for 1990-2000'))

    def test_analysis_1960_1970(self):
        self.assertTrue(_year_range('The analysis spans 1960-1970'))

    def test_focus_2015_2020(self):
        self.assertTrue(_year_range('The report focuses on 2015-2020'))

    def test_period_2008_2012(self):
        self.assertTrue(_year_range('The crisis period: 2008-2012'))

    def test_refer_1950_1960(self):
        self.assertTrue(_year_range('All figures refer to 1950-1960'))

    def test_war_years_1939_1945(self):
        self.assertTrue(_year_range('These are the war years 1939-1945'))

    def test_boom_1945_1955(self):
        self.assertTrue(_year_range('The boom years were 1945-1955'))

    def test_dot_com_1995_2001(self):
        self.assertTrue(_year_range('Peak dot-com era: 1995-2001'))

    def test_decade_2010_2020(self):
        self.assertTrue(_year_range('The last full decade was 2010-2020'))

    def test_trailing_period(self):
        self.assertTrue(_year_range('Data covers 2014-2015.'))

    def test_trailing_comma(self):
        self.assertTrue(_year_range('Data covers 2014-2015,'))

    def test_trailing_question(self):
        self.assertTrue(_year_range('Does it cover 2014-2015?'))

    def test_trailing_exclamation(self):
        self.assertTrue(_year_range('What a span: 2014-2015!'))


# ============================================================================
# Class 6 — TestHyphenWithSurroundingPunctuation
# 20 tests: Year range surrounded by various punctuation
# ============================================================================
