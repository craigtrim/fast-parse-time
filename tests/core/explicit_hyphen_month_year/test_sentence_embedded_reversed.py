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


class TestSentenceEmbeddedReversed:
    """Reversed hyphen-year-month tokens embedded in longer text."""

    def test_sentence_2023_jan(self):
        result = extract_explicit_dates('Filed under 2023-Jan records')
        assert len(result) >= 1

    def test_sentence_2023_feb(self):
        result = extract_explicit_dates('Audit from 2023-February completed')
        assert len(result) >= 1

    def test_sentence_23_mar(self):
        result = extract_explicit_dates('Reference period 23-Mar to 23-Jun')
        assert len(result) >= 1

    def test_sentence_2023_apr(self):
        result = extract_explicit_dates('Q2 starts 2023-Apr per schedule')
        assert len(result) >= 1

    def test_sentence_23_may(self):
        result = extract_explicit_dates('Budget approved for 23-May rollout')
        assert len(result) >= 1

    def test_sentence_2023_jun(self):
        result = extract_explicit_dates('Deliverables due 2023-Jun latest')
        assert len(result) >= 1

    def test_sentence_23_jul(self):
        result = extract_explicit_dates('The 23-July deadline is firm')
        assert len(result) >= 1

    def test_sentence_2023_aug(self):
        result = extract_explicit_dates('System goes live 2023-Aug')
        assert len(result) >= 1

    def test_sentence_23_sep(self):
        result = extract_explicit_dates('Pilot concluded 23-Sep successfully')
        assert len(result) >= 1

    def test_sentence_2023_oct(self):
        result = extract_explicit_dates('Started from 2023-Oct through present')
        assert len(result) >= 1

    def test_sentence_23_nov(self):
        result = extract_explicit_dates('Patch released 23-November hotfix')
        assert len(result) >= 1

    def test_sentence_2023_dec(self):
        result = extract_explicit_dates('Closed books 2023-December as scheduled')
        assert len(result) >= 1


# ---------------------------------------------------------------------------
# 17. Sept alternative abbreviation (6 tests)
# ---------------------------------------------------------------------------
