#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
from fast_parse_time import parse_time_references, has_temporal_info


# ============================================================================
# Group 1: hours -- gap range 25-168 (above current max of 24)
# ============================================================================


class TestHoursPriorLargeCardinality:
    """'prior' suffix for hours above current max of 24."""

    def test_25_hours_prior(self):
        result = parse_time_references('25 hours prior')
        assert len(result) == 1
        assert result[0].cardinality == 25
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_48_hours_prior(self):
        result = parse_time_references('48 hours prior')
        assert len(result) == 1
        assert result[0].cardinality == 48
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_1000_hours_prior(self):
        result = parse_time_references('1000 hours prior')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'hour'
