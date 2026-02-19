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


class TestExtremeWhitespace(unittest.TestCase):
    """Pathological whitespace around hyphens and dashes."""

    def test_many_spaces(self):
        self.assertTrue(_yr('2014     -     2015'))

    def test_many_tabs(self):
        self.assertTrue(_yr('2014\t\t\t-\t\t\t2015'))

    def test_mixed_space_tab(self):
        self.assertTrue(_yr('2014 \t - \t 2015'))

    def test_newline_around_hyphen(self):
        self.assertTrue(_yr('2014\n-\n2015'))

    def test_carriage_return_around_hyphen(self):
        self.assertTrue(_yr('2014\r-\r2015'))

    def test_nbsp_around_ascii_hyphen(self):
        """Non-breaking spaces around ASCII hyphen."""
        self.assertTrue(_yr(f'2014{NBSP}-{NBSP}2015'))

    def test_nbsp_around_en_dash(self):
        self.assertTrue(_yr(f'2014{NBSP}{EN}{NBSP}2015'))

    def test_nbsp_around_em_dash(self):
        self.assertTrue(_yr(f'2014{NBSP}{EM}{NBSP}2015'))

    def test_many_spaces_reversed_not_range(self):
        """Extreme spaces don't rescue a reversed range."""
        self.assertTrue(_no_yr('2015     -     2014'))

    def test_many_spaces_out_of_range(self):
        self.assertTrue(_no_yr('1800     -     1900'))

    def test_many_spaces_same_year(self):
        self.assertTrue(_no_yr('2014     -     2014'))

    def test_form_feed_around_hyphen(self):
        self.assertTrue(_safe('2014\f-\f2015'))

    def test_vertical_tab_around_hyphen(self):
        self.assertTrue(_safe('2014\v-\v2015'))

    def test_newline_and_nbsp(self):
        self.assertTrue(_safe(f'2014\n{NBSP}-{NBSP}\n2015'))

    def test_zwsp_around_hyphen(self):
        """Zero-width space around ASCII hyphen: after normalization may or may not match."""
        self.assertTrue(_safe(f'2014{ZWS}-{ZWS}2015'))


# ============================================================================
# Class 9 — TestMixedDashTypesInText
# 20 tests: texts containing multiple different dash types simultaneously
# ============================================================================
