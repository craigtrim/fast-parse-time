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


class TestParseDatesIntegration:
    """parse_dates picks up the new patterns in combined results."""

    def test_before_now_parse_dates_has_dates(self):
        result = parse_dates('5 minutes before now')
        assert result.has_dates is True

    def test_prior_parse_dates_has_dates(self):
        result = parse_dates('3 days prior')
        assert result.has_dates is True

    def test_back_parse_dates_has_dates(self):
        result = parse_dates('7 hours back')
        assert result.has_dates is True

    def test_before_now_relative_times(self):
        result = parse_dates('5 minutes before now')
        assert len(result.relative_times) == 1
        assert result.relative_times[0].tense == 'past'

    def test_prior_relative_times(self):
        result = parse_dates('3 days prior')
        assert len(result.relative_times) == 1
        assert result.relative_times[0].frame == 'day'

    def test_back_relative_times(self):
        result = parse_dates('7 hours back')
        assert len(result.relative_times) == 1
        assert result.relative_times[0].frame == 'hour'


# ============================================================================
# Group 13: Case insensitivity
# ============================================================================
