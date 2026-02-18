#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
from fast_parse_time import parse_time_references, has_temporal_info


# ============================================================================
# Group 1: hours -- gap range 25-168 (above current max of 24)
# ============================================================================


class TestTenseAccuracyLargeCardinality:
    """Tense is correctly past or future for large cardinality expressions."""

    def test_past_tense_ago(self):
        result = parse_time_references('48 hours ago')
        assert result[0].tense == 'past'

    def test_past_tense_before_now(self):
        result = parse_time_references('48 hours before now')
        assert result[0].tense == 'past'

    def test_past_tense_prior(self):
        result = parse_time_references('48 hours prior')
        assert result[0].tense == 'past'

    def test_past_tense_back(self):
        result = parse_time_references('48 hours back')
        assert result[0].tense == 'past'

    def test_future_tense_from_now(self):
        result = parse_time_references('48 hours from now')
        assert result[0].tense == 'future'

    def test_future_tense_in_n_hours(self):
        result = parse_time_references('in 48 hours')
        assert result[0].tense == 'future'

    def test_future_tense_large_months(self):
        result = parse_time_references('36 months from now')
        assert result[0].tense == 'future'

    def test_past_tense_large_months_ago(self):
        result = parse_time_references('36 months ago')
        assert result[0].tense == 'past'


# ============================================================================
# Group 15: Frame accuracy for large cardinalities
# ============================================================================
