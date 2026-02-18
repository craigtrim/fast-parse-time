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

class TestPartialDatesSlash(unittest.TestCase):
    """Two-component dates (no year) using slash delimiter."""

    def test_month_day_unambiguous(self):
        """Month/Day where month <= 12 and day > 12: clearly MONTH_DAY."""
        self.assertTrue(try_parse_date('3/15'))

    def test_day_month_unambiguous(self):
        """Day/Month where day > 12: clearly DAY_MONTH."""
        self.assertTrue(try_parse_date('31/03'))

    def test_ambiguous_both_small(self):
        """Both components <= 12: ambiguous but structurally valid."""
        self.assertTrue(try_parse_date('4/8'))

    def test_feb_29_partial(self):
        """Feb 29 as partial date (handled via leap year probe)."""
        self.assertTrue(try_parse_date('29/2'))

    def test_feb_29_partial_mdy(self):
        """Feb 29 month-first as partial date."""
        self.assertTrue(try_parse_date('2/29'))

    def test_calendar_impossible_day(self):
        """Feb 30 doesn't exist but structurally looks like DD/MM."""
        self.assertTrue(try_parse_date('30/2'))

    def test_party_date(self):
        """Typical partial date in context: 7/24."""
        self.assertTrue(try_parse_date('7/24'))

    def test_day_31_month_1(self):
        """Jan 31 partial."""
        self.assertTrue(try_parse_date('31/1'))

    def test_single_digit_both(self):
        """Both components single digit."""
        self.assertTrue(try_parse_date('1/1'))

    def test_month_12_day_1(self):
        """December 1st partial."""
        self.assertTrue(try_parse_date('12/1'))
