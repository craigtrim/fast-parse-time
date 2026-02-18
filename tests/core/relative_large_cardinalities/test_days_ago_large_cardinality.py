#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
from fast_parse_time import parse_time_references, has_temporal_info


# ============================================================================
# Group 1: hours -- gap range 25-168 (above current max of 24)
# ============================================================================


class TestDaysAgoLargeCardinality:
    """'ago' suffix for days above current max of 365."""

    def test_366_days_ago(self):
        result = parse_time_references('366 days ago')
        assert len(result) == 1
        assert result[0].cardinality == 366
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_400_days_ago(self):
        result = parse_time_references('400 days ago')
        assert len(result) == 1
        assert result[0].cardinality == 400
        assert result[0].frame == 'day'

    def test_500_days_ago(self):
        result = parse_time_references('500 days ago')
        assert len(result) == 1
        assert result[0].cardinality == 500
        assert result[0].frame == 'day'

    def test_730_days_ago(self):
        """2 years in days."""
        result = parse_time_references('730 days ago')
        assert len(result) == 1
        assert result[0].cardinality == 730
        assert result[0].frame == 'day'

    def test_1000_days_ago(self):
        result = parse_time_references('1000 days ago')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'day'
