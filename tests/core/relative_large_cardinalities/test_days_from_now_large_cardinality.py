#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
from fast_parse_time import parse_time_references, has_temporal_info


# ============================================================================
# Group 1: hours -- gap range 25-168 (above current max of 24)
# ============================================================================


class TestDaysFromNowLargeCardinality:
    def test_366_days_from_now(self):
        result = parse_time_references('366 days from now')
        assert len(result) == 1
        assert result[0].cardinality == 366
        assert result[0].frame == 'day'
        assert result[0].tense == 'future'

    def test_1000_days_from_now(self):
        result = parse_time_references('1000 days from now')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'day'
        assert result[0].tense == 'future'


# ============================================================================
# Group 10: Future tense -- 'in N units' (large cardinalities)
# ============================================================================
