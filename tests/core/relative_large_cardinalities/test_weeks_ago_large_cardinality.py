#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
from fast_parse_time import parse_time_references, has_temporal_info


# ============================================================================
# Group 1: hours -- gap range 25-168 (above current max of 24)
# ============================================================================


class TestWeeksAgoLargeCardinality:
    """'ago' suffix for weeks above current max of 52."""

    def test_53_weeks_ago(self):
        result = parse_time_references('53 weeks ago')
        assert len(result) == 1
        assert result[0].cardinality == 53
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_60_weeks_ago(self):
        result = parse_time_references('60 weeks ago')
        assert len(result) == 1
        assert result[0].cardinality == 60
        assert result[0].frame == 'week'

    def test_104_weeks_ago(self):
        """2 years expressed in weeks."""
        result = parse_time_references('104 weeks ago')
        assert len(result) == 1
        assert result[0].cardinality == 104
        assert result[0].frame == 'week'

    def test_200_weeks_ago(self):
        result = parse_time_references('200 weeks ago')
        assert len(result) == 1
        assert result[0].cardinality == 200
        assert result[0].frame == 'week'

    def test_500_weeks_ago(self):
        result = parse_time_references('500 weeks ago')
        assert len(result) == 1
        assert result[0].cardinality == 500
        assert result[0].frame == 'week'

    def test_1000_weeks_ago(self):
        result = parse_time_references('1000 weeks ago')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'week'
