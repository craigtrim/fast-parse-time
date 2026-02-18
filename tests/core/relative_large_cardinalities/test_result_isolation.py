#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
from fast_parse_time import parse_time_references, has_temporal_info


# ============================================================================
# Group 1: hours -- gap range 25-168 (above current max of 24)
# ============================================================================


class TestResultIsolation:
    """Only one result returned; no extra matches from numeric tokens."""

    def test_48_hours_ago_only_one_result(self):
        result = parse_time_references('48 hours ago')
        assert len(result) == 1

    def test_90_minutes_ago_only_one_result(self):
        result = parse_time_references('90 minutes ago')
        assert len(result) == 1

    def test_36_months_ago_only_one_result(self):
        result = parse_time_references('36 months ago')
        assert len(result) == 1

    def test_730_days_ago_only_one_result(self):
        result = parse_time_references('730 days ago')
        assert len(result) == 1

    def test_104_weeks_ago_only_one_result(self):
        result = parse_time_references('104 weeks ago')
        assert len(result) == 1

    def test_500_years_ago_only_one_result(self):
        result = parse_time_references('500 years ago')
        assert len(result) == 1

    def test_1000_seconds_ago_only_one_result(self):
        result = parse_time_references('1000 seconds ago')
        assert len(result) == 1


# ============================================================================
# Group 23: Seconds -- granular gap coverage (61-80)
# ============================================================================
