#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Tests verifying the extracted date component is accurate for all months/days.

Related GitHub Issue:
    #23 - Gap: ISO 8601 datetime strings not extracted
    https://github.com/craigtrim/fast-parse-time/issues/23

Ensures the correct YYYY-MM-DD is extracted regardless of the time/timezone.
"""

import pytest
from fast_parse_time import extract_explicit_dates


class TestIso8601DateCorrectness:
    """The date portion extracted from ISO 8601 strings is accurate."""

    def test_january(self):
        result = extract_explicit_dates('2023-01-15T12:00:00Z')
        assert '2023-01-15' in result

    def test_february(self):
        result = extract_explicit_dates('2023-02-28T12:00:00Z')
        assert '2023-02-28' in result

    def test_march(self):
        result = extract_explicit_dates('2023-03-31T12:00:00Z')
        assert '2023-03-31' in result

    def test_april(self):
        result = extract_explicit_dates('2023-04-30T12:00:00Z')
        assert '2023-04-30' in result

    def test_may(self):
        result = extract_explicit_dates('2023-05-01T12:00:00Z')
        assert '2023-05-01' in result

    def test_june(self):
        result = extract_explicit_dates('2023-06-15T12:00:00Z')
        assert '2023-06-15' in result

    def test_july(self):
        result = extract_explicit_dates('2023-07-04T12:00:00Z')
        assert '2023-07-04' in result

    def test_august(self):
        result = extract_explicit_dates('2023-08-20T12:00:00Z')
        assert '2023-08-20' in result

    def test_september(self):
        result = extract_explicit_dates('2023-09-01T12:00:00Z')
        assert '2023-09-01' in result

    def test_october(self):
        result = extract_explicit_dates('2023-10-31T12:00:00Z')
        assert '2023-10-31' in result

    def test_november(self):
        result = extract_explicit_dates('2023-11-11T12:00:00Z')
        assert '2023-11-11' in result

    def test_december(self):
        result = extract_explicit_dates('2023-12-25T12:00:00Z')
        assert '2023-12-25' in result

    def test_leap_year_feb_29(self):
        result = extract_explicit_dates('2024-02-29T08:00:00Z')
        assert '2024-02-29' in result

    def test_year_2000(self):
        result = extract_explicit_dates('2000-06-01T00:00:00Z')
        assert '2000-06-01' in result

    def test_year_1999(self):
        result = extract_explicit_dates('1999-12-31T23:59:59Z')
        assert '1999-12-31' in result

    def test_year_2030(self):
        result = extract_explicit_dates('2030-01-01T00:00:00Z')
        assert '2030-01-01' in result

    def test_day_01(self):
        result = extract_explicit_dates('2022-05-01T10:00:00Z')
        assert '2022-05-01' in result

    def test_day_15(self):
        result = extract_explicit_dates('2022-05-15T10:00:00Z')
        assert '2022-05-15' in result

    def test_day_28(self):
        result = extract_explicit_dates('2022-05-28T10:00:00Z')
        assert '2022-05-28' in result

    def test_day_31(self):
        result = extract_explicit_dates('2022-05-31T10:00:00Z')
        assert '2022-05-31' in result

    def test_date_not_polluted_by_time(self):
        """Time component must not bleed into the extracted date string."""
        result = extract_explicit_dates('2021-04-10T23:59:59Z')
        assert '2021-04-10' in result
        assert '23:59:59' not in str(result)

    def test_date_not_polluted_by_offset(self):
        result = extract_explicit_dates('2021-04-10T10:00:00+05:30')
        assert '2021-04-10' in result
        assert '+05:30' not in str(result)

    def test_with_z_suffix_date_only_key(self):
        result = extract_explicit_dates('2018-08-08T08:08:08Z')
        keys = list(result.keys())
        assert all('T' not in k for k in keys)

    def test_with_offset_date_only_key(self):
        result = extract_explicit_dates('2018-08-08T08:08:08+02:00')
        keys = list(result.keys())
        assert all('T' not in k for k in keys)

    def test_date_year_correct(self):
        result = extract_explicit_dates('2019-07-16T20:17:40Z')
        assert '2019-07-16' in result

    def test_multiple_month_02_various_years(self):
        for year in [2018, 2019, 2020, 2021, 2022]:
            result = extract_explicit_dates(f'{year}-02-14T12:00:00Z')
            assert f'{year}-02-14' in result
