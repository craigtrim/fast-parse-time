#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
from fast_parse_time import parse_time_references, has_temporal_info


# ============================================================================
# Group 1: hours -- gap range 25-168 (above current max of 24)
# ============================================================================


class TestMonthsBeforeNowLargeCardinality:
    def test_36_months_before_now(self):
        result = parse_time_references('36 months before now')
        assert len(result) == 1
        assert result[0].cardinality == 36
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_120_months_before_now(self):
        result = parse_time_references('120 months before now')
        assert len(result) == 1
        assert result[0].cardinality == 120
        assert result[0].frame == 'month'

    def test_1000_months_before_now(self):
        result = parse_time_references('1000 months before now')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'month'
