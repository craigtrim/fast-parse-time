#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
from fast_parse_time import parse_time_references, has_temporal_info


# ============================================================================
# Group 1: hours -- gap range 25-168 (above current max of 24)
# ============================================================================


class TestHasTemporalInfoLargeCardinality:
    """has_temporal_info correctly detects large cardinality expressions."""

    def test_34_hours_ago(self):
        assert has_temporal_info('34 hours ago') is True

    def test_90_minutes_ago(self):
        assert has_temporal_info('90 minutes ago') is True

    def test_36_months_ago(self):
        assert has_temporal_info('36 months ago') is True

    def test_366_days_ago(self):
        assert has_temporal_info('366 days ago') is True

    def test_1000_weeks_ago(self):
        assert has_temporal_info('1000 weeks ago') is True

    def test_500_years_ago(self):
        assert has_temporal_info('500 years ago') is True

    def test_48_hours_from_now(self):
        assert has_temporal_info('48 hours from now') is True

    def test_1000_days_from_now(self):
        assert has_temporal_info('1000 days from now') is True

    def test_no_false_positive_random_number(self):
        """A bare number is not a time reference."""
        assert has_temporal_info('the answer is 42') is False

    def test_no_false_positive_large_number(self):
        assert has_temporal_info('there are 1000 reasons') is False


# ============================================================================
# Group 12: Phrase context -- large cardinalities embedded in prose
# ============================================================================
