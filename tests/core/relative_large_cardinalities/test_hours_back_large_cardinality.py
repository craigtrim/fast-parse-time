#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
from fast_parse_time import parse_time_references, has_temporal_info


# ============================================================================
# Group 1: hours -- gap range 25-168 (above current max of 24)
# ============================================================================


class TestHoursBackLargeCardinality:
    """'back' suffix for hours above current max of 24."""

    def test_25_hours_back(self):
        result = parse_time_references('25 hours back')
        assert len(result) == 1
        assert result[0].cardinality == 25
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_48_hours_back(self):
        result = parse_time_references('48 hours back')
        assert len(result) == 1
        assert result[0].cardinality == 48
        assert result[0].frame == 'hour'

    def test_1000_hours_back(self):
        result = parse_time_references('1000 hours back')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'hour'


# ============================================================================
# Group 3: minutes -- gap range 61-1440 (above current max of 60)
# ============================================================================
