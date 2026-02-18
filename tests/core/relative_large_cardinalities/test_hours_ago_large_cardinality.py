#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
from fast_parse_time import parse_time_references, has_temporal_info


# ============================================================================
# Group 1: hours -- gap range 25-168 (above current max of 24)
# ============================================================================


class TestHoursAgoLargeCardinality:
    """'ago' suffix for hours above current max of 24."""

    def test_25_hours_ago(self):
        result = parse_time_references('25 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 25
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_34_hours_ago(self):
        """Explicit parsedatetime regression case."""
        result = parse_time_references('34 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 34
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_48_hours_ago(self):
        """2 days expressed in hours — very common."""
        result = parse_time_references('48 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 48
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_72_hours_ago(self):
        """3 days expressed in hours — very common."""
        result = parse_time_references('72 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 72
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_96_hours_ago(self):
        result = parse_time_references('96 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 96
        assert result[0].frame == 'hour'

    def test_100_hours_ago(self):
        result = parse_time_references('100 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 100
        assert result[0].frame == 'hour'

    def test_120_hours_ago(self):
        result = parse_time_references('120 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 120
        assert result[0].frame == 'hour'

    def test_168_hours_ago(self):
        """1 week expressed in hours."""
        result = parse_time_references('168 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 168
        assert result[0].frame == 'hour'

    def test_200_hours_ago(self):
        result = parse_time_references('200 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 200
        assert result[0].frame == 'hour'

    def test_500_hours_ago(self):
        result = parse_time_references('500 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 500
        assert result[0].frame == 'hour'

    def test_720_hours_ago(self):
        """1 month expressed in hours."""
        result = parse_time_references('720 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 720
        assert result[0].frame == 'hour'

    def test_1000_hours_ago(self):
        result = parse_time_references('1000 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'hour'


# ============================================================================
# Group 2: hours -- before now, prior, back (large cardinality)
# ============================================================================
