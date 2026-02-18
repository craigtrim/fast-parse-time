#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
from fast_parse_time import parse_time_references, has_temporal_info


# ============================================================================
# Group 1: hours -- gap range 25-168 (above current max of 24)
# ============================================================================


class TestMonthsGranularGap:
    """Values from 25-36 work for 'N months ago'."""

    def test_25(self):
        assert parse_time_references('25 months ago')[0].cardinality == 25

    def test_26(self):
        assert parse_time_references('26 months ago')[0].cardinality == 26

    def test_27(self):
        assert parse_time_references('27 months ago')[0].cardinality == 27

    def test_28(self):
        assert parse_time_references('28 months ago')[0].cardinality == 28

    def test_30(self):
        assert parse_time_references('30 months ago')[0].cardinality == 30

    def test_33(self):
        assert parse_time_references('33 months ago')[0].cardinality == 33

    def test_36(self):
        assert parse_time_references('36 months ago')[0].cardinality == 36


# ============================================================================
# Group 21: Weeks -- granular gap coverage (53-65)
# ============================================================================
