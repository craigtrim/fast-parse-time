#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Tests for the stdlib-based date validator that replaces dateparser.

Related GitHub Issue:
    #29 - Remove dateparser dependency: replace with stdlib datetime
    https://github.com/craigtrim/fast-parse-time/issues/29
"""

import unittest
from fast_parse_time.explicit.dmo.stdlib_date_validator import try_parse_date

class TestInvalidInputs(unittest.TestCase):
    """Inputs that must return False."""

    def test_none(self):
        """None returns False without raising."""
        self.assertFalse(try_parse_date(None))

    def test_empty_string(self):
        """Empty string returns False."""
        self.assertFalse(try_parse_date(''))

    def test_plain_text(self):
        """Non-date text returns False."""
        self.assertFalse(try_parse_date('hello world'))

    def test_single_word(self):
        """Single non-date word returns False."""
        self.assertFalse(try_parse_date('meeting'))

    def test_number_only(self):
        """A standalone number (not a year-month) returns False."""
        self.assertFalse(try_parse_date('42'))

    def test_iso_invalid_month_zero(self):
        """Month 00 in ISO position is invalid."""
        self.assertFalse(try_parse_date('2024-00-01'))

    def test_iso_invalid_month_13(self):
        """Month 13 in ISO position is invalid."""
        self.assertFalse(try_parse_date('2024-13-01'))

    def test_slash_invalid_month_zero(self):
        """Month 00 in slash format is invalid."""
        self.assertFalse(try_parse_date('00/08/2024'))

    def test_slash_invalid_day_zero(self):
        """Day 00 in slash format is invalid."""
        self.assertFalse(try_parse_date('04/00/2024'))

    def test_all_nines(self):
        """99/99/9999 is not a date."""
        self.assertFalse(try_parse_date('99/99/9999'))

    def test_iso_feb_29_nonleap(self):
        """Feb 29 in a non-leap year (2023) is invalid."""
        self.assertFalse(try_parse_date('2023-02-29'))

    def test_iso_feb_30(self):
        """Feb 30 in ISO format is always invalid."""
        self.assertFalse(try_parse_date('2024-02-30'))

    def test_iso_jan_32(self):
        """Day 32 in ISO format is always invalid."""
        self.assertFalse(try_parse_date('2024-01-32'))

    def test_too_many_components(self):
        """Four slash-separated components are not a date."""
        self.assertFalse(try_parse_date('04/08/2024/extra'))

    def test_partial_both_components_zero(self):
        """0/0 both zero — outside plausible range (1-31)."""
        self.assertFalse(try_parse_date('0/0'))

    def test_partial_first_component_zero(self):
        """0/8 first zero — outside plausible range."""
        self.assertFalse(try_parse_date('0/8'))

    def test_partial_second_component_zero(self):
        """4/0 second zero — outside plausible range."""
        self.assertFalse(try_parse_date('4/0'))

    def test_partial_both_over_31(self):
        """32/40 — both over 31, not plausible date components."""
        self.assertFalse(try_parse_date('32/40'))

    def test_text_with_numbers_not_date(self):
        """Text containing numbers but not a date."""
        self.assertFalse(try_parse_date('version 3 released'))

    def test_decimal_number(self):
        """Pi to 3 decimal places — second component exceeds 31, not a date."""
        self.assertFalse(try_parse_date('3.141'))

    def test_url_like(self):
        """URL-like string is not a date."""
        self.assertFalse(try_parse_date('http://example.com'))
