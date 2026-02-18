#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Regression tests: existing date formats still work after adding ISO 8601 support.

Related GitHub Issue:
    #23 - Gap: ISO 8601 datetime strings not extracted
    https://github.com/craigtrim/fast-parse-time/issues/23
"""

import pytest
from fast_parse_time import extract_explicit_dates, has_temporal_info, parse_dates


class TestIso8601Regression:
    """Existing date extraction is unaffected by ISO 8601 changes."""

    # --- plain ISO date (date-only, already worked) ---

    def test_iso_date_only_still_works(self):
        result = extract_explicit_dates('2017-02-03')
        assert '2017-02-03' in result

    def test_iso_date_only_type(self):
        result = extract_explicit_dates('2017-02-03')
        assert result['2017-02-03'] == 'FULL_EXPLICIT_DATE'

    def test_iso_date_only_2024(self):
        result = extract_explicit_dates('2024-04-08')
        assert '2024-04-08' in result

    # --- slash-delimited full dates ---

    def test_slash_mmddyyyy(self):
        result = extract_explicit_dates('04/08/2024')
        assert '04/08/2024' in result

    def test_slash_in_sentence(self):
        result = extract_explicit_dates('Event on 04/08/2024')
        assert '04/08/2024' in result

    # --- written month formats ---

    def test_written_month_march(self):
        result = extract_explicit_dates('March 15, 2024')
        assert result  # date found

    def test_written_month_in_sentence(self):
        result = extract_explicit_dates('Event on March 15, 2024')
        assert result

    # --- relative time expressions still work through has_temporal_info ---

    def test_relative_5_days_ago(self):
        assert has_temporal_info('5 days ago') is True

    def test_relative_last_week(self):
        assert has_temporal_info('last week') is True

    def test_relative_next_month(self):
        assert has_temporal_info('next month') is True

    # --- parse_dates regressions ---

    def test_parse_dates_slash_date(self):
        result = parse_dates('04/08/2024')
        assert result.has_dates is True

    def test_parse_dates_written_month(self):
        result = parse_dates('March 15, 2024')
        assert result.has_dates is True

    def test_parse_dates_relative(self):
        result = parse_dates('5 days ago')
        assert result.has_dates is True

    # --- has_temporal_info regressions ---

    def test_slash_date_has_temporal_info(self):
        assert has_temporal_info('04/08/2024') is True

    def test_iso_date_only_has_temporal_info(self):
        assert has_temporal_info('2024-01-15') is True

    def test_no_date_still_false(self):
        assert has_temporal_info('hello world') is False

    def test_number_only_still_false(self):
        assert has_temporal_info('12345') is False

    # --- ISO 8601 doesn't break plain-date extraction ---

    def test_plain_date_not_confused_with_iso_datetime(self):
        """A plain YYYY-MM-DD without T still resolves as before."""
        result = extract_explicit_dates('2023-06-15')
        assert '2023-06-15' in result
        assert result['2023-06-15'] == 'FULL_EXPLICIT_DATE'
