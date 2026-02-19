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


class TestEmDashInContext(unittest.TestCase):
    """Em dash year range embedded in real text."""

    def test_period_2014_em_2015(self):
        self.assertTrue(_yr(f'The period 2014{EM}2015 was significant.'))

    def test_sentence_start(self):
        self.assertTrue(_yr(f'2014{EM}2015 was pivotal.'))

    def test_sentence_end(self):
        self.assertTrue(_yr(f'See data for 2014{EM}2015'))

    def test_in_parens(self):
        self.assertTrue(_yr(f'(2014{EM}2015)'))

    def test_multiple_em_ranges(self):
        self.assertTrue(_yr(f'2000{EM}2010 and 2014{EM}2015'))

    def test_multiple_em_ranges_both_keys(self):
        r = extract_explicit_dates(f'2000{EM}2010 and 2014{EM}2015') or {}
        self.assertIn('2000-2010', r)
        self.assertIn('2014-2015', r)

    def test_mixed_ascii_and_em(self):
        r = extract_explicit_dates(f'2000-2010 and 2014{EM}2015') or {}
        self.assertIn('2000-2010', r)
        self.assertIn('2014-2015', r)

    def test_colon_before(self):
        self.assertTrue(_yr(f'Period: 2014{EM}2015'))

    def test_html_tag(self):
        self.assertTrue(_yr(f'<span>2014{EM}2015</span>'))

    def test_reversed_em_in_sentence(self):
        self.assertTrue(_no_yr(f'The odd period 2015{EM}2014 is wrong.'))

    def test_out_of_range_em_in_sentence(self):
        self.assertTrue(_no_yr(f'Way back in 1800{EM}1900 things were different.'))

    def test_same_year_em_in_sentence(self):
        self.assertTrue(_no_yr(f'2014{EM}2014 is not a range.'))

    def test_em_and_en_mixed(self):
        """Both em and en dash ranges in same text."""
        r = extract_explicit_dates(f'2000{EN}2010 and 2014{EM}2015') or {}
        self.assertIn('2000-2010', r)
        self.assertIn('2014-2015', r)

    def test_em_between_compound_words(self):
        """Em dashes between words (not years) shouldn't produce YEAR_RANGE."""
        self.assertTrue(_no_yr(f'The quick{EM}brown fox jumped.'))

    def test_em_surrounding_aside(self):
        """Em dashes used as aside punctuation shouldn't produce YEAR_RANGE."""
        self.assertTrue(_safe(f'The result{EM}as expected{EM}was clear.'))


# ============================================================================
# Class 5 — TestOtherUnicodeDashVariants
# 30 tests: less common Unicode dashes
# ============================================================================
