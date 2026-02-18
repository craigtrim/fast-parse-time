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

class TestWrittenMonthNoComma(unittest.TestCase):
    """Written month dates without comma."""

    def test_march_no_comma(self):
        """March 15 2024."""
        self.assertTrue(try_parse_date('March 15 2024'))

    def test_mar_no_comma(self):
        """Mar 15 2024."""
        self.assertTrue(try_parse_date('Mar 15 2024'))

    def test_day_month_year_european(self):
        """15 March 2024 (European order)."""
        self.assertTrue(try_parse_date('15 March 2024'))

    def test_day_abbreviated_month_year(self):
        """15 Mar 2024 (European abbreviated)."""
        self.assertTrue(try_parse_date('15 Mar 2024'))

    def test_january_no_comma(self):
        """January 1 2024."""
        self.assertTrue(try_parse_date('January 1 2024'))

    def test_december_no_comma(self):
        """December 31 2024."""
        self.assertTrue(try_parse_date('December 31 2024'))

    def test_all_months_jan(self):
        self.assertTrue(try_parse_date('January 15 2024'))

    def test_all_months_feb(self):
        self.assertTrue(try_parse_date('February 15 2024'))

    def test_all_months_apr(self):
        self.assertTrue(try_parse_date('April 15 2024'))

    def test_all_months_may(self):
        self.assertTrue(try_parse_date('May 15 2024'))

    def test_all_months_jun(self):
        self.assertTrue(try_parse_date('June 15 2024'))

    def test_all_months_jul(self):
        self.assertTrue(try_parse_date('July 15 2024'))

    def test_all_months_aug(self):
        self.assertTrue(try_parse_date('August 15 2024'))

    def test_all_months_sep(self):
        self.assertTrue(try_parse_date('September 15 2024'))

    def test_all_months_oct(self):
        self.assertTrue(try_parse_date('October 15 2024'))

    def test_all_months_nov(self):
        self.assertTrue(try_parse_date('November 15 2024'))

    def test_all_months_dec(self):
        self.assertTrue(try_parse_date('December 15 2024'))
