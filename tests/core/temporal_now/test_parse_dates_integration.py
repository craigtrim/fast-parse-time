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


class TestParseDatesIntegration:
    """parse_dates picks up now/right now."""

    def test_now_parse_dates_has_dates(self):
        result = parse_dates('now')
        assert result.has_dates is True

    def test_right_now_parse_dates_has_dates(self):
        result = parse_dates('right now')
        assert result.has_dates is True

    def test_now_parse_dates_relative_times(self):
        result = parse_dates('now')
        assert len(result.relative_times) == 1
        assert result.relative_times[0].frame == 'second'

    def test_right_now_parse_dates_relative_times(self):
        result = parse_dates('right now')
        assert len(result.relative_times) == 1
        assert result.relative_times[0].frame == 'second'

    def test_meeting_now_parse_dates(self):
        result = parse_dates('meeting now')
        assert result.has_dates is True
        assert result.relative_times[0].tense == 'present'

    def test_meeting_right_now_parse_dates(self):
        result = parse_dates('meeting right now')
        assert result.has_dates is True
        assert result.relative_times[0].tense == 'present'


# ============================================================================
# Group 13: Disambiguation -- 'now' inside 'X from now' patterns
# ============================================================================
