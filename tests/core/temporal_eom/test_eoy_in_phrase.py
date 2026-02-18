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
# Group 1: Bare 'eod' -- basic attribute checks
# ============================================================================


class TestEoyInPhrase:
    """eoy is extracted correctly when preceded by non-time words."""

    def test_meeting_eoy(self):
        result = parse_time_references('meeting eoy')
        assert len(result) == 1
        assert result[0].frame == 'year'

    def test_call_eoy(self):
        result = parse_time_references('call eoy')
        assert len(result) == 1
        assert result[0].frame == 'year'

    def test_reminder_eoy(self):
        result = parse_time_references('reminder eoy')
        assert len(result) == 1
        assert result[0].frame == 'year'

    def test_deadline_eoy(self):
        result = parse_time_references('deadline eoy')
        assert len(result) == 1
        assert result[0].frame == 'year'

    def test_submit_report_eoy(self):
        result = parse_time_references('submit report eoy')
        assert len(result) == 1
        assert result[0].frame == 'year'

    def test_status_update_eoy(self):
        result = parse_time_references('status update eoy')
        assert len(result) == 1
        assert result[0].frame == 'year'

    def test_project_eoy(self):
        result = parse_time_references('project eoy')
        assert len(result) == 1
        assert result[0].frame == 'year'

    def test_please_do_eoy(self):
        result = parse_time_references('please do eoy')
        assert len(result) == 1
        assert result[0].frame == 'year'


# ============================================================================
# Group 9: Phrase context -- eod/eom/eoy followed by trailing non-time words
# ============================================================================
