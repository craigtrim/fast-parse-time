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

class TestYearMonthOnly(unittest.TestCase):
    """Two-component year+month dates (no day)."""

    def test_year_month_slash(self):
        """YYYY/MM format."""
        self.assertTrue(try_parse_date('2023/01'))

    def test_year_month_dash(self):
        """YYYY-MM format."""
        self.assertTrue(try_parse_date('2023-01'))

    def test_year_december_slash(self):
        """YYYY/12 format."""
        self.assertTrue(try_parse_date('2024/12'))

    def test_year_december_dash(self):
        """YYYY-12 format."""
        self.assertTrue(try_parse_date('2024-12'))
