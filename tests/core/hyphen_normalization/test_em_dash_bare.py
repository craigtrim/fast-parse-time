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


class TestEmDashBare(unittest.TestCase):
    """Em dash between years — should produce YEAR_RANGE after normalization."""

    def test_2014_em_2015(self):
        self.assertTrue(_yr(f'2014{EM}2015'))

    def test_2000_em_2010(self):
        self.assertTrue(_yr(f'2000{EM}2010'))

    def test_1990_em_2000(self):
        self.assertTrue(_yr(f'1990{EM}2000'))

    def test_1939_em_1945(self):
        self.assertTrue(_yr(f'1939{EM}1945'))

    def test_2019_em_2020(self):
        self.assertTrue(_yr(f'2019{EM}2020'))

    def test_1926_em_1927(self):
        self.assertTrue(_yr(f'1926{EM}1927'))

    def test_2035_em_2036(self):
        self.assertTrue(_yr(f'2035{EM}2036'))

    def test_1960_em_1970(self):
        self.assertTrue(_yr(f'1960{EM}1970'))

    def test_key_format(self):
        """Result key should be ASCII YYYY-YYYY."""
        self.assertTrue(_key(f'2014{EM}2015', '2014-2015'))

    def test_value_format(self):
        r = extract_explicit_dates(f'2014{EM}2015') or {}
        self.assertEqual(r.get('2014-2015'), 'YEAR_RANGE')

    def test_result_is_dict(self):
        r = extract_explicit_dates(f'2014{EM}2015')
        self.assertIsInstance(r, dict)

    def test_result_nonempty(self):
        r = extract_explicit_dates(f'2014{EM}2015') or {}
        self.assertGreater(len(r), 0)

    def test_2004_em_2008(self):
        self.assertTrue(_yr(f'2004{EM}2008'))

    def test_span_50(self):
        self.assertTrue(_yr(f'1970{EM}2020'))

    def test_consecutive(self):
        self.assertTrue(_yr(f'2022{EM}2023'))

    def test_reversed_em_not_range(self):
        self.assertTrue(_no_yr(f'2015{EM}2014'))

    def test_same_year_em_not_range(self):
        self.assertTrue(_no_yr(f'2014{EM}2014'))

    def test_out_of_range_em(self):
        self.assertTrue(_no_yr(f'1800{EM}1900'))

    def test_em_key_not_native_dash(self):
        """Key in result must use ASCII hyphen, not em dash."""
        r = extract_explicit_dates(f'2014{EM}2015') or {}
        self.assertNotIn(f'2014{EM}2015', r)

    def test_en_key_not_native_dash(self):
        """Key in result must use ASCII hyphen, not en dash."""
        r = extract_explicit_dates(f'2014{EN}2015') or {}
        self.assertNotIn(f'2014{EN}2015', r)


# ============================================================================
# Class 4 — TestEmDashInContext
# 15 tests: em dash year range inside sentences
# ============================================================================
