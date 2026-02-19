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


class TestEnDashBare(unittest.TestCase):
    """En dash between years — should produce YEAR_RANGE after normalization."""

    def test_2014_en_2015(self):
        self.assertTrue(_yr(f'2014{EN}2015'))

    def test_2000_en_2010(self):
        self.assertTrue(_yr(f'2000{EN}2010'))

    def test_1990_en_2000(self):
        self.assertTrue(_yr(f'1990{EN}2000'))

    def test_1939_en_1945(self):
        self.assertTrue(_yr(f'1939{EN}1945'))

    def test_2019_en_2020(self):
        self.assertTrue(_yr(f'2019{EN}2020'))

    def test_1926_en_1927(self):
        self.assertTrue(_yr(f'1926{EN}1927'))

    def test_2035_en_2036(self):
        self.assertTrue(_yr(f'2035{EN}2036'))

    def test_1960_en_1970(self):
        self.assertTrue(_yr(f'1960{EN}1970'))

    def test_1970_en_1980(self):
        self.assertTrue(_yr(f'1970{EN}1980'))

    def test_1980_en_1990(self):
        self.assertTrue(_yr(f'1980{EN}1990'))

    def test_2010_en_2020(self):
        self.assertTrue(_yr(f'2010{EN}2020'))

    def test_2020_en_2025(self):
        self.assertTrue(_yr(f'2020{EN}2025'))

    def test_key_format(self):
        """Result key should be ASCII YYYY-YYYY regardless of input dash."""
        self.assertTrue(_key(f'2014{EN}2015', '2014-2015'))

    def test_value_format(self):
        r = extract_explicit_dates(f'2014{EN}2015') or {}
        self.assertEqual(r.get('2014-2015'), 'YEAR_RANGE')

    def test_result_is_dict(self):
        r = extract_explicit_dates(f'2014{EN}2015')
        self.assertIsInstance(r, dict)

    def test_result_nonempty(self):
        r = extract_explicit_dates(f'2014{EN}2015') or {}
        self.assertGreater(len(r), 0)

    def test_2004_en_2008(self):
        self.assertTrue(_yr(f'2004{EN}2008'))

    def test_1945_en_1955(self):
        self.assertTrue(_yr(f'1945{EN}1955'))

    def test_consecutive(self):
        self.assertTrue(_yr(f'2022{EN}2023'))

    def test_span_50(self):
        self.assertTrue(_yr(f'1970{EN}2020'))


# ============================================================================
# Class 2 — TestEnDashInContext
# 20 tests: en dash year range inside sentences and with punctuation
# ============================================================================
