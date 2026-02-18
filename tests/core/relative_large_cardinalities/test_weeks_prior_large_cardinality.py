#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
from fast_parse_time import parse_time_references, has_temporal_info


# ============================================================================
# Group 1: hours -- gap range 25-168 (above current max of 24)
# ============================================================================


class TestWeeksPriorLargeCardinality:
    def test_53_weeks_prior(self):
        result = parse_time_references('53 weeks prior')
        assert len(result) == 1
        assert result[0].cardinality == 53
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_1000_weeks_prior(self):
        result = parse_time_references('1000 weeks prior')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'week'
