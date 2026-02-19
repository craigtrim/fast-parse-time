#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
TDD tests for issue #21: abbreviated month-year format with hyphen delimiter.

Covers forward (MONTH_YEAR) and reversed (YEAR_MONTH) patterns for both
abbreviated and full month names, with 2-digit and 4-digit years.

Related GitHub Issue:
    #21 - Gap: abbreviated month-year format not supported (Oct-23, May-23)
    https://github.com/craigtrim/fast-parse-time/issues/21
"""

import pytest
from fast_parse_time import extract_explicit_dates


# ---------------------------------------------------------------------------
# 1. Abbreviated month + hyphen + 2-digit year → MONTH_YEAR (12 tests)
# ---------------------------------------------------------------------------


class TestExtractedTextKey:
    """The key returned in the result dict should match the original date token."""

    def test_key_oct_23(self):
        result = extract_explicit_dates('Oct-23')
        assert 'Oct-23' in result

    def test_key_jan_2023(self):
        result = extract_explicit_dates('Jan-2023')
        assert 'Jan-2023' in result

    def test_key_march_2023(self):
        result = extract_explicit_dates('March-2023')
        assert 'March-2023' in result

    def test_key_november_23(self):
        result = extract_explicit_dates('November-23')
        assert 'November-23' in result

    def test_key_2023_oct(self):
        result = extract_explicit_dates('2023-Oct')
        assert '2023-Oct' in result

    def test_key_23_jan(self):
        result = extract_explicit_dates('23-Jan')
        assert '23-Jan' in result

    def test_key_2023_march(self):
        result = extract_explicit_dates('2023-March')
        assert '2023-March' in result

    def test_key_23_december(self):
        result = extract_explicit_dates('23-December')
        assert '23-December' in result

    def test_key_sept_2023(self):
        result = extract_explicit_dates('Sept-2023')
        assert 'Sept-2023' in result

    def test_key_2023_sept(self):
        result = extract_explicit_dates('2023-Sept')
        assert '2023-Sept' in result

    def test_key_lower_oct_23(self):
        """Lowercase input — key should preserve original casing."""
        result = extract_explicit_dates('oct-23')
        assert 'oct-23' in result

    def test_key_upper_mar_2023(self):
        """Uppercase input — key should preserve original casing."""
        result = extract_explicit_dates('MAR-2023')
        assert 'MAR-2023' in result
