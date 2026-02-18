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

class TestBoundaryDates(unittest.TestCase):
    """Boundary values: first/last days, end of months, etc."""

    def test_jan_1(self):
        """January 1st."""
        self.assertTrue(try_parse_date('01/01/2024'))

    def test_dec_31(self):
        """December 31st."""
        self.assertTrue(try_parse_date('12/31/2024'))

    def test_leap_day_2000(self):
        """Leap day in year 2000 (divisible by 400)."""
        self.assertTrue(try_parse_date('02/29/2000'))

    def test_non_leap_year_1900(self):
        """1900 is NOT a leap year (divisible by 100 but not 400)."""
        self.assertFalse(try_parse_date('02/29/1900'))

    def test_century_year_2100(self):
        """2100 is NOT a leap year."""
        self.assertFalse(try_parse_date('02/29/2100'))

    def test_apr_30(self):
        """April 30 — valid last day of April."""
        self.assertTrue(try_parse_date('04/30/2024'))

    def test_apr_31_invalid(self):
        """April 31 — April has only 30 days."""
        self.assertFalse(try_parse_date('2024-04-31'))

    def test_nov_30(self):
        """November 30 — valid."""
        self.assertTrue(try_parse_date('11/30/2024'))

    def test_jun_31_invalid(self):
        """June 31 — June has only 30 days."""
        self.assertFalse(try_parse_date('2024-06-31'))


if __name__ == '__main__':
    unittest.main()
