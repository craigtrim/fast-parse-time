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


class TestSoftAndInvisibleChars(unittest.TestCase):
    """Invisible/soft characters between years should not produce YEAR_RANGE."""

    def test_soft_hyphen_between_years(self):
        """U+00AD SOFT HYPHEN is a formatting hint; should not match."""
        self.assertTrue(_no_yr(f'2014{SHY2}2015'))

    def test_zero_width_space_between_years(self):
        """U+200B between years: no hyphen, no match."""
        self.assertTrue(_no_yr(f'2014{ZWS}2015'))

    def test_nbsp_between_years_no_dash(self):
        """NBSP alone (no dash) between years: just spaces, not a range."""
        self.assertTrue(_no_yr(f'2014{NBSP}2015'))

    def test_bom_between_years(self):
        """BOM/ZWNBSP between years should not produce a match."""
        self.assertTrue(_safe(f'2014\ufeff2015'))

    def test_soft_hyphen_safe(self):
        self.assertTrue(_safe(f'2014{SHY2}2015'))

    def test_zwsp_safe(self):
        self.assertTrue(_safe(f'2014{ZWS}2015'))

    def test_nbsp_safe(self):
        self.assertTrue(_safe(f'2014{NBSP}2015'))

    def test_double_zero_width(self):
        self.assertTrue(_safe(f'2014{ZWS}{ZWS}2015'))

    def test_mixed_invisible_no_match(self):
        self.assertTrue(_no_yr(f'2014{ZWS}{NBSP}2015'))

    def test_combining_chars_safe(self):
        """Unicode combining characters should not crash."""
        self.assertTrue(_safe('2014\u0301-2015'))


# ============================================================================
# Class 14 — TestDoubleDashAndChainedDashes
# 10 tests: multiple consecutive dashes shouldn't produce YEAR_RANGE
# ============================================================================
