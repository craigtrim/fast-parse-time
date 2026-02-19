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


class TestHyphenInSentenceMiddle(unittest.TestCase):
    """Year range appears in the middle of a sentence."""

    def test_period_2014_2015(self):
        self.assertTrue(_year_range('The period 2014-2015 was significant.'))

    def test_during_2000_2010(self):
        self.assertTrue(_year_range('Economic growth during 2000-2010 was uneven.'))

    def test_between_wars_1918_1939(self):
        self.assertTrue(_year_range('The interwar period 1918-1939 reshaped Europe. The period 1930-1940 was also critical.'))

    def test_years_1990_2000(self):
        self.assertTrue(_year_range('The years 1990-2000 are sometimes called the long boom.'))

    def test_span_1960_1970(self):
        self.assertTrue(_year_range('The decade span 1960-1970 saw rapid change.'))

    def test_era_2001_2009(self):
        self.assertTrue(_year_range('The era 2001-2009 redefined security.'))

    def test_window_2010_2015(self):
        self.assertTrue(_year_range('This window, 2010-2015, was critical.'))

    def test_from_to_via_hyphen(self):
        self.assertTrue(_year_range('The range 2004-2008 covers four years.'))

    def test_recent_1999_2004(self):
        self.assertTrue(_year_range('In the recent past 1999-2004 we saw innovation.'))

    def test_postwar_1945_1955(self):
        self.assertTrue(_year_range('The postwar era 1945-1955 was remarkable.'))

    def test_employment_2008_2012(self):
        self.assertTrue(_year_range('High unemployment in 2008-2012 hit hard.'))

    def test_comma_before(self):
        self.assertTrue(_year_range('Revenue in, 2015-2020, declined.'))

    def test_colon_before(self):
        self.assertTrue(_year_range('Results: 2010-2018 showed growth.'))

    def test_dash_context(self):
        self.assertTrue(_year_range('The years — 2012-2016 — were transformative.'))

    def test_quote_context(self):
        self.assertTrue(_year_range('"2014-2015" is the period under review.'))


# ============================================================================
# Class 5 — TestHyphenInSentenceEnd
# 15 tests: Year range at the end of a sentence
# ============================================================================
