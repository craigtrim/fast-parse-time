#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
from fast_parse_time import parse_time_references, has_temporal_info


# ============================================================================
# Group 1: hours -- gap range 25-168 (above current max of 24)
# ============================================================================


class TestResultCountLargeCardinality:
    """Exactly one result is returned for each large cardinality expression."""

    def test_single_result_48_hours_ago(self):
        assert len(parse_time_references('48 hours ago')) == 1

    def test_single_result_90_minutes_ago(self):
        assert len(parse_time_references('90 minutes ago')) == 1

    def test_single_result_36_months_ago(self):
        assert len(parse_time_references('36 months ago')) == 1

    def test_single_result_1000_days_ago(self):
        assert len(parse_time_references('1000 days ago')) == 1

    def test_single_result_500_years_ago(self):
        assert len(parse_time_references('500 years ago')) == 1

    def test_single_result_104_weeks_before_now(self):
        assert len(parse_time_references('104 weeks before now')) == 1

    def test_single_result_200_hours_prior(self):
        assert len(parse_time_references('200 hours prior')) == 1

    def test_single_result_1000_months_back(self):
        assert len(parse_time_references('1000 months back')) == 1


# ============================================================================
# Group 17: Regressions -- previously passing tests still work
# ============================================================================
