#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for 'the NNth of Month [YYYY]' pattern.

With year → FULL_EXPLICIT_DATE.
Without year → DAY_MONTH.

Related GitHub Issue:
    #22 - Gap: ordinal day format not supported (12th day of December, 19th day of May)
    https://github.com/craigtrim/fast-parse-time/issues/22
"""

import pytest
from fast_parse_time import extract_explicit_dates


class TestOrdinalTheNthOfMonth:
    """'the NNth of Month [YYYY]' pattern."""

    # ── with year → FULL_EXPLICIT_DATE ───────────────────────────────────────

    def test_the_12th_of_december_2024(self):
        result = extract_explicit_dates('the 12th of December 2024')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_the_1st_of_january_2024(self):
        result = extract_explicit_dates('the 1st of January 2024')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_the_2nd_of_february_2023(self):
        result = extract_explicit_dates('the 2nd of February 2023')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_the_3rd_of_march_2022(self):
        result = extract_explicit_dates('the 3rd of March 2022')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_the_15th_of_june_2021(self):
        result = extract_explicit_dates('the 15th of June 2021')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_the_21st_of_july_2020(self):
        result = extract_explicit_dates('the 21st of July 2020')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_the_22nd_of_august_2019(self):
        result = extract_explicit_dates('the 22nd of August 2019')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_the_23rd_of_september_2018(self):
        result = extract_explicit_dates('the 23rd of September 2018')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_the_31st_of_october_2017(self):
        result = extract_explicit_dates('the 31st of October 2017')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_the_11th_of_november_2016(self):
        result = extract_explicit_dates('the 11th of November 2016')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    # ── with abbreviated month + year ─────────────────────────────────────────

    def test_the_12th_of_dec_2024(self):
        result = extract_explicit_dates('the 12th of Dec 2024')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_the_5th_of_jan_2023(self):
        result = extract_explicit_dates('the 5th of Jan 2023')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_the_3rd_of_mar_2022(self):
        result = extract_explicit_dates('the 3rd of Mar 2022')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    # ── without year → DAY_MONTH ──────────────────────────────────────────────

    def test_the_12th_of_december(self):
        result = extract_explicit_dates('the 12th of December')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_the_1st_of_january(self):
        result = extract_explicit_dates('the 1st of January')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_the_2nd_of_february(self):
        result = extract_explicit_dates('the 2nd of February')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_the_3rd_of_march(self):
        result = extract_explicit_dates('the 3rd of March')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_the_15th_of_june(self):
        result = extract_explicit_dates('the 15th of June')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_the_21st_of_july(self):
        result = extract_explicit_dates('the 21st of July')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_the_31st_of_december(self):
        result = extract_explicit_dates('the 31st of December')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_the_12th_of_dec(self):
        result = extract_explicit_dates('the 12th of Dec')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_the_5th_of_jan(self):
        result = extract_explicit_dates('the 5th of Jan')
        assert result
        assert 'DAY_MONTH' in result.values()

    # ── case insensitive ──────────────────────────────────────────────────────

    def test_the_12TH_of_december(self):
        result = extract_explicit_dates('the 12TH of December')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_the_3RD_of_march_2024(self):
        result = extract_explicit_dates('the 3RD of March 2024')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    # ── sentence context ──────────────────────────────────────────────────────

    def test_embedded_meeting_on_the_3rd(self):
        result = extract_explicit_dates('meeting on the 3rd of March 2024 at noon')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_embedded_born_on_the_12th(self):
        result = extract_explicit_dates('She was born on the 12th of December.')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_embedded_contract_signed(self):
        result = extract_explicit_dates('The contract was signed on the 1st of January 2024.')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()
