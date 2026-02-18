#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
from fast_parse_time import parse_time_references, has_temporal_info


# ============================================================================
# Group 1: hours -- gap range 25-168 (above current max of 24)
# ============================================================================


class TestMinutesGranularGap:
    """Values from 61-75 work for 'N minutes ago'."""

    def test_61(self):
        assert parse_time_references('61 minutes ago')[0].cardinality == 61

    def test_62(self):
        assert parse_time_references('62 minutes ago')[0].cardinality == 62

    def test_63(self):
        assert parse_time_references('63 minutes ago')[0].cardinality == 63

    def test_65(self):
        assert parse_time_references('65 minutes ago')[0].cardinality == 65

    def test_70(self):
        assert parse_time_references('70 minutes ago')[0].cardinality == 70

    def test_75(self):
        assert parse_time_references('75 minutes ago')[0].cardinality == 75

    def test_80(self):
        assert parse_time_references('80 minutes ago')[0].cardinality == 80

    def test_85(self):
        assert parse_time_references('85 minutes ago')[0].cardinality == 85

    def test_90(self):
        assert parse_time_references('90 minutes ago')[0].cardinality == 90

    def test_100(self):
        assert parse_time_references('100 minutes ago')[0].cardinality == 100


# ============================================================================
# Group 20: Months -- granular gap coverage (25-36)
# ============================================================================
