#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Tests for ISO 8601 datetime strings with milliseconds/fractional seconds.

Related GitHub Issue:
    #23 - Gap: ISO 8601 datetime strings not extracted
    https://github.com/craigtrim/fast-parse-time/issues/23

Covers:
    YYYY-MM-DDThh:mm:ss.NNNZ   (dot-decimal milliseconds)
    YYYY-MM-DDThh:mm:ss,NNNZ   (comma-decimal milliseconds)
    YYYY-MM-DDThh:mm:ss.NNNNNNZ  (microseconds)
"""

import pytest
from fast_parse_time import extract_explicit_dates


class TestIso8601WithMilliseconds:
    """ISO 8601 datetimes with fractional seconds extract the date correctly."""

    # --- dot-decimal milliseconds + Z ---

    def test_dot_millis_3_digits(self):
        result = extract_explicit_dates('2017-02-03T09:04:08.001Z')
        assert result == {'2017-02-03': 'FULL_EXPLICIT_DATE'}

    def test_dot_millis_zero(self):
        result = extract_explicit_dates('2021-05-10T12:00:00.000Z')
        assert result == {'2021-05-10': 'FULL_EXPLICIT_DATE'}

    def test_dot_millis_999(self):
        result = extract_explicit_dates('2021-05-10T12:00:00.999Z')
        assert result == {'2021-05-10': 'FULL_EXPLICIT_DATE'}

    def test_dot_millis_1_digit(self):
        result = extract_explicit_dates('2020-03-15T08:30:00.5Z')
        assert result == {'2020-03-15': 'FULL_EXPLICIT_DATE'}

    def test_dot_millis_2_digits(self):
        result = extract_explicit_dates('2020-03-15T08:30:00.50Z')
        assert result == {'2020-03-15': 'FULL_EXPLICIT_DATE'}

    def test_dot_millis_6_digits(self):
        result = extract_explicit_dates('2022-11-01T15:45:30.123456Z')
        assert result == {'2022-11-01': 'FULL_EXPLICIT_DATE'}

    def test_dot_millis_date_correct(self):
        result = extract_explicit_dates('2019-09-09T09:09:09.009Z')
        assert '2019-09-09' in result

    def test_dot_millis_not_empty(self):
        result = extract_explicit_dates('2017-02-03T09:04:08.001Z')
        assert result

    def test_dot_millis_one_entry(self):
        result = extract_explicit_dates('2017-02-03T09:04:08.001Z')
        assert len(result) == 1

    # --- dot-decimal milliseconds + UTC offset ---

    def test_dot_millis_plus_offset(self):
        result = extract_explicit_dates('2022-04-01T10:00:00.500+05:30')
        assert result == {'2022-04-01': 'FULL_EXPLICIT_DATE'}

    def test_dot_millis_minus_offset(self):
        result = extract_explicit_dates('2022-04-01T10:00:00.500-07:00')
        assert result == {'2022-04-01': 'FULL_EXPLICIT_DATE'}

    # --- comma-decimal milliseconds (RFC 3339 variant) ---

    def test_comma_millis_from_issue(self):
        """Exact comma-decimal example from issue #23."""
        result = extract_explicit_dates('2017-02-03T09:04:08,00123Z')
        assert result == {'2017-02-03': 'FULL_EXPLICIT_DATE'}

    def test_comma_millis_3_digits(self):
        result = extract_explicit_dates('2021-08-12T06:30:00,500Z')
        assert result == {'2021-08-12': 'FULL_EXPLICIT_DATE'}

    def test_comma_millis_zero(self):
        result = extract_explicit_dates('2021-08-12T06:30:00,000Z')
        assert result == {'2021-08-12': 'FULL_EXPLICIT_DATE'}

    def test_comma_millis_not_empty(self):
        result = extract_explicit_dates('2017-02-03T09:04:08,00123Z')
        assert result

    def test_comma_millis_one_entry(self):
        result = extract_explicit_dates('2017-02-03T09:04:08,00123Z')
        assert len(result) == 1

    def test_comma_millis_key_is_date(self):
        result = extract_explicit_dates('2017-02-03T09:04:08,00123Z')
        assert '2017-02-03' in result

    def test_dot_millis_dec_31(self):
        result = extract_explicit_dates('2023-12-31T23:59:59.999Z')
        assert result == {'2023-12-31': 'FULL_EXPLICIT_DATE'}

    def test_dot_millis_jan_first(self):
        result = extract_explicit_dates('2024-01-01T00:00:00.000Z')
        assert result == {'2024-01-01': 'FULL_EXPLICIT_DATE'}
