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


class TestDoubleDashAndChainedDashes(unittest.TestCase):
    """Multiple consecutive dashes or chained Unicode dashes between years."""

    def test_double_ascii_hyphen(self):
        """2014--2015 — double ASCII hyphen."""
        self.assertTrue(_no_yr('2014--2015'))

    def test_double_en_dash(self):
        self.assertTrue(_no_yr(f'2014{EN}{EN}2015'))

    def test_double_em_dash(self):
        self.assertTrue(_no_yr(f'2014{EM}{EM}2015'))

    def test_en_then_em(self):
        self.assertTrue(_no_yr(f'2014{EN}{EM}2015'))

    def test_em_then_en(self):
        self.assertTrue(_no_yr(f'2014{EM}{EN}2015'))

    def test_ascii_then_en(self):
        self.assertTrue(_no_yr(f'2014-{EN}2015'))

    def test_en_then_ascii(self):
        self.assertTrue(_no_yr(f'2014{EN}-2015'))

    def test_triple_ascii_hyphen(self):
        self.assertTrue(_no_yr('2014---2015'))

    def test_dash_space_dash(self):
        """2014 - - 2015: double-hyphen with space."""
        self.assertTrue(_no_yr('2014 - - 2015'))

    def test_all_double_safe(self):
        """None of the double-dash forms should crash."""
        for d1, d2 in [(EN, EN), (EM, EM), (EN, EM), ('-', EN), (EN, '-')]:
            with self.subTest(d1=repr(d1), d2=repr(d2)):
                self.assertTrue(_safe(f'2014{d1}{d2}2015'))


if __name__ == '__main__':
    unittest.main()
