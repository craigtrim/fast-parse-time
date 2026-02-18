#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Tests for multiple ISO 8601 datetime strings in a single input.

Related GitHub Issue:
    #23 - Gap: ISO 8601 datetime strings not extracted
    https://github.com/craigtrim/fast-parse-time/issues/23
"""

import pytest
from fast_parse_time import extract_explicit_dates, has_temporal_info


class TestIso8601MultipleInText:
    """Multiple ISO 8601 datetimes in one input are all extracted."""

    def test_two_z_suffix(self):
        result = extract_explicit_dates('start 2021-01-01T00:00:00Z end 2021-12-31T23:59:59Z')
        assert '2021-01-01' in result
        assert '2021-12-31' in result

    def test_two_z_suffix_count(self):
        result = extract_explicit_dates('start 2021-01-01T00:00:00Z end 2021-12-31T23:59:59Z')
        assert len(result) == 2

    def test_two_different_offsets(self):
        result = extract_explicit_dates('from 2022-03-01T08:00:00+05:30 to 2022-03-15T08:00:00-05:00')
        assert '2022-03-01' in result
        assert '2022-03-15' in result

    def test_mixed_formats_z_and_offset(self):
        result = extract_explicit_dates('created 2021-06-01T00:00:00Z updated 2021-09-01T10:00:00+01:00')
        assert '2021-06-01' in result
        assert '2021-09-01' in result

    def test_two_different_dates_not_same(self):
        result = extract_explicit_dates('2020-01-01T00:00:00Z and 2020-06-15T12:00:00Z')
        assert '2020-01-01' in result
        assert '2020-06-15' in result
        assert len(result) == 2

    def test_has_temporal_info_two_datetimes(self):
        assert has_temporal_info('start 2021-01-01T00:00:00Z end 2021-12-31T23:59:59Z') is True

    def test_date_range_same_dates_not_duplicated(self):
        """Same date with different times extracts the date once."""
        result = extract_explicit_dates('from 2022-05-01T08:00:00Z to 2022-05-01T17:00:00Z')
        assert '2022-05-01' in result

    def test_z_plus_offset_both_extracted(self):
        result = extract_explicit_dates('at 2019-03-15T10:00:00Z and 2019-04-15T10:00:00+02:00')
        assert '2019-03-15' in result
        assert '2019-04-15' in result

    def test_first_datetime_correct(self):
        result = extract_explicit_dates('2021-01-15T00:00:00Z and 2021-06-30T12:00:00Z')
        assert '2021-01-15' in result

    def test_second_datetime_correct(self):
        result = extract_explicit_dates('2021-01-15T00:00:00Z and 2021-06-30T12:00:00Z')
        assert '2021-06-30' in result

    def test_with_millis_multiple(self):
        result = extract_explicit_dates('a=2020-03-01T00:00:00.000Z b=2020-09-01T12:00:00.500Z')
        assert '2020-03-01' in result
        assert '2020-09-01' in result

    def test_three_datetimes(self):
        result = extract_explicit_dates(
            '2020-01-01T00:00:00Z then 2020-06-01T00:00:00Z then 2020-12-01T00:00:00Z'
        )
        assert '2020-01-01' in result
        assert '2020-06-01' in result
        assert '2020-12-01' in result
