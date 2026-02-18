#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
from fast_parse_time import parse_time_references, has_temporal_info


# ============================================================================
# Group 1: hours -- gap range 25-168 (above current max of 24)
# ============================================================================


class TestMonthsBackLargeCardinality:
    def test_36_months_back(self):
        result = parse_time_references('36 months back')
        assert len(result) == 1
        assert result[0].cardinality == 36
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_1000_months_back(self):
        result = parse_time_references('1000 months back')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'month'


# ============================================================================
# Group 7: days -- gap range 366-1000 (above current max of 365)
# ============================================================================
