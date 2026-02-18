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


class TestHasTemporalInfo:
    """has_temporal_info returns True for texts with the new patterns."""

    def test_before_now_has_temporal_info(self):
        assert has_temporal_info('5 minutes before now') is True

    def test_prior_has_temporal_info(self):
        assert has_temporal_info('3 days prior') is True

    def test_back_has_temporal_info(self):
        assert has_temporal_info('7 hours back') is True

    def test_before_now_in_sentence(self):
        assert has_temporal_info('data from 5 days before now') is True

    def test_prior_in_sentence(self):
        assert has_temporal_info('submitted 2 months prior') is True

    def test_back_in_sentence(self):
        assert has_temporal_info('created 3 weeks back') is True

    def test_non_temporal_false(self):
        assert has_temporal_info('regular text') is False

    def test_another_non_temporal_false(self):
        assert has_temporal_info('hello world') is False


# ============================================================================
# Group 9: extract_past_references
# ============================================================================
