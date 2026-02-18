#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Tests for ISO 8601 datetime strings with Z (UTC) suffix.

Related GitHub Issue:
    #23 - Gap: ISO 8601 datetime strings not extracted
    https://github.com/craigtrim/fast-parse-time/issues/23

Covers: YYYY-MM-DDThh:mm:ssZ patterns.
"""

import pytest
from fast_parse_time import extract_explicit_dates


class TestIso8601ZSuffix:
    """ISO 8601 datetimes with Z suffix extract the date portion as FULL_EXPLICIT_DATE."""

    def test_basic_z_suffix(self):
        result = extract_explicit_dates('2017-02-03T09:04:08Z')
        assert result == {'2017-02-03': 'FULL_EXPLICIT_DATE'}

    def test_z_suffix_different_date(self):
        result = extract_explicit_dates('2021-11-15T14:30:00Z')
        assert result == {'2021-11-15': 'FULL_EXPLICIT_DATE'}

    def test_z_suffix_jan_first(self):
        result = extract_explicit_dates('2020-01-01T00:00:00Z')
        assert result == {'2020-01-01': 'FULL_EXPLICIT_DATE'}

    def test_z_suffix_dec_31(self):
        result = extract_explicit_dates('2023-12-31T23:59:59Z')
        assert result == {'2023-12-31': 'FULL_EXPLICIT_DATE'}

    def test_z_suffix_midnight(self):
        result = extract_explicit_dates('2022-06-15T00:00:00Z')
        assert result == {'2022-06-15': 'FULL_EXPLICIT_DATE'}

    def test_z_suffix_noon(self):
        result = extract_explicit_dates('2022-06-15T12:00:00Z')
        assert result == {'2022-06-15': 'FULL_EXPLICIT_DATE'}

    def test_z_suffix_end_of_day(self):
        result = extract_explicit_dates('2022-06-15T23:59:59Z')
        assert result == {'2022-06-15': 'FULL_EXPLICIT_DATE'}

    def test_z_suffix_leap_day(self):
        result = extract_explicit_dates('2024-02-29T10:30:00Z')
        assert result == {'2024-02-29': 'FULL_EXPLICIT_DATE'}

    def test_z_suffix_single_digit_month_padded(self):
        result = extract_explicit_dates('2019-03-07T08:15:00Z')
        assert result == {'2019-03-07': 'FULL_EXPLICIT_DATE'}

    def test_z_suffix_returns_one_entry(self):
        result = extract_explicit_dates('2017-02-03T09:04:08Z')
        assert len(result) == 1

    def test_z_suffix_key_is_date_only(self):
        result = extract_explicit_dates('2017-02-03T09:04:08Z')
        assert '2017-02-03' in result

    def test_z_suffix_value_is_full_explicit(self):
        result = extract_explicit_dates('2017-02-03T09:04:08Z')
        assert result['2017-02-03'] == 'FULL_EXPLICIT_DATE'

    def test_z_suffix_not_empty(self):
        result = extract_explicit_dates('2017-02-03T09:04:08Z')
        assert result

    def test_z_suffix_2000(self):
        result = extract_explicit_dates('2000-01-01T00:00:00Z')
        assert result == {'2000-01-01': 'FULL_EXPLICIT_DATE'}

    def test_z_suffix_early_time(self):
        result = extract_explicit_dates('2018-08-20T01:02:03Z')
        assert result == {'2018-08-20': 'FULL_EXPLICIT_DATE'}

    def test_z_suffix_from_issue(self):
        """Exact example from issue #23."""
        result = extract_explicit_dates('2017-02-03T09:04:08Z')
        assert result == {'2017-02-03': 'FULL_EXPLICIT_DATE'}

    def test_z_suffix_all_zeros_time(self):
        result = extract_explicit_dates('2015-05-05T00:00:00Z')
        assert result == {'2015-05-05': 'FULL_EXPLICIT_DATE'}

    def test_z_suffix_max_time(self):
        result = extract_explicit_dates('2015-05-05T23:59:59Z')
        assert result == {'2015-05-05': 'FULL_EXPLICIT_DATE'}

    def test_z_suffix_2016(self):
        result = extract_explicit_dates('2016-07-04T16:30:00Z')
        assert result == {'2016-07-04': 'FULL_EXPLICIT_DATE'}

    def test_z_suffix_october(self):
        result = extract_explicit_dates('2023-10-31T11:11:11Z')
        assert result == {'2023-10-31': 'FULL_EXPLICIT_DATE'}
