#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
from fast_parse_time import parse_time_references, has_temporal_info


# ============================================================================
# Group 1: hours -- gap range 25-168 (above current max of 24)
# ============================================================================


class TestSecondsAgoLargeCardinality:
    """'ago' suffix for seconds above current max of 60."""

    def test_61_seconds_ago(self):
        result = parse_time_references('61 seconds ago')
        assert len(result) == 1
        assert result[0].cardinality == 61
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_90_seconds_ago(self):
        result = parse_time_references('90 seconds ago')
        assert len(result) == 1
        assert result[0].cardinality == 90
        assert result[0].frame == 'second'

    def test_120_seconds_ago(self):
        result = parse_time_references('120 seconds ago')
        assert len(result) == 1
        assert result[0].cardinality == 120
        assert result[0].frame == 'second'

    def test_500_seconds_ago(self):
        result = parse_time_references('500 seconds ago')
        assert len(result) == 1
        assert result[0].cardinality == 500
        assert result[0].frame == 'second'

    def test_1000_seconds_ago(self):
        result = parse_time_references('1000 seconds ago')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'second'
