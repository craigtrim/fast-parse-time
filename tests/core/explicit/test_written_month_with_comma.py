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

class TestWrittenMonthWithComma(unittest.TestCase):
    """Written month dates with comma separator (English prose style)."""

    def test_march_comma(self):
        """March 15, 2024."""
        self.assertTrue(try_parse_date('March 15, 2024'))

    def test_abbreviated_mar_comma(self):
        """Mar 15, 2024."""
        self.assertTrue(try_parse_date('Mar 15, 2024'))

    def test_january_comma(self):
        """January 1, 2024."""
        self.assertTrue(try_parse_date('January 1, 2024'))

    def test_december_comma(self):
        """December 31, 2024."""
        self.assertTrue(try_parse_date('December 31, 2024'))

    def test_feb_comma_leap(self):
        """February 29, 2024 — leap year."""
        self.assertTrue(try_parse_date('February 29, 2024'))

    def test_june_comma(self):
        """June 15, 2024."""
        self.assertTrue(try_parse_date('June 15, 2024'))

    def test_sep_abbreviated_comma(self):
        """Sep 15, 2024 (standard 3-letter)."""
        self.assertTrue(try_parse_date('Sep 15, 2024'))

    def test_oct_abbreviated_comma(self):
        """Oct 1, 2024."""
        self.assertTrue(try_parse_date('Oct 1, 2024'))
