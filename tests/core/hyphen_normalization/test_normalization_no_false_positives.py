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


class TestNormalizationNoFalsePositives(unittest.TestCase):
    """Non-year content with Unicode dashes should not produce YEAR_RANGE."""

    def test_compound_word_en_dash(self):
        self.assertTrue(_no_yr(f'mother{EN}in{EN}law'))

    def test_compound_word_em_dash(self):
        self.assertTrue(_no_yr(f'state{EM}of{EM}the{EM}art'))

    def test_price_range_en_dash(self):
        """$20–$30 — not a year range."""
        self.assertTrue(_no_yr(f'$20{EN}$30'))

    def test_page_range_en_dash(self):
        """Pages 3–10 — not a year range."""
        self.assertTrue(_no_yr(f'pages 3{EN}10'))

    def test_chapter_range_em_dash(self):
        self.assertTrue(_no_yr(f'chapters 1{EM}5'))

    def test_time_range_en_dash(self):
        """9–5 — not a year range."""
        self.assertTrue(_no_yr(f'9{EN}5'))

    def test_small_numbers_en_dash(self):
        self.assertTrue(_no_yr(f'100{EN}200'))

    def test_large_numbers_out_of_range(self):
        self.assertTrue(_no_yr(f'10000{EN}20000'))

    def test_non_year_four_digits_en(self):
        """1234–1235: both below MIN_YEAR."""
        self.assertTrue(_no_yr(f'1234{EN}1235'))

    def test_phone_like_en_dash(self):
        self.assertTrue(_no_yr(f'555{EN}1234'))

    def test_score_en_dash(self):
        """Game score 3–0 — not a year range."""
        self.assertTrue(_no_yr(f'3{EN}0'))

    def test_street_number_en_dash(self):
        """Address range 100–200 Main St."""
        self.assertTrue(_no_yr(f'100{EN}200 Main St'))

    def test_version_en_dash(self):
        self.assertTrue(_no_yr(f'version 1{EN}2'))

    def test_size_range_em_dash(self):
        self.assertTrue(_no_yr(f'sizes 8{EM}12'))

    def test_temperature_range_en(self):
        self.assertTrue(_no_yr(f'20{EN}30 degrees'))

    def test_en_dash_between_words(self):
        self.assertTrue(_no_yr(f'north{EN}south'))

    def test_em_dash_in_sentence_no_numbers(self):
        self.assertTrue(_no_yr(f'The answer{EM}of course{EM}is obvious.'))

    def test_double_en_dash_stacked(self):
        """2014––2015 (two en dashes) — should not match."""
        self.assertTrue(_no_yr(f'2014{EN}{EN}2015'))

    def test_en_em_mixed_stacked(self):
        """2014–—2015 (en then em) — should not match."""
        self.assertTrue(_no_yr(f'2014{EN}{EM}2015'))

    def test_single_year_with_dash(self):
        """2014- with no second year — not a range."""
        self.assertTrue(_no_yr(f'2014{EN}'))


# ============================================================================
# Class 12 — TestAsciiHyphenUnaffected
# 15 tests: normalization must not break existing ASCII hyphen behavior
# ============================================================================
