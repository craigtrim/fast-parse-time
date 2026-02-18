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

class TestNonStandardAbbreviations(unittest.TestCase):
    """Non-standard month abbreviations that need alias normalisation."""

    def test_sept_with_comma(self):
        """'Sept 15, 2024' — 4-letter Sept variant."""
        self.assertTrue(try_parse_date('Sept 15, 2024'))

    def test_sept_no_comma(self):
        """'Sept 15 2024' without comma."""
        self.assertTrue(try_parse_date('Sept 15 2024'))

    def test_sept_year_only(self):
        """'Sept 2024' — month+year with Sept."""
        self.assertTrue(try_parse_date('Sept 2024'))

    def test_sept_lowercase(self):
        """'sept 15, 2024' — all lowercase."""
        self.assertTrue(try_parse_date('sept 15, 2024'))
