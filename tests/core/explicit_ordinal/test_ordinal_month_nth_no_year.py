#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for 'Month NNth' and 'MonthAbbr NNth' (no year) patterns → DAY_MONTH.

These are unambiguous: the ordinal suffix makes it clear the number is a day.

Related GitHub Issue:
    #22 - Gap: ordinal day format not supported (12th day of December, 19th day of May)
    https://github.com/craigtrim/fast-parse-time/issues/22
"""

import pytest
from fast_parse_time import extract_explicit_dates


class TestOrdinalMonthNthNoYear:
    """'Month NNth' and 'MonthAbbr NNth' (no year) → DAY_MONTH."""

    # ── full month names ──────────────────────────────────────────────────────

    def test_december_12th(self):
        result = extract_explicit_dates('December 12th')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_may_19th(self):
        result = extract_explicit_dates('May 19th')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_january_1st(self):
        result = extract_explicit_dates('January 1st')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_february_2nd(self):
        result = extract_explicit_dates('February 2nd')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_march_3rd(self):
        result = extract_explicit_dates('March 3rd')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_april_4th(self):
        result = extract_explicit_dates('April 4th')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_june_15th(self):
        result = extract_explicit_dates('June 15th')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_july_21st(self):
        result = extract_explicit_dates('July 21st')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_august_22nd(self):
        result = extract_explicit_dates('August 22nd')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_september_23rd(self):
        result = extract_explicit_dates('September 23rd')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_october_31st(self):
        result = extract_explicit_dates('October 31st')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_november_11th(self):
        result = extract_explicit_dates('November 11th')
        assert result
        assert 'DAY_MONTH' in result.values()

    # ── abbreviated month names ───────────────────────────────────────────────

    def test_dec_12th(self):
        result = extract_explicit_dates('Dec 12th')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_sep_3rd(self):
        result = extract_explicit_dates('Sep 3rd')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_jan_1st(self):
        result = extract_explicit_dates('Jan 1st')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_feb_2nd(self):
        result = extract_explicit_dates('Feb 2nd')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_mar_3rd(self):
        result = extract_explicit_dates('Mar 3rd')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_apr_4th(self):
        result = extract_explicit_dates('Apr 4th')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_jun_15th(self):
        result = extract_explicit_dates('Jun 15th')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_jul_21st(self):
        result = extract_explicit_dates('Jul 21st')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_aug_22nd(self):
        result = extract_explicit_dates('Aug 22nd')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_oct_23rd(self):
        result = extract_explicit_dates('Oct 23rd')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_nov_30th(self):
        result = extract_explicit_dates('Nov 30th')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_sept_5th(self):
        result = extract_explicit_dates('Sept 5th')
        assert result
        assert 'DAY_MONTH' in result.values()

    # ── case insensitive ──────────────────────────────────────────────────────

    def test_december_12TH_uppercase(self):
        result = extract_explicit_dates('December 12TH')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_oct_23RD_uppercase(self):
        result = extract_explicit_dates('Oct 23RD')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_jan_1ST_uppercase(self):
        result = extract_explicit_dates('Jan 1ST')
        assert result
        assert 'DAY_MONTH' in result.values()

    # ── sentence context ──────────────────────────────────────────────────────

    def test_embedded_december_12th(self):
        result = extract_explicit_dates('The deadline is December 12th.')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_embedded_may_19th(self):
        result = extract_explicit_dates('Born on May 19th in Paris.')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_embedded_oct_23rd(self):
        result = extract_explicit_dates('Submit by Oct 23rd.')
        assert result
        assert 'DAY_MONTH' in result.values()
