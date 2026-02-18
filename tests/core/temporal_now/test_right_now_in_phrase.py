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


class TestRightNowInPhrase:
    """'right now' is extracted when preceded by non-time words."""

    def test_meeting_right_now(self):
        result = parse_time_references('meeting right now')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_do_it_right_now(self):
        result = parse_time_references('do it right now')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_check_right_now(self):
        result = parse_time_references('check right now')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_status_right_now(self):
        result = parse_time_references('status right now')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_call_right_now(self):
        result = parse_time_references('call right now')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_available_right_now(self):
        result = parse_time_references('available right now')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_happening_right_now(self):
        result = parse_time_references('happening right now')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_starting_right_now(self):
        result = parse_time_references('starting right now')
        assert len(result) == 1
        assert result[0].tense == 'present'


# ============================================================================
# Group 7: 'right now' in phrase context -- trailing non-time words
# ============================================================================
