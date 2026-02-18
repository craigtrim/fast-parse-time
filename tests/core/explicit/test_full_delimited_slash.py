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

class TestFullDelimitedSlash(unittest.TestCase):
    """Full 3-component dates using slash delimiter."""

    def test_mdy_standard(self):
        """Standard US format MM/DD/YYYY."""
        self.assertTrue(try_parse_date('04/08/2024'))

    def test_dmy_european(self):
        """European format DD/MM/YYYY."""
        self.assertTrue(try_parse_date('08/04/2024'))

    def test_mdy_single_digit_month(self):
        """Single-digit month."""
        self.assertTrue(try_parse_date('4/08/2024'))

    def test_mdy_single_digit_day(self):
        """Single-digit day."""
        self.assertTrue(try_parse_date('04/8/2024'))

    def test_mdy_single_digit_both(self):
        """Single-digit month and day."""
        self.assertTrue(try_parse_date('4/8/2024'))

    def test_dmy_day_31(self):
        """Day 31 in a 31-day month."""
        self.assertTrue(try_parse_date('31/01/2024'))

    def test_mdy_december(self):
        """December (month 12)."""
        self.assertTrue(try_parse_date('12/25/2024'))

    def test_mdy_leap_day(self):
        """Feb 29 in a leap year."""
        self.assertTrue(try_parse_date('02/29/2024'))

    def test_ymd_slash(self):
        """Year-first with slash: YYYY/MM/DD."""
        self.assertTrue(try_parse_date('2024/04/08'))

    def test_ymd_slash_single_digit(self):
        """Year-first single-digit month and day."""
        self.assertTrue(try_parse_date('2024/4/8'))
