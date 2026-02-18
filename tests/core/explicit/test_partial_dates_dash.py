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

class TestPartialDatesDash(unittest.TestCase):
    """Two-component dates (no year) using dash delimiter."""

    def test_month_day_dashed(self):
        """MM-DD partial."""
        self.assertTrue(try_parse_date('3-15'))

    def test_day_month_dashed(self):
        """DD-MM partial."""
        self.assertTrue(try_parse_date('31-03'))

    def test_ambiguous_dashed(self):
        """Ambiguous partial with dash."""
        self.assertTrue(try_parse_date('4-8'))

    def test_feb_29_dash(self):
        """Feb 29 partial with dash."""
        self.assertTrue(try_parse_date('29-2'))
