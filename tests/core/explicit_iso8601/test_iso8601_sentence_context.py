#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Tests for ISO 8601 datetime strings embedded in sentence context.

Related GitHub Issue:
    #23 - Gap: ISO 8601 datetime strings not extracted
    https://github.com/craigtrim/fast-parse-time/issues/23

ISO datetimes appear in logs, API responses, and prose.
"""

import pytest
from fast_parse_time import extract_explicit_dates


class TestIso8601SentenceContext:
    """ISO 8601 datetimes are extracted correctly when surrounded by text."""

    # --- log-line patterns ---

    def test_log_timestamp_prefix(self):
        result = extract_explicit_dates('INFO 2017-02-03T09:04:08Z service started')
        assert '2017-02-03' in result

    def test_log_timestamp_inline(self):
        result = extract_explicit_dates('Event occurred at 2021-11-15T14:30:00Z in datacenter')
        assert '2021-11-15' in result

    def test_log_error_timestamp(self):
        result = extract_explicit_dates('ERROR: connection failed at 2022-06-10T08:00:00Z')
        assert '2022-06-10' in result

    def test_log_created_at(self):
        result = extract_explicit_dates('created_at: 2023-01-20T10:05:30+00:00')
        assert '2023-01-20' in result

    def test_log_updated_at(self):
        result = extract_explicit_dates('updated_at: 2023-03-15T16:45:00-05:00')
        assert '2023-03-15' in result

    # --- API response prose ---

    def test_api_response_context(self):
        result = extract_explicit_dates('The resource was created on 2022-08-01T00:00:00Z.')
        assert '2022-08-01' in result

    def test_api_expiry_context(self):
        result = extract_explicit_dates('Token expires at 2025-01-01T00:00:00Z')
        assert '2025-01-01' in result

    def test_api_last_modified(self):
        result = extract_explicit_dates('last modified: 2020-09-09T09:09:09Z')
        assert '2020-09-09' in result

    def test_api_timestamp_field(self):
        result = extract_explicit_dates('timestamp=2019-05-20T12:00:00+01:00 status=ok')
        assert '2019-05-20' in result

    # --- sentence-embedded ---

    def test_prose_recorded_on(self):
        result = extract_explicit_dates('The transaction was recorded on 2021-04-15T10:30:00Z.')
        assert '2021-04-15' in result

    def test_prose_deployment_date(self):
        result = extract_explicit_dates('Deployment completed at 2023-11-01T03:00:00+00:00.')
        assert '2023-11-01' in result

    def test_prose_backup_timestamp(self):
        result = extract_explicit_dates('Backup taken at 2022-02-22T22:22:22Z successfully.')
        assert '2022-02-22' in result

    def test_prose_leading_text(self):
        result = extract_explicit_dates('Please note that 2020-06-01T00:00:00Z is the cutoff.')
        assert '2020-06-01' in result

    def test_prose_trailing_text(self):
        result = extract_explicit_dates('The deadline is 2024-12-31T23:59:59Z, do not miss it.')
        assert '2024-12-31' in result

    def test_prose_middle_of_sentence(self):
        result = extract_explicit_dates('Meetings from 2021-01-01T08:00:00Z to end of quarter')
        assert '2021-01-01' in result

    # --- result correctness in context ---

    def test_sentence_only_date_extracted(self):
        result = extract_explicit_dates('Alert fired at 2023-07-04T15:00:00Z in production')
        assert '2023-07-04' in result

    def test_sentence_result_not_empty(self):
        result = extract_explicit_dates('Event at 2021-06-15T09:00:00Z')
        assert result

    def test_sentence_single_entry(self):
        result = extract_explicit_dates('Logged at 2021-06-15T09:00:00Z')
        assert len(result) == 1

    def test_sentence_with_millis_z(self):
        result = extract_explicit_dates('Recorded at 2017-02-03T09:04:08.001Z in system')
        assert '2017-02-03' in result

    def test_sentence_with_plus_offset(self):
        result = extract_explicit_dates('Scheduled for 2022-04-15T10:30:00+05:30 IST')
        assert '2022-04-15' in result

    def test_sentence_with_minus_offset(self):
        result = extract_explicit_dates('Archived at 2022-03-15T09:30:00-05:00 EST')
        assert '2022-03-15' in result

    def test_sentence_comma_millis_in_context(self):
        result = extract_explicit_dates('Event at 2017-02-03T09:04:08,00123Z logged')
        assert '2017-02-03' in result

    def test_sentence_colon_separator(self):
        result = extract_explicit_dates('timestamp: 2021-09-09T09:09:09Z')
        assert '2021-09-09' in result

    def test_sentence_no_extra_keys(self):
        result = extract_explicit_dates('Logged at 2021-06-15T09:00:00Z')
        assert len(result) == 1

    def test_json_like_context(self):
        result = extract_explicit_dates('"created_at": "2023-03-01T12:00:00Z"')
        assert '2023-03-01' in result

    def test_csv_like_context(self):
        result = extract_explicit_dates('row,2022-10-10T10:10:10Z,value')
        assert '2022-10-10' in result
