#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from datetime import timedelta

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


# ============================================================================
# Group 1: Bare 'now' -- basic attribute checks
# ============================================================================


class TestNowInPhrase:
    """'now' is extracted when preceded by non-time words."""

    def test_meeting_now(self):
        result = parse_time_references('meeting now')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_do_it_now(self):
        result = parse_time_references('do it now')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_check_now(self):
        result = parse_time_references('check now')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_status_now(self):
        result = parse_time_references('status now')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_call_now(self):
        result = parse_time_references('call now')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_available_now(self):
        result = parse_time_references('available now')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_happening_now(self):
        result = parse_time_references('happening now')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_starting_now(self):
        result = parse_time_references('starting now')
        assert len(result) == 1
        assert result[0].tense == 'present'


# ============================================================================
# Group 5: 'now' in phrase context -- trailing non-time words
# ============================================================================
