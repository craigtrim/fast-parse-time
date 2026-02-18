#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Edge case and boundary tests for ISO 8601 datetime extraction.

Related GitHub Issue:
    #23 - Gap: ISO 8601 datetime strings not extracted
    https://github.com/craigtrim/fast-parse-time/issues/23
"""

import pytest
from fast_parse_time import extract_explicit_dates, has_temporal_info


class TestIso8601EdgeCases:
    """Edge cases and boundary conditions for ISO 8601 extraction."""

    def test_start_of_epoch(self):
        result = extract_explicit_dates('1970-01-01T00:00:00Z')
        assert '1970-01-01' in result

    def test_y2k(self):
        result = extract_explicit_dates('2000-01-01T00:00:00Z')
        assert '2000-01-01' in result

    def test_max_seconds(self):
        result = extract_explicit_dates('2022-08-15T23:59:59Z')
        assert '2022-08-15' in result

    def test_single_digit_hour_padded(self):
        result = extract_explicit_dates('2023-04-01T09:05:03Z')
        assert '2023-04-01' in result

    def test_high_microseconds(self):
        result = extract_explicit_dates('2021-07-07T07:07:07.999999Z')
        assert '2021-07-07' in result

    def test_full_offset_plus_12(self):
        result = extract_explicit_dates('2022-03-20T08:00:00+12:00')
        assert '2022-03-20' in result

    def test_full_offset_minus_11(self):
        result = extract_explicit_dates('2022-03-20T08:00:00-11:00')
        assert '2022-03-20' in result

    def test_no_t_no_match(self):
        """Plain YYYY-MM-DD without T is still handled (not broken)."""
        result = extract_explicit_dates('2017-02-03')
        assert result is not None

    def test_iso_in_brackets(self):
        result = extract_explicit_dates('[2022-11-11T11:11:11Z]')
        assert '2022-11-11' in result

    def test_iso_in_quotes(self):
        result = extract_explicit_dates('"2022-11-11T11:11:11Z"')
        assert '2022-11-11' in result

    def test_has_temporal_info_epoch(self):
        assert has_temporal_info('1970-01-01T00:00:00Z') is True

    def test_has_temporal_info_y2k(self):
        assert has_temporal_info('2000-01-01T00:00:00Z') is True

    def test_result_not_bool(self):
        result = extract_explicit_dates('2022-05-05T05:05:05Z')
        assert not isinstance(result, bool)

    def test_result_is_dict_type(self):
        result = extract_explicit_dates('2022-05-05T05:05:05Z')
        assert isinstance(result, dict)

    def test_three_digit_millis_plus_offset(self):
        result = extract_explicit_dates('2021-06-21T14:00:00.123+01:00')
        assert '2021-06-21' in result
