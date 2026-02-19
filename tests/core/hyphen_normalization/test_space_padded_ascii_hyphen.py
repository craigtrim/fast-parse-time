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


class TestSpacePaddedAsciiHyphen(unittest.TestCase):
    """ASCII hyphen flanked by one or more spaces."""

    def test_single_space_2014_2015(self):
        self.assertTrue(_yr('2014 - 2015'))

    def test_single_space_2000_2010(self):
        self.assertTrue(_yr('2000 - 2010'))

    def test_single_space_1939_1945(self):
        self.assertTrue(_yr('1939 - 1945'))

    def test_single_space_consecutive(self):
        self.assertTrue(_yr('2019 - 2020'))

    def test_single_space_in_sentence(self):
        self.assertTrue(_yr('The period 2014 - 2015 was notable.'))

    def test_single_space_reversed_not_range(self):
        self.assertTrue(_no_yr('2015 - 2014'))

    def test_single_space_same_year_not_range(self):
        self.assertTrue(_no_yr('2014 - 2014'))

    def test_single_space_out_of_range(self):
        self.assertTrue(_no_yr('1800 - 1900'))

    def test_key_is_ascii_no_spaces(self):
        """Key should be '2014-2015', not '2014 - 2015'."""
        r = extract_explicit_dates('2014 - 2015') or {}
        self.assertIn('2014-2015', r)
        self.assertNotIn('2014 - 2015', r)

    def test_value_is_year_range(self):
        r = extract_explicit_dates('2014 - 2015') or {}
        self.assertEqual(r.get('2014-2015'), 'YEAR_RANGE')

    def test_double_space(self):
        self.assertTrue(_yr('2014  -  2015'))

    def test_triple_space(self):
        self.assertTrue(_yr('2014   -   2015'))

    def test_tab_around_hyphen(self):
        self.assertTrue(_yr('2014\t-\t2015'))

    def test_tab_before_only(self):
        self.assertTrue(_yr('2014\t- 2015'))

    def test_space_before_only(self):
        """Asymmetric: space before, no space after."""
        self.assertTrue(_yr('2014 -2015'))

    def test_space_after_only(self):
        """Asymmetric: no space before, space after."""
        self.assertTrue(_yr('2014- 2015'))

    def test_multiple_spaced_ranges(self):
        r = extract_explicit_dates('2000 - 2010 and 2014 - 2015') or {}
        self.assertIn('2000-2010', r)
        self.assertIn('2014-2015', r)

    def test_spaced_and_compact_same_text(self):
        """One compact ASCII range, one spaced range in same text."""
        r = extract_explicit_dates('2000-2010 and 2014 - 2015') or {}
        self.assertIn('2000-2010', r)
        self.assertIn('2014-2015', r)

    def test_spaced_range_in_parens(self):
        self.assertTrue(_yr('(2014 - 2015)'))

    def test_spaced_range_trailing_period(self):
        self.assertTrue(_yr('2014 - 2015.'))


# ============================================================================
# Class 8 — TestExtremeWhitespace
# 15 tests: extreme/unusual whitespace combos
# ============================================================================
