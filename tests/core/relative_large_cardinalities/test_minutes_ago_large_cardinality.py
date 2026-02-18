#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
from fast_parse_time import parse_time_references, has_temporal_info


# ============================================================================
# Group 1: hours -- gap range 25-168 (above current max of 24)
# ============================================================================


class TestMinutesAgoLargeCardinality:
    """'ago' suffix for minutes above current max of 60."""

    def test_61_minutes_ago(self):
        result = parse_time_references('61 minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 61
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_90_minutes_ago(self):
        """Very common — 'an hour and a half ago'."""
        result = parse_time_references('90 minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 90
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_120_minutes_ago(self):
        """2 hours expressed in minutes."""
        result = parse_time_references('120 minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 120
        assert result[0].frame == 'minute'

    def test_180_minutes_ago(self):
        result = parse_time_references('180 minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 180
        assert result[0].frame == 'minute'

    def test_240_minutes_ago(self):
        result = parse_time_references('240 minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 240
        assert result[0].frame == 'minute'

    def test_500_minutes_ago(self):
        result = parse_time_references('500 minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 500
        assert result[0].frame == 'minute'

    def test_1000_minutes_ago(self):
        result = parse_time_references('1000 minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'minute'
