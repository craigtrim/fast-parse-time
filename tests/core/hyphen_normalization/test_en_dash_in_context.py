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


class TestEnDashInContext(unittest.TestCase):
    """En dash year range embedded in real text."""

    def test_period_2014_en_2015(self):
        self.assertTrue(_yr(f'The period 2014{EN}2015 was significant.'))

    def test_sentence_start(self):
        self.assertTrue(_yr(f'2014{EN}2015 was pivotal.'))

    def test_sentence_end(self):
        self.assertTrue(_yr(f'See data for 2014{EN}2015'))

    def test_trailing_period(self):
        self.assertTrue(_yr(f'2014{EN}2015.'))

    def test_trailing_comma(self):
        self.assertTrue(_yr(f'2014{EN}2015,'))

    def test_in_parens(self):
        self.assertTrue(_yr(f'(2014{EN}2015)'))

    def test_in_brackets(self):
        self.assertTrue(_yr(f'[2014{EN}2015]'))

    def test_quoted(self):
        self.assertTrue(_yr(f'"2014{EN}2015"'))

    def test_multiple_en_ranges(self):
        self.assertTrue(_yr(f'2000{EN}2010 and 2014{EN}2015'))

    def test_multiple_ranges_both_keys(self):
        r = extract_explicit_dates(f'2000{EN}2010 and 2014{EN}2015') or {}
        self.assertIn('2000-2010', r)
        self.assertIn('2014-2015', r)

    def test_mixed_ascii_and_en(self):
        """One ASCII hyphen range, one en dash range in same text."""
        r = extract_explicit_dates(f'2000-2010 and 2014{EN}2015') or {}
        self.assertIn('2000-2010', r)
        self.assertIn('2014-2015', r)

    def test_en_range_with_prose_year(self):
        r = extract_explicit_dates(f'In 2024 the era 2014{EN}2015 was recalled.') or {}
        self.assertIn('YEAR_RANGE', r.values())
        self.assertIn('YEAR_ONLY', r.values())

    def test_colon_before(self):
        self.assertTrue(_yr(f'Period: 2014{EN}2015'))

    def test_markdown_bold(self):
        self.assertTrue(_yr(f'**2014{EN}2015**'))

    def test_html_tag(self):
        self.assertTrue(_yr(f'<b>2014{EN}2015</b>'))

    def test_from_to_with_en_key(self):
        """from X to Y is unrelated; unaffected by en-dash normalization."""
        self.assertTrue(_yr('from 2004 to 2008'))

    def test_reversed_en_not_range(self):
        self.assertTrue(_no_yr(f'2015{EN}2014'))

    def test_same_year_en_not_range(self):
        self.assertTrue(_no_yr(f'2014{EN}2014'))

    def test_out_of_range_en(self):
        self.assertTrue(_no_yr(f'1800{EN}1900'))

    def test_long_sentence(self):
        text = f'Many scholars refer to the era 2014{EN}2015 as a turning point in history.'
        self.assertTrue(_yr(text))


# ============================================================================
# Class 3 — TestEmDashBare
# 20 tests: bare YYYY—YYYY (em dash, U+2014)
# ============================================================================
