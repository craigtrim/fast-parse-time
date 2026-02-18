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


class TestEodInPhrase:
    """eod is extracted correctly when preceded by non-time words."""

    def test_meeting_eod(self):
        result = parse_time_references('meeting eod')
        assert len(result) == 1
        assert result[0].frame == 'day'

    def test_call_eod(self):
        result = parse_time_references('call eod')
        assert len(result) == 1
        assert result[0].frame == 'day'

    def test_reminder_eod(self):
        result = parse_time_references('reminder eod')
        assert len(result) == 1
        assert result[0].frame == 'day'

    def test_deadline_eod(self):
        result = parse_time_references('deadline eod')
        assert len(result) == 1
        assert result[0].frame == 'day'

    def test_submit_report_eod(self):
        result = parse_time_references('submit report eod')
        assert len(result) == 1
        assert result[0].frame == 'day'

    def test_status_update_eod(self):
        result = parse_time_references('status update eod')
        assert len(result) == 1
        assert result[0].frame == 'day'

    def test_project_eod(self):
        result = parse_time_references('project eod')
        assert len(result) == 1
        assert result[0].frame == 'day'

    def test_please_do_eod(self):
        result = parse_time_references('please do eod')
        assert len(result) == 1
        assert result[0].frame == 'day'


# ============================================================================
# Group 7: Phrase context -- leading non-time words + eom
# ============================================================================
