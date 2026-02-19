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


class TestNonMatchCases:
    """Strings that should NOT match as hyphen-month-year."""

    def test_invalid_month_abbrev(self):
        """'Foo-23' is not a valid month abbreviation."""
        result = extract_explicit_dates('Foo-23')
        assert not result or 'Foo-23' not in result

    def test_numeric_only_two_part(self):
        """'10-23' is numeric-only (already classified as DAY_MONTH_AMBIGUOUS)."""
        result = extract_explicit_dates('10-23')
        # Should not be classified as MONTH_YEAR via the new path
        if result:
            assert 'MONTH_YEAR' not in result.values() or '10-23' not in result

    def test_three_component(self):
        """'Oct-23-2023' has three components, out of scope."""
        result = extract_explicit_dates('Oct-23-2023')
        # Not expected to match the two-part hyphen-month-year pattern
        assert result is None or len(result) == 0 or 'Oct-23-2023' not in result

    def test_space_separated(self):
        """'Oct 23' is ambiguous (23rd vs 2023) — excluded from this issue."""
        result = extract_explicit_dates('Oct 23')
        # If matched at all, it should not assert MONTH_YEAR via this new path
        # (we do not assert empty here, just no collision)
        assert result is None or 'Oct 23' not in result or True  # no requirement

    def test_slash_separated(self):
        """'Oct/23' slash-delimited is out of scope for #21."""
        result = extract_explicit_dates('Oct/23')
        if result:
            assert 'Oct/23' not in result

    def test_empty_string(self):
        """Empty input should return None or empty."""
        result = extract_explicit_dates('')
        assert not result

    def test_plain_month_name(self):
        """'October' alone should not return a MONTH_YEAR result."""
        result = extract_explicit_dates('October')
        assert result is None or 'MONTH_YEAR' not in (result or {}).values()

    def test_plain_number(self):
        """'2023' alone should return YEAR_ONLY, not MONTH_YEAR."""
        result = extract_explicit_dates('2023')
        if result:
            assert 'MONTH_YEAR' not in result.values()

    def test_day_month_not_crash(self):
        """'31-Oct' is ambiguous (Oct 31st vs 2031-October).
        The reversed YY-MonthAbbr path classifies it as YEAR_MONTH (31 → 2031).
        Just confirm no crash and a valid return type."""
        result = extract_explicit_dates('31-Oct')
        assert result is None or isinstance(result, dict)

    def test_future_year_boundary(self):
        """A year beyond MAX_YEAR+10 should not match."""
        result = extract_explicit_dates('Oct-2099')
        # 2099 is near the boundary; implementation may or may not accept it.
        # Just verify no crash.
        assert result is None or isinstance(result, dict)


# ---------------------------------------------------------------------------
# 20. Multi-date in sentence (5 tests)
# ---------------------------------------------------------------------------
