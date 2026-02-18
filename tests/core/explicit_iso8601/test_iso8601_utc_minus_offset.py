#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Tests for ISO 8601 datetime strings with negative UTC offset (-HH:MM).

Related GitHub Issue:
    #23 - Gap: ISO 8601 datetime strings not extracted
    https://github.com/craigtrim/fast-parse-time/issues/23

Covers: YYYY-MM-DDThh:mm:ss-HH:MM (negative UTC offsets).
"""

import pytest
from fast_parse_time import extract_explicit_dates


class TestIso8601UtcMinusOffset:
    """ISO 8601 datetimes with negative UTC offset extract the date correctly."""

    def test_minus_05_00(self):
        """US Eastern Standard Time."""
        result = extract_explicit_dates('2022-03-15T09:30:00-05:00')
        assert result == {'2022-03-15': 'FULL_EXPLICIT_DATE'}

    def test_minus_08_00(self):
        """US Pacific Standard Time."""
        result = extract_explicit_dates('2021-11-01T06:00:00-08:00')
        assert result == {'2021-11-01': 'FULL_EXPLICIT_DATE'}

    def test_minus_07_00(self):
        """US Mountain Standard Time."""
        result = extract_explicit_dates('2020-07-04T08:00:00-07:00')
        assert result == {'2020-07-04': 'FULL_EXPLICIT_DATE'}

    def test_minus_06_00(self):
        """US Central Standard Time."""
        result = extract_explicit_dates('2019-12-25T10:00:00-06:00')
        assert result == {'2019-12-25': 'FULL_EXPLICIT_DATE'}

    def test_minus_03_00(self):
        """Brazil Time."""
        result = extract_explicit_dates('2023-06-01T14:30:00-03:00')
        assert result == {'2023-06-01': 'FULL_EXPLICIT_DATE'}

    def test_minus_04_00(self):
        result = extract_explicit_dates('2022-09-10T11:00:00-04:00')
        assert result == {'2022-09-10': 'FULL_EXPLICIT_DATE'}

    def test_minus_12_00(self):
        """Baker Island (max negative offset)."""
        result = extract_explicit_dates('2020-01-01T00:00:00-12:00')
        assert result == {'2020-01-01': 'FULL_EXPLICIT_DATE'}

    def test_minus_offset_not_empty(self):
        result = extract_explicit_dates('2022-03-15T09:30:00-05:00')
        assert result

    def test_minus_offset_one_entry(self):
        result = extract_explicit_dates('2022-03-15T09:30:00-05:00')
        assert len(result) == 1

    def test_minus_offset_key_is_date(self):
        result = extract_explicit_dates('2022-03-15T09:30:00-05:00')
        assert '2022-03-15' in result

    def test_minus_offset_value_is_full_explicit(self):
        result = extract_explicit_dates('2022-03-15T09:30:00-05:00')
        assert result['2022-03-15'] == 'FULL_EXPLICIT_DATE'

    def test_minus_09_00(self):
        result = extract_explicit_dates('2021-05-05T05:05:05-09:00')
        assert result == {'2021-05-05': 'FULL_EXPLICIT_DATE'}

    def test_minus_02_30(self):
        """Newfoundland Standard Time."""
        result = extract_explicit_dates('2022-02-14T20:00:00-02:30')
        assert result == {'2022-02-14': 'FULL_EXPLICIT_DATE'}

    def test_minus_01_00(self):
        result = extract_explicit_dates('2023-08-08T08:08:08-01:00')
        assert result == {'2023-08-08': 'FULL_EXPLICIT_DATE'}

    def test_minus_offset_leap_day(self):
        result = extract_explicit_dates('2024-02-29T18:00:00-05:00')
        assert result == {'2024-02-29': 'FULL_EXPLICIT_DATE'}
