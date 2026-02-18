#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Direct tests for extract_explicit_dates with all ISO 8601 datetime variants.

Related GitHub Issue:
    #23 - Gap: ISO 8601 datetime strings not extracted
    https://github.com/craigtrim/fast-parse-time/issues/23

Exercises the full API contract: return type, structure, and correctness.
"""

import pytest
from fast_parse_time import extract_explicit_dates


class TestIso8601ExtractExplicitDates:
    """extract_explicit_dates API contract tests for ISO 8601 datetimes."""

    # --- return type ---

    def test_z_returns_dict(self):
        result = extract_explicit_dates('2017-02-03T09:04:08Z')
        assert isinstance(result, dict)

    def test_plus_offset_returns_dict(self):
        result = extract_explicit_dates('2022-04-15T10:30:00+05:30')
        assert isinstance(result, dict)

    def test_minus_offset_returns_dict(self):
        result = extract_explicit_dates('2022-03-15T09:30:00-05:00')
        assert isinstance(result, dict)

    def test_millis_returns_dict(self):
        result = extract_explicit_dates('2017-02-03T09:04:08.001Z')
        assert isinstance(result, dict)

    # --- dict is not None ---

    def test_z_not_none(self):
        result = extract_explicit_dates('2017-02-03T09:04:08Z')
        assert result is not None

    def test_plus_offset_not_none(self):
        result = extract_explicit_dates('2016-02-04T20:16:26+00:00')
        assert result is not None

    # --- key format (YYYY-MM-DD only) ---

    def test_z_key_length(self):
        result = extract_explicit_dates('2017-02-03T09:04:08Z')
        key = list(result.keys())[0]
        assert len(key) == 10  # YYYY-MM-DD

    def test_z_key_format(self):
        result = extract_explicit_dates('2017-02-03T09:04:08Z')
        key = list(result.keys())[0]
        import re
        assert re.match(r'\d{4}-\d{2}-\d{2}', key)

    def test_plus_offset_key_no_T(self):
        result = extract_explicit_dates('2022-04-15T10:30:00+05:30')
        for key in result:
            assert 'T' not in key

    def test_z_key_no_Z(self):
        result = extract_explicit_dates('2017-02-03T09:04:08Z')
        for key in result:
            assert 'Z' not in key

    def test_offset_key_no_plus(self):
        result = extract_explicit_dates('2022-04-15T10:30:00+05:30')
        for key in result:
            assert '+' not in key

    def test_offset_key_no_colon_after_pos8(self):
        """Key should be YYYY-MM-DD only (colons only at pos 4 and 7)."""
        result = extract_explicit_dates('2022-04-15T10:30:00+05:30')
        key = list(result.keys())[0]
        assert len(key) == 10

    # --- value is always FULL_EXPLICIT_DATE ---

    def test_z_value(self):
        result = extract_explicit_dates('2017-02-03T09:04:08Z')
        assert list(result.values())[0] == 'FULL_EXPLICIT_DATE'

    def test_plus_offset_value(self):
        result = extract_explicit_dates('2022-04-15T10:30:00+05:30')
        assert list(result.values())[0] == 'FULL_EXPLICIT_DATE'

    def test_minus_offset_value(self):
        result = extract_explicit_dates('2022-03-15T09:30:00-05:00')
        assert list(result.values())[0] == 'FULL_EXPLICIT_DATE'

    def test_millis_value(self):
        result = extract_explicit_dates('2017-02-03T09:04:08.001Z')
        assert list(result.values())[0] == 'FULL_EXPLICIT_DATE'

    # --- specific issue examples verbatim ---

    def test_issue_example_1(self):
        """Verbatim from issue: 2016-02-04T20:16:26+00:00"""
        result = extract_explicit_dates('2016-02-04T20:16:26+00:00')
        assert result == {'2016-02-04': 'FULL_EXPLICIT_DATE'}

    def test_issue_example_2(self):
        """Verbatim from issue: 2017-02-03T09:04:08Z"""
        result = extract_explicit_dates('2017-02-03T09:04:08Z')
        assert result == {'2017-02-03': 'FULL_EXPLICIT_DATE'}

    def test_issue_example_3(self):
        """Verbatim from issue: 2017-02-03T09:04:08.001Z"""
        result = extract_explicit_dates('2017-02-03T09:04:08.001Z')
        assert result == {'2017-02-03': 'FULL_EXPLICIT_DATE'}

    def test_issue_example_4(self):
        """Verbatim from issue: 2017-02-03T09:04:08,00123Z"""
        result = extract_explicit_dates('2017-02-03T09:04:08,00123Z')
        assert result == {'2017-02-03': 'FULL_EXPLICIT_DATE'}

    # --- empty input ---

    def test_empty_string_returns_empty(self):
        result = extract_explicit_dates('')
        assert result == {} or result is None or len(result) == 0

    def test_no_iso_datetime_no_result(self):
        result = extract_explicit_dates('no date here at all')
        assert not result

    # --- extra variants ---

    def test_t_lowercase_handled(self):
        """Lowercase 't' separator may appear in some generators."""
        result = extract_explicit_dates('2022-06-15t10:30:00z')
        # Should extract 2022-06-15 OR return empty (lowercase not required)
        # Just ensure no exception is raised
        assert result is not None

    def test_various_years(self):
        for year in [2010, 2015, 2020, 2025]:
            result = extract_explicit_dates(f'{year}-06-15T10:00:00Z')
            assert f'{year}-06-15' in result
