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

class TestWhitespaceHandling(unittest.TestCase):
    """Whitespace edge cases."""

    def test_leading_spaces(self):
        """Leading whitespace is stripped."""
        self.assertTrue(try_parse_date('   04/08/2024'))

    def test_trailing_spaces(self):
        """Trailing whitespace is stripped."""
        self.assertTrue(try_parse_date('04/08/2024   '))

    def test_both_sides(self):
        """Whitespace on both sides."""
        self.assertTrue(try_parse_date('  04/08/2024  '))

    def test_written_month_with_whitespace(self):
        """Written month with surrounding whitespace."""
        self.assertTrue(try_parse_date('  March 15, 2024  '))

    def test_whitespace_only(self):
        """Whitespace-only string returns False."""
        self.assertFalse(try_parse_date('   '))
