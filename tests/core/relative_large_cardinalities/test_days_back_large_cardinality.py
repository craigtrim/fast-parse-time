#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
from fast_parse_time import parse_time_references, has_temporal_info


# ============================================================================
# Group 1: hours -- gap range 25-168 (above current max of 24)
# ============================================================================


class TestDaysBackLargeCardinality:
    def test_366_days_back(self):
        result = parse_time_references('366 days back')
        assert len(result) == 1
        assert result[0].cardinality == 366
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_1000_days_back(self):
        result = parse_time_references('1000 days back')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'day'


# ============================================================================
# Group 8: years -- gap range 101-1000 (above current max of 100)
# ============================================================================
