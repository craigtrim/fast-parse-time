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

class TestFullDelimitedDash(unittest.TestCase):
    """Full 3-component dates using dash delimiter."""

    def test_iso_standard(self):
        """ISO 8601: YYYY-MM-DD."""
        self.assertTrue(try_parse_date('2024-04-08'))

    def test_iso_december(self):
        """ISO 8601 December."""
        self.assertTrue(try_parse_date('2024-12-31'))

    def test_mdy_dashed(self):
        """Dashed MM-DD-YYYY."""
        self.assertTrue(try_parse_date('04-08-2024'))

    def test_dmy_dashed(self):
        """Dashed DD-MM-YYYY."""
        self.assertTrue(try_parse_date('08-04-2024'))

    def test_iso_leap_day(self):
        """ISO leap day."""
        self.assertTrue(try_parse_date('2024-02-29'))

    def test_iso_jan_first(self):
        """ISO January 1st."""
        self.assertTrue(try_parse_date('2024-01-01'))
