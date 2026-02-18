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


class TestHasTemporalInfo:
    """has_temporal_info returns True for texts containing eod/eom/eoy."""

    def test_eod_has_temporal_info(self):
        assert has_temporal_info('eod') is True

    def test_eom_has_temporal_info(self):
        assert has_temporal_info('eom') is True

    def test_eoy_has_temporal_info(self):
        assert has_temporal_info('eoy') is True

    def test_meeting_eod_has_temporal_info(self):
        assert has_temporal_info('meeting eod') is True

    def test_meeting_eom_has_temporal_info(self):
        assert has_temporal_info('meeting eom') is True

    def test_meeting_eoy_has_temporal_info(self):
        assert has_temporal_info('meeting eoy') is True

    def test_non_temporal_text_false(self):
        assert has_temporal_info('regular sentence with no dates') is False

    def test_another_non_temporal_false(self):
        assert has_temporal_info('just a random phrase') is False


# ============================================================================
# Group 11: extract_future_references
# ============================================================================
