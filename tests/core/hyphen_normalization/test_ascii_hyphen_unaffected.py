#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""TDD red-team tests for hyphen normalization (issue #44).

275 test cases probing Unicode dash variants, space-padded hyphens,
asymmetric spacing, combined forms, and normalization side-effects.

These tests define the correct behaviour AFTER #44 is implemented.
Most will fail until normalization is in place.

Related GitHub Issue:
    #44 - feat: Normalize hyphen-like characters and space-padded hyphens before parsing
    https://github.com/craigtrim/fast-parse-time/issues/44
    Prerequisite for: #40
"""

import unittest

from fast_parse_time import extract_explicit_dates

# ---------------------------------------------------------------------------
# Unicode dash constants (named for readability in test bodies)
# ---------------------------------------------------------------------------
EN  = '\u2013'   # EN DASH
EM  = '\u2014'   # EM DASH
HY  = '\u2010'   # HYPHEN (proper)
NBH = '\u2011'   # NON-BREAKING HYPHEN
FIG = '\u2012'   # FIGURE DASH
HB  = '\u2015'   # HORIZONTAL BAR
MIN = '\u2212'   # MINUS SIGN
SHY = '\ufe63'   # SMALL HYPHEN-MINUS
FWH = '\uff0d'   # FULLWIDTH HYPHEN-MINUS
NBSP= '\u00a0'   # NON-BREAKING SPACE
ZWS = '\u200b'   # ZERO-WIDTH SPACE
SHY2= '\u00ad'   # SOFT HYPHEN


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _yr(text) -> bool:
    """Return True if at least one YEAR_RANGE entry exists."""
    try:
        r = extract_explicit_dates(text)
        return r is not None and 'YEAR_RANGE' in r.values()
    except Exception:
        return False


def _no_yr(text) -> bool:
    """Return True if no YEAR_RANGE entry exists."""
    try:
        r = extract_explicit_dates(text)
        return r is None or 'YEAR_RANGE' not in r.values()
    except Exception:
        return True


def _key(text: str, k: str) -> bool:
    """Return True if k maps to YEAR_RANGE."""
    try:
        r = extract_explicit_dates(text)
        return r is not None and r.get(k) == 'YEAR_RANGE'
    except Exception:
        return False


def _safe(text) -> bool:
    """Return True if call does not raise."""
    try:
        extract_explicit_dates(text)
        return True
    except Exception:
        return False


# ============================================================================
# Class 1 — TestEnDashBare
# 20 tests: bare YYYY–YYYY (en dash, U+2013)
# ============================================================================


class TestAsciiHyphenUnaffected(unittest.TestCase):
    """Pre-existing ASCII hyphen behavior must be preserved after normalization is added."""

    def test_ascii_2014_2015_still_works(self):
        self.assertTrue(_yr('2014-2015'))

    def test_ascii_2000_2010_still_works(self):
        self.assertTrue(_yr('2000-2010'))

    def test_ascii_1939_1945_still_works(self):
        self.assertTrue(_yr('1939-1945'))

    def test_ascii_reversed_still_fails(self):
        self.assertTrue(_no_yr('2015-2014'))

    def test_ascii_same_year_still_fails(self):
        self.assertTrue(_no_yr('2014-2014'))

    def test_ascii_out_of_range_still_fails(self):
        self.assertTrue(_no_yr('1800-1900'))

    def test_ascii_from_to_still_works(self):
        self.assertTrue(_yr('from 2004 to 2008'))

    def test_ascii_between_and_still_works(self):
        self.assertTrue(_yr('between 2010 and 2020'))

    def test_ascii_in_sentence_still_works(self):
        self.assertTrue(_yr('The period 2014-2015 was significant.'))

    def test_ascii_key_format_unchanged(self):
        r = extract_explicit_dates('2014-2015') or {}
        self.assertEqual(r.get('2014-2015'), 'YEAR_RANGE')

    def test_hyphenated_word_no_regression(self):
        """Compound words with ASCII hyphens should never produce YEAR_RANGE."""
        self.assertTrue(_no_yr('mother-in-law'))

    def test_isbn_no_regression(self):
        self.assertTrue(_no_yr('978-3-16'))

    def test_multiple_ascii_ranges_no_regression(self):
        r = extract_explicit_dates('2000-2010 and 2014-2015') or {}
        self.assertIn('2000-2010', r)
        self.assertIn('2014-2015', r)

    def test_prose_year_only_no_regression(self):
        r = extract_explicit_dates('in 2024') or {}
        self.assertIn('YEAR_ONLY', r.values())

    def test_written_date_no_regression(self):
        """March 2024: written date parsing not affected by normalization."""
        self.assertTrue(_safe('March 2024'))


# ============================================================================
# Class 13 — TestSoftAndInvisibleChars
# 10 tests: soft hyphen, zero-width space, BOM — should not produce YEAR_RANGE
# ============================================================================
