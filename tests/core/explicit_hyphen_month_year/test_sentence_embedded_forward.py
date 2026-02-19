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


class TestSentenceEmbeddedForward:
    """Hyphen-month-year tokens embedded in longer text."""

    def test_sentence_jan_abbrev(self):
        result = extract_explicit_dates('Report filed in Jan-2023 for review')
        assert len(result) >= 1

    def test_sentence_feb_abbrev(self):
        result = extract_explicit_dates('Data collected from Feb-23 onward')
        assert len(result) >= 1

    def test_sentence_mar_full(self):
        result = extract_explicit_dates('Records from March-2023 are available')
        assert len(result) >= 1

    def test_sentence_apr_full(self):
        result = extract_explicit_dates('Quarter ending April-23 results')
        assert len(result) >= 1

    def test_sentence_may_abbrev(self):
        result = extract_explicit_dates('Contract signed May-2023 expires next year')
        assert len(result) >= 1

    def test_sentence_jun_abbrev(self):
        result = extract_explicit_dates('The Jun-23 figures show a 12 percent increase')
        assert len(result) >= 1

    def test_sentence_jul_full(self):
        result = extract_explicit_dates('Fiscal year ended July-2023')
        assert len(result) >= 1

    def test_sentence_aug_abbrev(self):
        result = extract_explicit_dates('Market data for Aug-23 is attached')
        assert len(result) >= 1

    def test_sentence_sep_full(self):
        result = extract_explicit_dates('September-2023 was the peak month')
        assert len(result) >= 1

    def test_sentence_oct_abbrev(self):
        result = extract_explicit_dates('Review period covers Oct-23 through Dec-23')
        assert len(result) >= 1

    def test_sentence_nov_full(self):
        result = extract_explicit_dates('See November-2023 appendix for details')
        assert len(result) >= 1

    def test_sentence_dec_abbrev(self):
        result = extract_explicit_dates('Year-end closing Dec-2023 balances')
        assert len(result) >= 1


# ---------------------------------------------------------------------------
# 16. Sentence-embedded: reversed formats in prose (12 tests)
# ---------------------------------------------------------------------------
