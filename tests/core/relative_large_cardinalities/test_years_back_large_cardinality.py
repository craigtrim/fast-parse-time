#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
from fast_parse_time import parse_time_references, has_temporal_info


# ============================================================================
# Group 1: hours -- gap range 25-168 (above current max of 24)
# ============================================================================


class TestYearsBackLargeCardinality:
    def test_101_years_back(self):
        result = parse_time_references('101 years back')
        assert len(result) == 1
        assert result[0].cardinality == 101
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_1000_years_back(self):
        result = parse_time_references('1000 years back')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'year'


# ============================================================================
# Group 9: Future tense -- from now (large cardinalities)
# ============================================================================
