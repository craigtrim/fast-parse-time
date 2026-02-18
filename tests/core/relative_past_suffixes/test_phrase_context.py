#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest

from fast_parse_time import (
    RelativeTime,
    extract_future_references,
    extract_past_references,
    extract_relative_times,
    has_temporal_info,
    parse_dates,
    parse_time_references,
    resolve_to_timedelta,
)
from datetime import timedelta


# ============================================================================
# Group 1: 'before now' -- core unit coverage
# ============================================================================


class TestPhraseContext:
    """Expressions are extracted correctly when embedded in sentences."""

    def test_sent_from_5_minutes_before_now(self):
        result = parse_time_references('data from 5 minutes before now')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'minute'

    def test_sent_records_3_days_before_now(self):
        result = parse_time_references('records created 3 days before now')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'day'

    def test_sent_meeting_2_weeks_prior(self):
        result = parse_time_references('meeting scheduled 2 weeks prior')
        assert len(result) == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_sent_report_submitted_6_months_prior(self):
        result = parse_time_references('report submitted 6 months prior')
        assert len(result) == 1
        assert result[0].cardinality == 6
        assert result[0].frame == 'month'

    def test_sent_sent_10_minutes_back(self):
        result = parse_time_references('message sent 10 minutes back')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'minute'

    def test_sent_created_5_days_back(self):
        result = parse_time_references('file created 5 days back')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'day'


# ============================================================================
# Group 8: has_temporal_info
# ============================================================================
