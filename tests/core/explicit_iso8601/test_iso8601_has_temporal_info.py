#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Tests for has_temporal_info with ISO 8601 datetime strings.

Related GitHub Issue:
    #23 - Gap: ISO 8601 datetime strings not extracted
    https://github.com/craigtrim/fast-parse-time/issues/23
"""

import pytest
from fast_parse_time import has_temporal_info


class TestIso8601HasTemporalInfo:
    """has_temporal_info returns True for all ISO 8601 datetime variants."""

    # --- Z suffix ---

    def test_z_suffix_basic(self):
        assert has_temporal_info('2017-02-03T09:04:08Z') is True

    def test_z_suffix_different_date(self):
        assert has_temporal_info('2021-11-15T14:30:00Z') is True

    def test_z_suffix_midnight(self):
        assert has_temporal_info('2020-01-01T00:00:00Z') is True

    # --- UTC +00:00 ---

    def test_plus_zero_offset(self):
        assert has_temporal_info('2016-02-04T20:16:26+00:00') is True

    def test_minus_zero_offset(self):
        assert has_temporal_info('2016-02-04T20:16:26-00:00') is True

    # --- Positive offsets ---

    def test_plus_05_30(self):
        assert has_temporal_info('2022-04-15T10:30:00+05:30') is True

    def test_plus_08_00(self):
        assert has_temporal_info('2023-01-15T08:00:00+08:00') is True

    # --- Negative offsets ---

    def test_minus_05_00(self):
        assert has_temporal_info('2022-03-15T09:30:00-05:00') is True

    def test_minus_08_00(self):
        assert has_temporal_info('2021-11-01T06:00:00-08:00') is True

    # --- With milliseconds ---

    def test_dot_millis_z(self):
        assert has_temporal_info('2017-02-03T09:04:08.001Z') is True

    def test_comma_millis_z(self):
        assert has_temporal_info('2017-02-03T09:04:08,00123Z') is True

    # --- In sentence context ---

    def test_in_sentence_z(self):
        assert has_temporal_info('Logged at 2021-06-15T09:00:00Z') is True

    def test_in_sentence_plus_offset(self):
        assert has_temporal_info('Created at 2022-04-15T10:30:00+05:30') is True

    def test_in_sentence_minus_offset(self):
        assert has_temporal_info('Archived at 2022-03-15T09:30:00-05:00') is True

    # --- False cases (no temporal info) ---

    def test_plain_text_false(self):
        assert has_temporal_info('hello world') is False

    def test_random_numbers_false(self):
        assert has_temporal_info('version 3.14.0') is False

    def test_empty_ish_false(self):
        assert has_temporal_info('no date here') is False

    # --- Additional positive cases ---

    def test_z_suffix_leap_day(self):
        assert has_temporal_info('2024-02-29T10:30:00Z') is True

    def test_z_suffix_dec_31(self):
        assert has_temporal_info('2023-12-31T23:59:59Z') is True

    def test_plus_offset_various(self):
        assert has_temporal_info('2020-10-10T10:10:10+02:00') is True

    def test_minus_offset_various(self):
        assert has_temporal_info('2019-12-25T10:00:00-06:00') is True
