#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
from fast_parse_time import parse_time_references, has_temporal_info


# ============================================================================
# Group 1: hours -- gap range 25-168 (above current max of 24)
# ============================================================================


class TestInNUnitsLargeCardinality:
    """'in N units' future pattern with large cardinalities."""

    def test_in_48_hours(self):
        result = parse_time_references('in 48 hours')
        assert len(result) == 1
        assert result[0].cardinality == 48
        assert result[0].frame == 'hour'
        assert result[0].tense == 'future'

    def test_in_90_minutes(self):
        result = parse_time_references('in 90 minutes')
        assert len(result) == 1
        assert result[0].cardinality == 90
        assert result[0].frame == 'minute'
        assert result[0].tense == 'future'

    def test_in_53_weeks(self):
        result = parse_time_references('in 53 weeks')
        assert len(result) == 1
        assert result[0].cardinality == 53
        assert result[0].frame == 'week'
        assert result[0].tense == 'future'

    def test_in_36_months(self):
        result = parse_time_references('in 36 months')
        assert len(result) == 1
        assert result[0].cardinality == 36
        assert result[0].frame == 'month'
        assert result[0].tense == 'future'

    def test_in_500_days(self):
        result = parse_time_references('in 500 days')
        assert len(result) == 1
        assert result[0].cardinality == 500
        assert result[0].frame == 'day'
        assert result[0].tense == 'future'

    def test_in_1000_hours(self):
        result = parse_time_references('in 1000 hours')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'hour'
        assert result[0].tense == 'future'


# ============================================================================
# Group 11: has_temporal_info for large cardinalities
# ============================================================================
