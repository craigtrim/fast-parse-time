#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
from fast_parse_time import parse_time_references, has_temporal_info


# ============================================================================
# Group 1: hours -- gap range 25-168 (above current max of 24)
# ============================================================================


class TestYearsAgoLargeCardinality:
    """'ago' suffix for years above current max of 100."""

    def test_101_years_ago(self):
        result = parse_time_references('101 years ago')
        assert len(result) == 1
        assert result[0].cardinality == 101
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_150_years_ago(self):
        result = parse_time_references('150 years ago')
        assert len(result) == 1
        assert result[0].cardinality == 150
        assert result[0].frame == 'year'

    def test_200_years_ago(self):
        result = parse_time_references('200 years ago')
        assert len(result) == 1
        assert result[0].cardinality == 200
        assert result[0].frame == 'year'

    def test_500_years_ago(self):
        result = parse_time_references('500 years ago')
        assert len(result) == 1
        assert result[0].cardinality == 500
        assert result[0].frame == 'year'

    def test_1000_years_ago(self):
        result = parse_time_references('1000 years ago')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'year'
