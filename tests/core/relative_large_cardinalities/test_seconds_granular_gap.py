#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
from fast_parse_time import parse_time_references, has_temporal_info


# ============================================================================
# Group 1: hours -- gap range 25-168 (above current max of 24)
# ============================================================================


class TestSecondsGranularGap:
    """Values from 61-80 work for 'N seconds ago'."""

    def test_61(self):
        assert parse_time_references('61 seconds ago')[0].cardinality == 61

    def test_62(self):
        assert parse_time_references('62 seconds ago')[0].cardinality == 62

    def test_63(self):
        assert parse_time_references('63 seconds ago')[0].cardinality == 63

    def test_70(self):
        assert parse_time_references('70 seconds ago')[0].cardinality == 70

    def test_75(self):
        assert parse_time_references('75 seconds ago')[0].cardinality == 75

    def test_80(self):
        assert parse_time_references('80 seconds ago')[0].cardinality == 80

    def test_90(self):
        assert parse_time_references('90 seconds ago')[0].cardinality == 90

    def test_100(self):
        assert parse_time_references('100 seconds ago')[0].cardinality == 100

    def test_200(self):
        assert parse_time_references('200 seconds ago')[0].cardinality == 200


# ============================================================================
# Group 24: Days -- granular gap coverage (366-380)
# ============================================================================
