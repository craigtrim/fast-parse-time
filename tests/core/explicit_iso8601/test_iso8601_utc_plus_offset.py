#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Tests for ISO 8601 datetime strings with positive UTC offset (+HH:MM).

Related GitHub Issue:
    #23 - Gap: ISO 8601 datetime strings not extracted
    https://github.com/craigtrim/fast-parse-time/issues/23

Covers: YYYY-MM-DDThh:mm:ss+HH:MM (non-zero positive offsets).
"""

import pytest
from fast_parse_time import extract_explicit_dates


class TestIso8601UtcPlusOffset:
    """ISO 8601 datetimes with positive UTC offset extract the date correctly."""

    def test_plus_05_30(self):
        """India Standard Time."""
        result = extract_explicit_dates('2022-04-15T10:30:00+05:30')
        assert result == {'2022-04-15': 'FULL_EXPLICIT_DATE'}

    def test_plus_01_00(self):
        """Central European Time."""
        result = extract_explicit_dates('2021-06-21T14:00:00+01:00')
        assert result == {'2021-06-21': 'FULL_EXPLICIT_DATE'}

    def test_plus_02_00(self):
        result = extract_explicit_dates('2020-10-10T10:10:10+02:00')
        assert result == {'2020-10-10': 'FULL_EXPLICIT_DATE'}

    def test_plus_03_00(self):
        result = extract_explicit_dates('2019-03-20T07:00:00+03:00')
        assert result == {'2019-03-20': 'FULL_EXPLICIT_DATE'}

    def test_plus_08_00(self):
        """China Standard Time."""
        result = extract_explicit_dates('2023-01-15T08:00:00+08:00')
        assert result == {'2023-01-15': 'FULL_EXPLICIT_DATE'}

    def test_plus_09_00(self):
        """Japan Standard Time."""
        result = extract_explicit_dates('2021-11-03T18:45:00+09:00')
        assert result == {'2021-11-03': 'FULL_EXPLICIT_DATE'}

    def test_plus_09_30(self):
        """Australia Central Time."""
        result = extract_explicit_dates('2022-07-04T11:30:00+09:30')
        assert result == {'2022-07-04': 'FULL_EXPLICIT_DATE'}

    def test_plus_10_00(self):
        """Australia Eastern Time."""
        result = extract_explicit_dates('2022-02-20T09:15:00+10:00')
        assert result == {'2022-02-20': 'FULL_EXPLICIT_DATE'}

    def test_plus_05_00(self):
        """Pakistan Standard Time."""
        result = extract_explicit_dates('2021-08-14T12:00:00+05:00')
        assert result == {'2021-08-14': 'FULL_EXPLICIT_DATE'}

    def test_plus_04_00(self):
        result = extract_explicit_dates('2023-06-01T06:00:00+04:00')
        assert result == {'2023-06-01': 'FULL_EXPLICIT_DATE'}

    def test_plus_offset_not_empty(self):
        result = extract_explicit_dates('2022-04-15T10:30:00+05:30')
        assert result

    def test_plus_offset_one_entry(self):
        result = extract_explicit_dates('2022-04-15T10:30:00+05:30')
        assert len(result) == 1

    def test_plus_offset_key_is_date(self):
        result = extract_explicit_dates('2022-04-15T10:30:00+05:30')
        assert '2022-04-15' in result

    def test_plus_offset_value_is_full_explicit(self):
        result = extract_explicit_dates('2022-04-15T10:30:00+05:30')
        assert result['2022-04-15'] == 'FULL_EXPLICIT_DATE'

    def test_plus_14_00(self):
        """Line Islands (max positive offset)."""
        result = extract_explicit_dates('2020-12-31T23:00:00+14:00')
        assert result == {'2020-12-31': 'FULL_EXPLICIT_DATE'}

    def test_plus_06_30(self):
        """Myanmar Time."""
        result = extract_explicit_dates('2022-05-05T05:05:05+06:30')
        assert result == {'2022-05-05': 'FULL_EXPLICIT_DATE'}

    def test_plus_03_30(self):
        """Iran Standard Time."""
        result = extract_explicit_dates('2021-03-21T09:00:00+03:30')
        assert result == {'2021-03-21': 'FULL_EXPLICIT_DATE'}

    def test_plus_offset_leap_day(self):
        result = extract_explicit_dates('2024-02-29T10:00:00+05:30')
        assert result == {'2024-02-29': 'FULL_EXPLICIT_DATE'}
