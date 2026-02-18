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

class TestFullDelimitedDot(unittest.TestCase):
    """Full 3-component dates using dot delimiter."""

    def test_dot_mdy(self):
        """Dot-separated MM.DD.YYYY."""
        self.assertTrue(try_parse_date('04.08.2024'))

    def test_dot_dmy(self):
        """Dot-separated DD.MM.YYYY."""
        self.assertTrue(try_parse_date('08.04.2024'))

    def test_dot_version_number_style(self):
        """Version-number-style date with 2-digit year: 20.04.01."""
        self.assertTrue(try_parse_date('20.04.01'))

    def test_dot_year_month_day_2digit(self):
        """2-digit year first: 24.04.08."""
        self.assertTrue(try_parse_date('24.04.08'))
