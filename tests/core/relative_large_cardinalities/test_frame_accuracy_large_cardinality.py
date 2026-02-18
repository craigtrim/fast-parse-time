#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
from fast_parse_time import parse_time_references, has_temporal_info


# ============================================================================
# Group 1: hours -- gap range 25-168 (above current max of 24)
# ============================================================================


class TestFrameAccuracyLargeCardinality:
    """Frame (unit) is correctly identified for large cardinality expressions."""

    def test_frame_hours_large(self):
        result = parse_time_references('500 hours ago')
        assert result[0].frame == 'hour'

    def test_frame_minutes_large(self):
        result = parse_time_references('500 minutes ago')
        assert result[0].frame == 'minute'

    def test_frame_seconds_large(self):
        result = parse_time_references('500 seconds ago')
        assert result[0].frame == 'second'

    def test_frame_days_large(self):
        result = parse_time_references('500 days ago')
        assert result[0].frame == 'day'

    def test_frame_weeks_large(self):
        result = parse_time_references('500 weeks ago')
        assert result[0].frame == 'week'

    def test_frame_months_large(self):
        result = parse_time_references('500 months ago')
        assert result[0].frame == 'month'

    def test_frame_years_large(self):
        result = parse_time_references('500 years ago')
        assert result[0].frame == 'year'


# ============================================================================
# Group 16: Result count -- exactly one result per expression
# ============================================================================
