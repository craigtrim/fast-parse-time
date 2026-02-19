#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""TDD tests for year-range expression extraction.

620 test cases covering:
  - True positives: YYYY-YYYY bare, from/to, between/and forms
  - False positives: same year, reversed, out-of-range, non-year numbers
  - Edge cases: boundary years, punctuation, adjacency, multiple ranges
  - Crazy inputs: None, malformed, Unicode, HTML
  - Currently-unsupported forms (en dash, spaces, abbreviated year, etc.)

Related GitHub Issue:
    #40 - feat: Parse year-range expressions (e.g., 2014-2015)
    https://github.com/craigtrim/fast-parse-time/issues/40
"""

import unittest
import pytest

from fast_parse_time import extract_explicit_dates


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _year_range(text) -> bool:
    """Return True if at least one YEAR_RANGE entry exists in the result."""
    try:
        result = extract_explicit_dates(text)
        return result is not None and 'YEAR_RANGE' in result.values()
    except Exception:
        return False


def _no_year_range(text) -> bool:
    """Return True if no YEAR_RANGE entry exists (valid false-positive check)."""
    try:
        result = extract_explicit_dates(text)
        return result is None or 'YEAR_RANGE' not in result.values()
    except Exception:
        return True


def _range_key(text: str, key: str) -> bool:
    """Return True if the specific key maps to YEAR_RANGE."""
    try:
        result = extract_explicit_dates(text)
        return result is not None and result.get(key) == 'YEAR_RANGE'
    except Exception:
        return False


def _is_dict_or_none(text) -> bool:
    """Result must be a dict or None — never raise."""
    try:
        result = extract_explicit_dates(text)
        return result is None or isinstance(result, dict)
    except Exception:
        return False


# ============================================================================
# Class 1 — TestHyphenBareValidPairs
# 40 tests: valid YYYY-YYYY pairs, bare (no surrounding text)
# ============================================================================


class TestCrazyInputs(unittest.TestCase):
    """Unusual, unexpected, or pathological inputs."""

    def test_emoji_only(self):
        self.assertTrue(_is_dict_or_none('🎉🎂🎊'))

    def test_emoji_with_years(self):
        self.assertTrue(_is_dict_or_none('🎉 2014-2015 🎂'))

    def test_html_entity(self):
        self.assertTrue(_is_dict_or_none('2014&ndash;2015'))

    def test_html_tag(self):
        self.assertTrue(_is_dict_or_none('<b>2014-2015</b>'))

    def test_html_year_range(self):
        """HTML-wrapped year range should still be detected."""
        self.assertTrue(_year_range('<b>2014-2015</b>'))

    def test_unicode_quotes(self):
        self.assertTrue(_is_dict_or_none('\u20182014-2015\u2019'))

    def test_very_long_string(self):
        text = 'lorem ipsum ' * 1000 + '2014-2015' + ' dolor sit amet' * 1000
        self.assertTrue(_year_range(text))

    def test_null_bytes(self):
        self.assertTrue(_is_dict_or_none('2014\x002015'))

    def test_escaped_chars(self):
        self.assertTrue(_is_dict_or_none('2014\\n2015'))

    def test_carriage_return(self):
        self.assertTrue(_is_dict_or_none('2014\r2015'))

    def test_sql_injection_like(self):
        self.assertTrue(_is_dict_or_none("'; DROP TABLE years; --"))

    def test_json_like(self):
        self.assertTrue(_is_dict_or_none('{"year": "2014-2015"}'))

    def test_json_range_detected(self):
        self.assertTrue(_year_range('{"year": "2014-2015"}'))

    def test_xml_like(self):
        self.assertTrue(_is_dict_or_none('<year>2014-2015</year>'))

    def test_markdown_like(self):
        self.assertTrue(_year_range('**The period 2014-2015** was notable.'))

    def test_repeated_range(self):
        text = '2014-2015 ' * 100
        self.assertTrue(_year_range(text))

    def test_alternating_valid_invalid(self):
        text = '2014-2015 abc 1800-1900 xyz 2000-2010'
        result = extract_explicit_dates(text) or {}
        self.assertIn('2014-2015', result)
        self.assertIn('2000-2010', result)
        self.assertNotIn('1800-1900', result)

    def test_url_like(self):
        self.assertTrue(_is_dict_or_none('https://example.com/report/2014-2015'))

    def test_path_like(self):
        self.assertTrue(_is_dict_or_none('/usr/local/data/2014-2015/report.csv'))

    def test_decade_as_range(self):
        """The 2010s could loosely suggest a range but isn't YYYY-YYYY."""
        self.assertTrue(_is_dict_or_none('the 2010s'))


# ============================================================================
# Class 35 — TestEnDashForm (EDGE CASE — may fail; xfail TBD)
# 10 tests: "YYYY–YYYY" using en dash (U+2013)
# ============================================================================
