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


class TestEomInPhrase:
    """eom is extracted correctly when preceded by non-time words."""

    def test_meeting_eom(self):
        result = parse_time_references('meeting eom')
        assert len(result) == 1
        assert result[0].frame == 'month'

    def test_call_eom(self):
        result = parse_time_references('call eom')
        assert len(result) == 1
        assert result[0].frame == 'month'

    def test_reminder_eom(self):
        result = parse_time_references('reminder eom')
        assert len(result) == 1
        assert result[0].frame == 'month'

    def test_deadline_eom(self):
        result = parse_time_references('deadline eom')
        assert len(result) == 1
        assert result[0].frame == 'month'

    def test_submit_report_eom(self):
        result = parse_time_references('submit report eom')
        assert len(result) == 1
        assert result[0].frame == 'month'

    def test_status_update_eom(self):
        result = parse_time_references('status update eom')
        assert len(result) == 1
        assert result[0].frame == 'month'

    def test_project_eom(self):
        result = parse_time_references('project eom')
        assert len(result) == 1
        assert result[0].frame == 'month'

    def test_please_do_eom(self):
        result = parse_time_references('please do eom')
        assert len(result) == 1
        assert result[0].frame == 'month'


# ============================================================================
# Group 8: Phrase context -- leading non-time words + eoy
# ============================================================================
