#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
from fast_parse_time import parse_time_references, has_temporal_info


# ============================================================================
# Group 1: hours -- gap range 25-168 (above current max of 24)
# ============================================================================


class TestMonthsAgoLargeCardinality:
    """'ago' suffix for months above current max of 24."""

    def test_25_months_ago(self):
        result = parse_time_references('25 months ago')
        assert len(result) == 1
        assert result[0].cardinality == 25
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_36_months_ago(self):
        """3 years expressed in months — very common."""
        result = parse_time_references('36 months ago')
        assert len(result) == 1
        assert result[0].cardinality == 36
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_48_months_ago(self):
        """4 years in months."""
        result = parse_time_references('48 months ago')
        assert len(result) == 1
        assert result[0].cardinality == 48
        assert result[0].frame == 'month'

    def test_60_months_ago(self):
        """5 years in months."""
        result = parse_time_references('60 months ago')
        assert len(result) == 1
        assert result[0].cardinality == 60
        assert result[0].frame == 'month'

    def test_120_months_ago(self):
        """10 years in months."""
        result = parse_time_references('120 months ago')
        assert len(result) == 1
        assert result[0].cardinality == 120
        assert result[0].frame == 'month'

    def test_200_months_ago(self):
        result = parse_time_references('200 months ago')
        assert len(result) == 1
        assert result[0].cardinality == 200
        assert result[0].frame == 'month'

    def test_500_months_ago(self):
        result = parse_time_references('500 months ago')
        assert len(result) == 1
        assert result[0].cardinality == 500
        assert result[0].frame == 'month'

    def test_1000_months_ago(self):
        result = parse_time_references('1000 months ago')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'month'
