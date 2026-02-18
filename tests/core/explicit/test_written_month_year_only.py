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

class TestWrittenMonthYearOnly(unittest.TestCase):
    """Month + year only (no day component)."""

    def test_march_year(self):
        """March 2024."""
        self.assertTrue(try_parse_date('March 2024'))

    def test_mar_year(self):
        """Mar 2024."""
        self.assertTrue(try_parse_date('Mar 2024'))

    def test_january_year(self):
        """January 2024."""
        self.assertTrue(try_parse_date('January 2024'))

    def test_december_year(self):
        """December 2024."""
        self.assertTrue(try_parse_date('December 2024'))

    def test_feb_year(self):
        """Feb 2024."""
        self.assertTrue(try_parse_date('Feb 2024'))

    def test_sep_year(self):
        """Sep 2024."""
        self.assertTrue(try_parse_date('Sep 2024'))
