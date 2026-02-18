#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests covering all valid ordinal suffixes (1st through 31st) across pattern families.

Related GitHub Issue:
    #22 - Gap: ordinal day format not supported (12th day of December, 19th day of May)
    https://github.com/craigtrim/fast-parse-time/issues/22
"""

import pytest
from fast_parse_time import extract_explicit_dates


class TestOrdinalAllSuffixes:
    """Every valid ordinal day value should be recognized."""

    # ── 'NNth of Month' covering all calendar days ────────────────────────────

    def test_1st_of_march(self):
        assert 'DAY_MONTH' in extract_explicit_dates('1st of March').values()

    def test_2nd_of_march(self):
        assert 'DAY_MONTH' in extract_explicit_dates('2nd of March').values()

    def test_3rd_of_march(self):
        assert 'DAY_MONTH' in extract_explicit_dates('3rd of March').values()

    def test_4th_of_march(self):
        assert 'DAY_MONTH' in extract_explicit_dates('4th of March').values()

    def test_5th_of_march(self):
        assert 'DAY_MONTH' in extract_explicit_dates('5th of march').values()

    def test_6th_of_march(self):
        assert 'DAY_MONTH' in extract_explicit_dates('6th of march').values()

    def test_7th_of_march(self):
        assert 'DAY_MONTH' in extract_explicit_dates('7th of march').values()

    def test_8th_of_march(self):
        assert 'DAY_MONTH' in extract_explicit_dates('8th of march').values()

    def test_9th_of_march(self):
        assert 'DAY_MONTH' in extract_explicit_dates('9th of march').values()

    def test_10th_of_march(self):
        assert 'DAY_MONTH' in extract_explicit_dates('10th of march').values()

    def test_11th_of_march(self):
        assert 'DAY_MONTH' in extract_explicit_dates('11th of march').values()

    def test_12th_of_march(self):
        assert 'DAY_MONTH' in extract_explicit_dates('12th of march').values()

    def test_13th_of_march(self):
        assert 'DAY_MONTH' in extract_explicit_dates('13th of march').values()

    def test_14th_of_march(self):
        assert 'DAY_MONTH' in extract_explicit_dates('14th of march').values()

    def test_15th_of_march(self):
        assert 'DAY_MONTH' in extract_explicit_dates('15th of march').values()

    def test_16th_of_march(self):
        assert 'DAY_MONTH' in extract_explicit_dates('16th of march').values()

    def test_17th_of_march(self):
        assert 'DAY_MONTH' in extract_explicit_dates('17th of march').values()

    def test_18th_of_march(self):
        assert 'DAY_MONTH' in extract_explicit_dates('18th of march').values()

    def test_19th_of_march(self):
        assert 'DAY_MONTH' in extract_explicit_dates('19th of march').values()

    def test_20th_of_march(self):
        assert 'DAY_MONTH' in extract_explicit_dates('20th of march').values()

    def test_21st_of_march(self):
        assert 'DAY_MONTH' in extract_explicit_dates('21st of march').values()

    def test_22nd_of_march(self):
        assert 'DAY_MONTH' in extract_explicit_dates('22nd of march').values()

    def test_23rd_of_march(self):
        assert 'DAY_MONTH' in extract_explicit_dates('23rd of march').values()

    def test_24th_of_march(self):
        assert 'DAY_MONTH' in extract_explicit_dates('24th of march').values()

    def test_25th_of_march(self):
        assert 'DAY_MONTH' in extract_explicit_dates('25th of march').values()

    def test_26th_of_march(self):
        assert 'DAY_MONTH' in extract_explicit_dates('26th of march').values()

    def test_27th_of_march(self):
        assert 'DAY_MONTH' in extract_explicit_dates('27th of march').values()

    def test_28th_of_march(self):
        assert 'DAY_MONTH' in extract_explicit_dates('28th of march').values()

    def test_29th_of_march(self):
        assert 'DAY_MONTH' in extract_explicit_dates('29th of march').values()

    def test_30th_of_march(self):
        assert 'DAY_MONTH' in extract_explicit_dates('30th of march').values()

    def test_31st_of_march(self):
        assert 'DAY_MONTH' in extract_explicit_dates('31st of march').values()

    # ── ordinal suffix correctness (st/nd/rd/th applied correctly) ────────────

    def test_21st_suffix(self):
        assert 'DAY_MONTH' in extract_explicit_dates('21st of January').values()

    def test_22nd_suffix(self):
        assert 'DAY_MONTH' in extract_explicit_dates('22nd of January').values()

    def test_23rd_suffix(self):
        assert 'DAY_MONTH' in extract_explicit_dates('23rd of January').values()

    def test_24th_suffix(self):
        assert 'DAY_MONTH' in extract_explicit_dates('24th of January').values()

    def test_31st_suffix(self):
        assert 'DAY_MONTH' in extract_explicit_dates('31st of January').values()

    def test_11th_suffix(self):
        assert 'DAY_MONTH' in extract_explicit_dates('11th of January').values()

    def test_12th_suffix(self):
        assert 'DAY_MONTH' in extract_explicit_dates('12th of January').values()

    def test_13th_suffix(self):
        assert 'DAY_MONTH' in extract_explicit_dates('13th of January').values()
