#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for 'NNth day of Month' (no year) pattern → DAY_MONTH.

Related GitHub Issue:
    #22 - Gap: ordinal day format not supported (12th day of December, 19th day of May)
    https://github.com/craigtrim/fast-parse-time/issues/22
"""

import pytest
from fast_parse_time import extract_explicit_dates


class TestOrdinalDayOfMonthNoYear:
    """'NNth day of Month' (no year) → DAY_MONTH."""

    def test_12th_day_of_december(self):
        result = extract_explicit_dates('12th day of December')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_19th_day_of_may(self):
        result = extract_explicit_dates('19th day of May')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_1st_day_of_january(self):
        result = extract_explicit_dates('1st day of January')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_2nd_day_of_february(self):
        result = extract_explicit_dates('2nd day of February')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_3rd_day_of_march(self):
        result = extract_explicit_dates('3rd day of March')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_15th_day_of_june(self):
        result = extract_explicit_dates('15th day of June')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_21st_day_of_july(self):
        result = extract_explicit_dates('21st day of July')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_22nd_day_of_august(self):
        result = extract_explicit_dates('22nd day of August')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_23rd_day_of_september(self):
        result = extract_explicit_dates('23rd day of September')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_30th_day_of_october(self):
        result = extract_explicit_dates('30th day of October')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_11th_day_of_november(self):
        result = extract_explicit_dates('11th day of November')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_31st_day_of_december(self):
        result = extract_explicit_dates('31st day of December')
        assert result
        assert 'DAY_MONTH' in result.values()

    # ── abbreviated months ────────────────────────────────────────────────────

    def test_12th_day_of_dec(self):
        result = extract_explicit_dates('12th day of Dec')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_5th_day_of_jan(self):
        result = extract_explicit_dates('5th day of Jan')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_3rd_day_of_mar(self):
        result = extract_explicit_dates('3rd day of Mar')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_20th_day_of_sep(self):
        result = extract_explicit_dates('20th day of Sep')
        assert result
        assert 'DAY_MONTH' in result.values()

    # ── case insensitive ──────────────────────────────────────────────────────

    def test_12TH_day_of_december_uppercase(self):
        result = extract_explicit_dates('12TH day of December')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_3RD_day_of_march_uppercase(self):
        result = extract_explicit_dates('3RD day of March')
        assert result
        assert 'DAY_MONTH' in result.values()

    # ── sentence context ──────────────────────────────────────────────────────

    def test_embedded_in_sentence(self):
        result = extract_explicit_dates('Please report on the 12th day of December.')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_embedded_meeting(self):
        result = extract_explicit_dates('The meeting is set for the 3rd day of March.')
        assert result
        assert 'DAY_MONTH' in result.values()
