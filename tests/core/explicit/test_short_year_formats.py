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

class TestShortYearFormats(unittest.TestCase):
    """Dates with 2-digit years (version-number style, etc.)."""

    def test_dot_dmy_short_year(self):
        """DD.MM.YY format."""
        self.assertTrue(try_parse_date('20.04.01'))

    def test_slash_mdy_short_year(self):
        """MM/DD/YY format."""
        self.assertTrue(try_parse_date('04/08/24'))

    def test_slash_dmy_short_year(self):
        """DD/MM/YY format."""
        self.assertTrue(try_parse_date('08/04/24'))
