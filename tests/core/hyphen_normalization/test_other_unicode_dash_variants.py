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


class TestOtherUnicodeDashVariants(unittest.TestCase):
    """Exotic Unicode hyphen/dash chars should all normalize to ASCII hyphen."""

    # U+2010 HYPHEN
    def test_hyphen_proper_bare(self):
        self.assertTrue(_yr(f'2014{HY}2015'))

    def test_hyphen_proper_in_sentence(self):
        self.assertTrue(_yr(f'The period 2014{HY}2015.'))

    def test_hyphen_proper_reversed(self):
        self.assertTrue(_no_yr(f'2015{HY}2014'))

    def test_hyphen_proper_out_of_range(self):
        self.assertTrue(_no_yr(f'1800{HY}1900'))

    # U+2011 NON-BREAKING HYPHEN
    def test_nb_hyphen_bare(self):
        self.assertTrue(_yr(f'2014{NBH}2015'))

    def test_nb_hyphen_in_sentence(self):
        self.assertTrue(_yr(f'The era 2014{NBH}2015 passed.'))

    def test_nb_hyphen_reversed(self):
        self.assertTrue(_no_yr(f'2015{NBH}2014'))

    def test_nb_hyphen_out_of_range(self):
        self.assertTrue(_no_yr(f'1800{NBH}1900'))

    # U+2012 FIGURE DASH
    def test_figure_dash_bare(self):
        self.assertTrue(_yr(f'2014{FIG}2015'))

    def test_figure_dash_in_sentence(self):
        self.assertTrue(_yr(f'Period 2014{FIG}2015 matters.'))

    def test_figure_dash_reversed(self):
        self.assertTrue(_no_yr(f'2015{FIG}2014'))

    def test_figure_dash_out_of_range(self):
        self.assertTrue(_no_yr(f'1800{FIG}1900'))

    # U+2015 HORIZONTAL BAR
    def test_horizontal_bar_bare(self):
        self.assertTrue(_yr(f'2014{HB}2015'))

    def test_horizontal_bar_in_sentence(self):
        self.assertTrue(_yr(f'Range 2014{HB}2015.'))

    def test_horizontal_bar_reversed(self):
        self.assertTrue(_no_yr(f'2015{HB}2014'))

    # U+2212 MINUS SIGN
    def test_minus_sign_bare(self):
        self.assertTrue(_yr(f'2014{MIN}2015'))

    def test_minus_sign_in_sentence(self):
        self.assertTrue(_yr(f'Years 2014{MIN}2015.'))

    def test_minus_sign_reversed(self):
        self.assertTrue(_no_yr(f'2015{MIN}2014'))

    def test_minus_sign_out_of_range(self):
        self.assertTrue(_no_yr(f'1800{MIN}1900'))

    # U+FE63 SMALL HYPHEN-MINUS
    def test_small_hyphen_bare(self):
        self.assertTrue(_yr(f'2014{SHY}2015'))

    def test_small_hyphen_in_sentence(self):
        self.assertTrue(_yr(f'Span 2014{SHY}2015.'))

    def test_small_hyphen_reversed(self):
        self.assertTrue(_no_yr(f'2015{SHY}2014'))

    # U+FF0D FULLWIDTH HYPHEN-MINUS
    def test_fullwidth_hyphen_bare(self):
        self.assertTrue(_yr(f'2014{FWH}2015'))

    def test_fullwidth_hyphen_in_sentence(self):
        self.assertTrue(_yr(f'Period 2014{FWH}2015 reviewed.'))

    def test_fullwidth_hyphen_reversed(self):
        self.assertTrue(_no_yr(f'2015{FWH}2014'))

    def test_fullwidth_hyphen_out_of_range(self):
        self.assertTrue(_no_yr(f'1800{FWH}1900'))

    def test_all_variants_produce_ascii_key(self):
        """Every dash variant should produce '2014-2015' as the dict key."""
        for dash in [EN, EM, HY, NBH, FIG, HB, MIN, SHY, FWH]:
            with self.subTest(dash=repr(dash)):
                r = extract_explicit_dates(f'2014{dash}2015') or {}
                self.assertIn('2014-2015', r, msg=f'dash={repr(dash)} did not produce key 2014-2015')

    def test_all_variants_produce_year_range_value(self):
        """Every dash variant should produce 'YEAR_RANGE' as value."""
        for dash in [EN, EM, HY, NBH, FIG, HB, MIN, SHY, FWH]:
            with self.subTest(dash=repr(dash)):
                r = extract_explicit_dates(f'2014{dash}2015') or {}
                self.assertEqual(r.get('2014-2015'), 'YEAR_RANGE',
                                 msg=f'dash={repr(dash)} did not produce YEAR_RANGE')

    def test_all_variants_safe(self):
        """None of the exotic dash chars should cause an exception."""
        for dash in [EN, EM, HY, NBH, FIG, HB, MIN, SHY, FWH]:
            with self.subTest(dash=repr(dash)):
                self.assertTrue(_safe(f'2014{dash}2015'))


# ============================================================================
# Class 6 — TestEnDashWithSurroundingSpaces
# 20 tests: en or em dash WITH spaces — e.g. "2014 – 2015"
# ============================================================================
