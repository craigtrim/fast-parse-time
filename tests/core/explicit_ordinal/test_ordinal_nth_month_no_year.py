#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for 'NNth Month' (ordinal-first, no year) pattern → DAY_MONTH.

Examples: '3rd March', '1st January', '23rd December', '3rd Mar'.

Related GitHub Issue:
    #22 - Gap: ordinal day format not supported (12th day of December, 19th day of May)
    https://github.com/craigtrim/fast-parse-time/issues/22
"""

import pytest
from fast_parse_time import extract_explicit_dates


class TestOrdinalNthMonthNoYear:
    """'NNth Month' and 'NNth MonthAbbr' (no year) → DAY_MONTH."""

    # ── full month names ──────────────────────────────────────────────────────

    def test_3rd_march(self):
        result = extract_explicit_dates('3rd March')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_1st_january(self):
        result = extract_explicit_dates('1st January')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_2nd_february(self):
        result = extract_explicit_dates('2nd February')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_4th_april(self):
        result = extract_explicit_dates('4th April')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_5th_may(self):
        result = extract_explicit_dates('5th May')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_15th_june(self):
        result = extract_explicit_dates('15th June')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_21st_july(self):
        result = extract_explicit_dates('21st July')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_22nd_august(self):
        result = extract_explicit_dates('22nd August')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_23rd_september(self):
        result = extract_explicit_dates('23rd September')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_31st_october(self):
        result = extract_explicit_dates('31st October')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_11th_november(self):
        result = extract_explicit_dates('11th November')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_25th_december(self):
        result = extract_explicit_dates('25th December')
        assert result
        assert 'DAY_MONTH' in result.values()

    # ── abbreviated month names ───────────────────────────────────────────────

    def test_3rd_mar(self):
        result = extract_explicit_dates('3rd Mar')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_1st_jan(self):
        result = extract_explicit_dates('1st Jan')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_2nd_feb(self):
        result = extract_explicit_dates('2nd Feb')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_15th_jun(self):
        result = extract_explicit_dates('15th Jun')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_21st_jul(self):
        result = extract_explicit_dates('21st Jul')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_22nd_aug(self):
        result = extract_explicit_dates('22nd Aug')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_23rd_sep(self):
        result = extract_explicit_dates('23rd Sep')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_31st_oct(self):
        result = extract_explicit_dates('31st Oct')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_11th_nov(self):
        result = extract_explicit_dates('11th Nov')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_25th_dec(self):
        result = extract_explicit_dates('25th Dec')
        assert result
        assert 'DAY_MONTH' in result.values()

    # ── case insensitive ──────────────────────────────────────────────────────

    def test_3RD_march_uppercase(self):
        result = extract_explicit_dates('3RD March')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_1ST_january_uppercase(self):
        result = extract_explicit_dates('1ST January')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_21ST_jul_uppercase(self):
        result = extract_explicit_dates('21ST Jul')
        assert result
        assert 'DAY_MONTH' in result.values()

    # ── sentence context ──────────────────────────────────────────────────────

    def test_embedded_3rd_march(self):
        result = extract_explicit_dates('The event is on 3rd March.')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_embedded_1st_january(self):
        result = extract_explicit_dates('It starts 1st January next year.')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_embedded_25th_dec(self):
        result = extract_explicit_dates('Christmas falls on 25th Dec.')
        assert result
        assert 'DAY_MONTH' in result.values()
