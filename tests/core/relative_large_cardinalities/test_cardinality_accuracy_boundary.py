#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
from fast_parse_time import parse_time_references, has_temporal_info


# ============================================================================
# Group 1: hours -- gap range 25-168 (above current max of 24)
# ============================================================================


class TestCardinalityAccuracyBoundary:
    """Cardinality values are precisely preserved at boundary points."""

    def test_hours_boundary_24(self):
        """Still works at old max."""
        result = parse_time_references('24 hours ago')
        assert result[0].cardinality == 24

    def test_hours_boundary_25(self):
        """First new value."""
        result = parse_time_references('25 hours ago')
        assert result[0].cardinality == 25

    def test_minutes_boundary_60(self):
        result = parse_time_references('60 minutes ago')
        assert result[0].cardinality == 60

    def test_minutes_boundary_61(self):
        result = parse_time_references('61 minutes ago')
        assert result[0].cardinality == 61

    def test_seconds_boundary_60(self):
        result = parse_time_references('60 seconds ago')
        assert result[0].cardinality == 60

    def test_seconds_boundary_61(self):
        result = parse_time_references('61 seconds ago')
        assert result[0].cardinality == 61

    def test_weeks_boundary_52(self):
        result = parse_time_references('52 weeks ago')
        assert result[0].cardinality == 52

    def test_weeks_boundary_53(self):
        result = parse_time_references('53 weeks ago')
        assert result[0].cardinality == 53

    def test_months_boundary_24(self):
        result = parse_time_references('24 months ago')
        assert result[0].cardinality == 24

    def test_months_boundary_25(self):
        result = parse_time_references('25 months ago')
        assert result[0].cardinality == 25

    def test_days_boundary_365(self):
        result = parse_time_references('365 days ago')
        assert result[0].cardinality == 365

    def test_days_boundary_366(self):
        result = parse_time_references('366 days ago')
        assert result[0].cardinality == 366

    def test_years_boundary_100(self):
        result = parse_time_references('100 years ago')
        assert result[0].cardinality == 100

    def test_years_boundary_101(self):
        result = parse_time_references('101 years ago')
        assert result[0].cardinality == 101

    def test_all_at_max_1000(self):
        """All units reach 1000."""
        for unit in ['hours', 'minutes', 'seconds', 'days', 'weeks', 'months', 'years']:
            result = parse_time_references(f'1000 {unit} ago')
            assert len(result) == 1, f'Failed for 1000 {unit} ago'
            assert result[0].cardinality == 1000, f'Wrong cardinality for 1000 {unit} ago'


# ============================================================================
# Group 14: Tense accuracy for large cardinalities
# ============================================================================
