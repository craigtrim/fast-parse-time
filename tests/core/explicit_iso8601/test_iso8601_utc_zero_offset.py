#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Tests for ISO 8601 datetime strings with +00:00 UTC offset.

Related GitHub Issue:
    #23 - Gap: ISO 8601 datetime strings not extracted
    https://github.com/craigtrim/fast-parse-time/issues/23

Covers: YYYY-MM-DDThh:mm:ss+00:00 patterns (explicit UTC offset zero).
"""

import pytest
from fast_parse_time import extract_explicit_dates


class TestIso8601UtcZeroOffset:
    """ISO 8601 datetimes with +00:00 extract the date portion correctly."""

    def test_plus_zero_basic(self):
        """Exact example from issue #23."""
        result = extract_explicit_dates('2016-02-04T20:16:26+00:00')
        assert result == {'2016-02-04': 'FULL_EXPLICIT_DATE'}

    def test_plus_zero_different_date(self):
        result = extract_explicit_dates('2021-07-20T08:45:00+00:00')
        assert result == {'2021-07-20': 'FULL_EXPLICIT_DATE'}

    def test_plus_zero_jan_first(self):
        result = extract_explicit_dates('2020-01-01T00:00:00+00:00')
        assert result == {'2020-01-01': 'FULL_EXPLICIT_DATE'}

    def test_plus_zero_dec_31(self):
        result = extract_explicit_dates('2023-12-31T23:59:59+00:00')
        assert result == {'2023-12-31': 'FULL_EXPLICIT_DATE'}

    def test_plus_zero_not_empty(self):
        result = extract_explicit_dates('2016-02-04T20:16:26+00:00')
        assert result

    def test_plus_zero_one_entry(self):
        result = extract_explicit_dates('2016-02-04T20:16:26+00:00')
        assert len(result) == 1

    def test_plus_zero_key_is_date(self):
        result = extract_explicit_dates('2016-02-04T20:16:26+00:00')
        assert '2016-02-04' in result

    def test_plus_zero_value_is_full_explicit(self):
        result = extract_explicit_dates('2016-02-04T20:16:26+00:00')
        assert result['2016-02-04'] == 'FULL_EXPLICIT_DATE'

    def test_minus_zero(self):
        result = extract_explicit_dates('2016-02-04T20:16:26-00:00')
        assert result == {'2016-02-04': 'FULL_EXPLICIT_DATE'}

    def test_plus_zero_noon(self):
        result = extract_explicit_dates('2022-09-15T12:00:00+00:00')
        assert result == {'2022-09-15': 'FULL_EXPLICIT_DATE'}

    def test_plus_zero_midnight(self):
        result = extract_explicit_dates('2022-09-15T00:00:00+00:00')
        assert result == {'2022-09-15': 'FULL_EXPLICIT_DATE'}

    def test_plus_zero_2017(self):
        result = extract_explicit_dates('2017-11-11T11:11:11+00:00')
        assert result == {'2017-11-11': 'FULL_EXPLICIT_DATE'}

    def test_plus_zero_leap_day(self):
        result = extract_explicit_dates('2024-02-29T15:00:00+00:00')
        assert result == {'2024-02-29': 'FULL_EXPLICIT_DATE'}

    def test_plus_zero_march(self):
        result = extract_explicit_dates('2019-03-01T09:30:00+00:00')
        assert result == {'2019-03-01': 'FULL_EXPLICIT_DATE'}
