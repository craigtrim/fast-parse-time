#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
from fast_parse_time import parse_time_references, has_temporal_info


# ============================================================================
# Group 1: hours -- gap range 25-168 (above current max of 24)
# ============================================================================


class TestPhraseContextLargeCardinality:
    """Large cardinality time references embedded in sentences."""

    def test_48_hours_ago_in_prose(self):
        result = parse_time_references('the outage started 48 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 48
        assert result[0].frame == 'hour'

    def test_90_minutes_ago_in_prose(self):
        result = parse_time_references('she called 90 minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 90
        assert result[0].frame == 'minute'

    def test_36_months_ago_in_prose(self):
        result = parse_time_references('that happened 36 months ago')
        assert len(result) == 1
        assert result[0].cardinality == 36
        assert result[0].frame == 'month'

    def test_500_days_ago_in_prose(self):
        result = parse_time_references('the project started 500 days ago')
        assert len(result) == 1
        assert result[0].cardinality == 500
        assert result[0].frame == 'day'

    def test_1000_hours_from_now_in_prose(self):
        result = parse_time_references('the deadline is 1000 hours from now')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'hour'
        assert result[0].tense == 'future'

    def test_72_hours_before_now_in_prose(self):
        result = parse_time_references('the backup was created 72 hours before now')
        assert len(result) == 1
        assert result[0].cardinality == 72
        assert result[0].frame == 'hour'

    def test_104_weeks_prior_in_prose(self):
        result = parse_time_references('the contract expired 104 weeks prior')
        assert len(result) == 1
        assert result[0].cardinality == 104
        assert result[0].frame == 'week'


# ============================================================================
# Group 13: Cardinality accuracy at boundary values
# ============================================================================
