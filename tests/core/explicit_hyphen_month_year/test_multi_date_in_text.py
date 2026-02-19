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


class TestMultiDateInText:
    """Multiple hyphen-month-year tokens in a single string."""

    def test_two_forward_dates(self):
        """Two forward-format dates in one sentence."""
        result = extract_explicit_dates('Review period Oct-23 through Dec-23')
        assert len(result) >= 2

    def test_two_reversed_dates(self):
        """Two reversed-format dates in one sentence."""
        result = extract_explicit_dates('Span from 2023-Jan to 2023-Mar')
        assert len(result) >= 2

    def test_mixed_forward_reversed(self):
        """One forward and one reversed in same sentence."""
        result = extract_explicit_dates('Filed Oct-2023 and archived under 2023-Nov')
        assert len(result) >= 2

    def test_abbrev_and_full_month(self):
        """Abbreviated and full-month format in same sentence."""
        result = extract_explicit_dates('Covers Oct-23 and November-2023')
        assert len(result) >= 2

    def test_three_dates_in_sentence(self):
        """Three date tokens in one sentence."""
        result = extract_explicit_dates('Quarters: Jan-23, Apr-23, Jul-23')
        assert len(result) >= 3


# ---------------------------------------------------------------------------
# 21. Various year values across decades (10 tests)
# ---------------------------------------------------------------------------
