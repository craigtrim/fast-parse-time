#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for 'NNth day of Month, YYYY' pattern → FULL_EXPLICIT_DATE.

Related GitHub Issue:
    #22 - Gap: ordinal day format not supported (12th day of December, 19th day of May)
    https://github.com/craigtrim/fast-parse-time/issues/22
"""

import pytest
from fast_parse_time import extract_explicit_dates


class TestOrdinalDayOfMonthWithYear:
    """'NNth day of Month[,] YYYY' → FULL_EXPLICIT_DATE."""

    # ── compat cases (from datefinder test suite) ────────────────────────────

    def test_12th_day_of_december_2001(self):
        result = extract_explicit_dates('12th day of December, 2001')
        assert len(result) >= 1

    def test_19th_day_of_may_2015(self):
        result = extract_explicit_dates('19th day of May, 2015')
        assert len(result) >= 1

    # ── full-month names ──────────────────────────────────────────────────────

    def test_1st_day_of_january_2024(self):
        result = extract_explicit_dates('1st day of January, 2024')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_2nd_day_of_february_2023(self):
        result = extract_explicit_dates('2nd day of February, 2023')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_3rd_day_of_march_2022(self):
        result = extract_explicit_dates('3rd day of March, 2022')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_4th_day_of_april_2021(self):
        result = extract_explicit_dates('4th day of April, 2021')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_15th_day_of_june_2020(self):
        result = extract_explicit_dates('15th day of June, 2020')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_21st_day_of_july_2019(self):
        result = extract_explicit_dates('21st day of July, 2019')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_22nd_day_of_august_2018(self):
        result = extract_explicit_dates('22nd day of August, 2018')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_23rd_day_of_september_2017(self):
        result = extract_explicit_dates('23rd day of September, 2017')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_30th_day_of_october_2016(self):
        result = extract_explicit_dates('30th day of October, 2016')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_11th_day_of_november_2015(self):
        result = extract_explicit_dates('11th day of November, 2015')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_31st_day_of_december_2014(self):
        result = extract_explicit_dates('31st day of December, 2014')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    # ── without comma before year ─────────────────────────────────────────────

    def test_12th_day_of_december_2001_no_comma(self):
        result = extract_explicit_dates('12th day of December 2001')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_5th_day_of_march_2024_no_comma(self):
        result = extract_explicit_dates('5th day of March 2024')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_20th_day_of_june_2019_no_comma(self):
        result = extract_explicit_dates('20th day of June 2019')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    # ── case insensitive ──────────────────────────────────────────────────────

    def test_12TH_day_of_december_uppercase(self):
        result = extract_explicit_dates('12TH day of December, 2001')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_3RD_day_of_march_uppercase(self):
        result = extract_explicit_dates('3RD day of March, 2024')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_21ST_day_of_july_uppercase(self):
        result = extract_explicit_dates('21ST day of July, 2023')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    # ── sentence context ──────────────────────────────────────────────────────

    def test_embedded_12th_day_of_december(self):
        result = extract_explicit_dates('The contract was signed on the 12th day of December, 2001.')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_embedded_19th_day_of_may(self):
        result = extract_explicit_dates('Born on 19th day of May, 2015 in the city.')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_embedded_1st_day_of_january(self):
        result = extract_explicit_dates('Effective 1st day of January, 2024 hereafter.')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()
