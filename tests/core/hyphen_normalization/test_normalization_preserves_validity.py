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


class TestNormalizationPreservesValidity(unittest.TestCase):
    """After normalization, reversed/same/out-of-range rules still hold."""

    def test_en_reversed_still_fails(self):
        self.assertTrue(_no_yr(f'2020{EN}2010'))

    def test_em_reversed_still_fails(self):
        self.assertTrue(_no_yr(f'2020{EM}2010'))

    def test_hy_reversed_still_fails(self):
        self.assertTrue(_no_yr(f'2020{HY}2010'))

    def test_min_reversed_still_fails(self):
        self.assertTrue(_no_yr(f'2020{MIN}2010'))

    def test_fwh_reversed_still_fails(self):
        self.assertTrue(_no_yr(f'2020{FWH}2010'))

    def test_en_same_year_still_fails(self):
        self.assertTrue(_no_yr(f'2014{EN}2014'))

    def test_em_same_year_still_fails(self):
        self.assertTrue(_no_yr(f'2014{EM}2014'))

    def test_hy_same_year_still_fails(self):
        self.assertTrue(_no_yr(f'2014{HY}2014'))

    def test_en_below_min_still_fails(self):
        self.assertTrue(_no_yr(f'1800{EN}1900'))

    def test_em_below_min_still_fails(self):
        self.assertTrue(_no_yr(f'1800{EM}1900'))

    def test_hy_below_min_still_fails(self):
        self.assertTrue(_no_yr(f'1800{HY}1900'))

    def test_en_above_max_still_fails(self):
        self.assertTrue(_no_yr(f'2040{EN}2050'))

    def test_em_above_max_still_fails(self):
        self.assertTrue(_no_yr(f'2040{EM}2050'))

    def test_spaced_reversed_still_fails(self):
        self.assertTrue(_no_yr('2020 - 2010'))

    def test_spaced_same_year_still_fails(self):
        self.assertTrue(_no_yr('2014 - 2014'))

    def test_spaced_below_min_still_fails(self):
        self.assertTrue(_no_yr('1800 - 1900'))

    def test_spaced_above_max_still_fails(self):
        self.assertTrue(_no_yr('2040 - 2050'))

    def test_spaced_en_reversed_still_fails(self):
        self.assertTrue(_no_yr(f'2020 {EN} 2010'))

    def test_spaced_em_reversed_still_fails(self):
        self.assertTrue(_no_yr(f'2020 {EM} 2010'))

    def test_spaced_en_same_still_fails(self):
        self.assertTrue(_no_yr(f'2014 {EN} 2014'))

    def test_spaced_em_out_of_range_still_fails(self):
        self.assertTrue(_no_yr(f'1800 {EM} 1900'))

    def test_one_year_out_of_range_en_still_fails(self):
        """Start in range, end out of range."""
        self.assertTrue(_no_yr(f'2025{EN}2099'))

    def test_one_year_out_of_range_em_still_fails(self):
        self.assertTrue(_no_yr(f'2025{EM}2099'))

    def test_start_out_end_in_range_en_still_fails(self):
        """Start out of range, end in range."""
        self.assertTrue(_no_yr(f'1899{EN}2010'))

    def test_start_out_end_in_range_em_still_fails(self):
        self.assertTrue(_no_yr(f'1899{EM}2010'))


# ============================================================================
# Class 11 — TestNormalizationNoFalsePositives
# 20 tests: normalization must not introduce YEAR_RANGE where none exists
# ============================================================================
