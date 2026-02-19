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


class TestMixedDashTypesInText(unittest.TestCase):
    """Multiple different Unicode dash types in the same text."""

    def test_en_and_em_in_same_text(self):
        r = extract_explicit_dates(f'2000{EN}2010 and 2014{EM}2015') or {}
        self.assertIn('2000-2010', r)
        self.assertIn('2014-2015', r)

    def test_en_and_ascii_in_same_text(self):
        r = extract_explicit_dates(f'2000-2010 and 2014{EN}2015') or {}
        self.assertIn('2000-2010', r)
        self.assertIn('2014-2015', r)

    def test_em_and_ascii_in_same_text(self):
        r = extract_explicit_dates(f'2000-2010 and 2014{EM}2015') or {}
        self.assertIn('2000-2010', r)
        self.assertIn('2014-2015', r)

    def test_three_dash_types(self):
        r = extract_explicit_dates(f'1990-2000, 2000{EN}2010, 2014{EM}2015') or {}
        self.assertIn('1990-2000', r)
        self.assertIn('2000-2010', r)
        self.assertIn('2014-2015', r)

    def test_figure_and_en(self):
        r = extract_explicit_dates(f'2000{FIG}2010 and 2014{EN}2015') or {}
        self.assertIn('2000-2010', r)
        self.assertIn('2014-2015', r)

    def test_minus_and_em(self):
        r = extract_explicit_dates(f'2000{MIN}2010 and 2014{EM}2015') or {}
        self.assertIn('2000-2010', r)
        self.assertIn('2014-2015', r)

    def test_fullwidth_and_ascii(self):
        r = extract_explicit_dates(f'2000{FWH}2010 and 2014-2015') or {}
        self.assertIn('2000-2010', r)
        self.assertIn('2014-2015', r)

    def test_spaced_and_nonspaced_en(self):
        r = extract_explicit_dates(f'2000 {EN} 2010 and 2014{EN}2015') or {}
        self.assertIn('2000-2010', r)
        self.assertIn('2014-2015', r)

    def test_all_types_one_sentence(self):
        """Each variant in a list — all should be detected."""
        parts = [
            f'2000{EN}2001',
            f'2001{EM}2002',
            f'2002{HY}2003',
            f'2003{MIN}2004',
        ]
        text = ', '.join(parts)
        r = extract_explicit_dates(text) or {}
        yr_count = sum(1 for v in r.values() if v == 'YEAR_RANGE')
        self.assertGreaterEqual(yr_count, 4)

    def test_en_dash_in_text_non_year_hyphens_safe(self):
        """Compound words with hyphens + en dash year range — no interference."""
        text = f'mother-in-law attended the 2014{EN}2015 reunion.'
        self.assertTrue(_yr(text))

    def test_hyphenated_word_no_false_positive(self):
        """Compound word hyphens shouldn't produce YEAR_RANGE."""
        self.assertTrue(_no_yr('state-of-the-art technology'))

    def test_en_dash_between_words_no_false_positive(self):
        """En dash between plain words — no YEAR_RANGE."""
        self.assertTrue(_no_yr(f'north{EN}south corridor'))

    def test_em_dash_between_words_no_false_positive(self):
        self.assertTrue(_no_yr(f'the result{EM}as expected{EM}was clear'))

    def test_mixed_dash_all_invalid_years(self):
        """All dash types with out-of-range years — no YEAR_RANGE."""
        for dash in [EN, EM, HY, MIN, FWH]:
            with self.subTest(dash=repr(dash)):
                self.assertTrue(_no_yr(f'1800{dash}1900'))

    def test_mixed_dash_all_reversed(self):
        """All dash types with reversed years — no YEAR_RANGE."""
        for dash in [EN, EM, HY, MIN, FWH]:
            with self.subTest(dash=repr(dash)):
                self.assertTrue(_no_yr(f'2015{dash}2014'))

    def test_mixed_dash_all_same_year(self):
        """All dash types with same year — no YEAR_RANGE."""
        for dash in [EN, EM, HY, MIN, FWH]:
            with self.subTest(dash=repr(dash)):
                self.assertTrue(_no_yr(f'2014{dash}2014'))

    def test_list_of_ranges_different_dashes(self):
        text = f'- 2000{EN}2005\n- 2005{EM}2010\n- 2010-2015'
        self.assertTrue(_yr(text))

    def test_two_ranges_result_count(self):
        r = extract_explicit_dates(f'2000{EN}2010 then 2014{EM}2015') or {}
        yr_count = sum(1 for v in r.values() if v == 'YEAR_RANGE')
        self.assertGreaterEqual(yr_count, 2)

    def test_all_seven_unicode_variants_safe(self):
        """All exotic chars should not crash the extractor."""
        for dash in [EN, EM, HY, NBH, FIG, HB, MIN, SHY, FWH]:
            with self.subTest(dash=repr(dash)):
                self.assertTrue(_safe(f'2014{dash}2015'))

    def test_compact_and_spaced_mixed(self):
        r = extract_explicit_dates(f'2000{EN}2010 and 2014 - 2015') or {}
        self.assertIn('2000-2010', r)
        self.assertIn('2014-2015', r)


# ============================================================================
# Class 10 — TestNormalizationPreservesValidity
# 25 tests: normalization must not bypass year validation rules
# ============================================================================
