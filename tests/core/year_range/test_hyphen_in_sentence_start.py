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


class TestHyphenInSentenceStart(unittest.TestCase):
    """Year range appears at the beginning of a sentence."""

    def test_2014_2015_start(self):
        self.assertTrue(_year_range('2014-2015 was a pivotal period.'))

    def test_2000_2010_start(self):
        self.assertTrue(_year_range('2000-2010 saw dramatic changes.'))

    def test_1990_2000_start(self):
        self.assertTrue(_year_range('1990-2000 was the last decade of the century.'))

    def test_1939_1945_start(self):
        self.assertTrue(_year_range('1939-1945 marked World War II.'))

    def test_2008_2009_start(self):
        self.assertTrue(_year_range('2008-2009 were years of financial crisis.'))

    def test_2020_2021_start(self):
        self.assertTrue(_year_range('2020-2021 brought the global pandemic.'))

    def test_2010_2015_start(self):
        self.assertTrue(_year_range('2010-2015 are the years I want to highlight.'))

    def test_1960_1970_start(self):
        self.assertTrue(_year_range('1960-1970 covered the space race.'))

    def test_2001_2003_start(self):
        self.assertTrue(_year_range('2001-2003 followed the dot-com crash.'))

    def test_1950_1960_start(self):
        self.assertTrue(_year_range('1950-1960 was the postwar boom.'))

    def test_2015_2020_start(self):
        self.assertTrue(_year_range('2015-2020 shaped the modern tech landscape.'))

    def test_2024_2026_start(self):
        self.assertTrue(_year_range('2024-2026 will be years of AI growth.'))

    def test_1926_1936_start(self):
        self.assertTrue(_year_range('1926-1936 saw the Great Depression.'))

    def test_1980_1990_start(self):
        self.assertTrue(_year_range('1980-1990 is often called the decade of excess.'))

    def test_1970_1975_start(self):
        self.assertTrue(_year_range('1970-1975 were challenging economic years.'))


# ============================================================================
# Class 4 — TestHyphenInSentenceMiddle
# 15 tests: Year range embedded in the middle of a sentence
# ============================================================================
