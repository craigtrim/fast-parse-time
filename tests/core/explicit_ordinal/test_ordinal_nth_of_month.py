#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for 'NNth of Month [YYYY]' pattern (no article 'the').

With year → FULL_EXPLICIT_DATE.
Without year → DAY_MONTH.

Related GitHub Issue:
    #22 - Gap: ordinal day format not supported (12th day of December, 19th day of May)
    https://github.com/craigtrim/fast-parse-time/issues/22
"""

import pytest
from fast_parse_time import extract_explicit_dates


class TestOrdinalNthOfMonth:
    """'NNth of Month [YYYY]' (no article) pattern."""

    # ── with year → FULL_EXPLICIT_DATE ───────────────────────────────────────

    def test_2nd_of_february_2023(self):
        result = extract_explicit_dates('2nd of February 2023')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_1st_of_january_2024(self):
        result = extract_explicit_dates('1st of January 2024')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_3rd_of_march_2022(self):
        result = extract_explicit_dates('3rd of March 2022')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_4th_of_april_2021(self):
        result = extract_explicit_dates('4th of April 2021')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_15th_of_june_2020(self):
        result = extract_explicit_dates('15th of June 2020')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_21st_of_july_2019(self):
        result = extract_explicit_dates('21st of July 2019')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_22nd_of_august_2018(self):
        result = extract_explicit_dates('22nd of August 2018')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_23rd_of_september_2017(self):
        result = extract_explicit_dates('23rd of September 2017')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_31st_of_october_2016(self):
        result = extract_explicit_dates('31st of October 2016')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_11th_of_november_2015(self):
        result = extract_explicit_dates('11th of November 2015')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_12th_of_december_2014(self):
        result = extract_explicit_dates('12th of December 2014')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_5th_of_may_2024(self):
        result = extract_explicit_dates('5th of May 2024')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    # ── with abbreviated month + year ─────────────────────────────────────────

    def test_2nd_of_feb_2023(self):
        result = extract_explicit_dates('2nd of Feb 2023')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_12th_of_dec_2024(self):
        result = extract_explicit_dates('12th of Dec 2024')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_3rd_of_mar_2022(self):
        result = extract_explicit_dates('3rd of Mar 2022')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_5th_of_oct_2019(self):
        result = extract_explicit_dates('5th of Oct 2019')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    # ── without year → DAY_MONTH ──────────────────────────────────────────────

    def test_2nd_of_february(self):
        result = extract_explicit_dates('2nd of February')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_1st_of_january(self):
        result = extract_explicit_dates('1st of January')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_3rd_of_march(self):
        result = extract_explicit_dates('3rd of March')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_15th_of_june(self):
        result = extract_explicit_dates('15th of June')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_21st_of_july(self):
        result = extract_explicit_dates('21st of July')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_12th_of_december(self):
        result = extract_explicit_dates('12th of December')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_31st_of_january(self):
        result = extract_explicit_dates('31st of January')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_2nd_of_feb(self):
        result = extract_explicit_dates('2nd of Feb')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_12th_of_dec(self):
        result = extract_explicit_dates('12th of Dec')
        assert result
        assert 'DAY_MONTH' in result.values()

    # ── case insensitive ──────────────────────────────────────────────────────

    def test_2ND_of_february_2023_uppercase(self):
        result = extract_explicit_dates('2ND of February 2023')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_12TH_of_december_uppercase(self):
        result = extract_explicit_dates('12TH of December')
        assert result
        assert 'DAY_MONTH' in result.values()

    # ── sentence context ──────────────────────────────────────────────────────

    def test_embedded_born_2nd_of_february(self):
        result = extract_explicit_dates('She was born 2nd of February 2023 in London.')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_embedded_report_12th_of_december(self):
        result = extract_explicit_dates('Submit by 12th of December.')
        assert result
        assert 'DAY_MONTH' in result.values()
