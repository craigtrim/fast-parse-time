#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
from fast_parse_time import parse_time_references, has_temporal_info


# ============================================================================
# Group 1: hours -- gap range 25-168 (above current max of 24)
# ============================================================================


class TestMonthsFromNowLargeCardinality:
    def test_36_months_from_now(self):
        result = parse_time_references('36 months from now')
        assert len(result) == 1
        assert result[0].cardinality == 36
        assert result[0].frame == 'month'
        assert result[0].tense == 'future'

    def test_1000_months_from_now(self):
        result = parse_time_references('1000 months from now')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'month'
        assert result[0].tense == 'future'
