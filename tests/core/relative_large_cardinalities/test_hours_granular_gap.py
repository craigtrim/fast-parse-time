#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
from fast_parse_time import parse_time_references, has_temporal_info


# ============================================================================
# Group 1: hours -- gap range 25-168 (above current max of 24)
# ============================================================================


class TestHoursGranularGap:
    """Every value from 25-40 works for 'N hours ago'."""

    def test_25(self):
        assert parse_time_references('25 hours ago')[0].cardinality == 25

    def test_26(self):
        assert parse_time_references('26 hours ago')[0].cardinality == 26

    def test_27(self):
        assert parse_time_references('27 hours ago')[0].cardinality == 27

    def test_28(self):
        assert parse_time_references('28 hours ago')[0].cardinality == 28

    def test_29(self):
        assert parse_time_references('29 hours ago')[0].cardinality == 29

    def test_30(self):
        assert parse_time_references('30 hours ago')[0].cardinality == 30

    def test_31(self):
        assert parse_time_references('31 hours ago')[0].cardinality == 31

    def test_32(self):
        assert parse_time_references('32 hours ago')[0].cardinality == 32

    def test_33(self):
        assert parse_time_references('33 hours ago')[0].cardinality == 33

    def test_34(self):
        assert parse_time_references('34 hours ago')[0].cardinality == 34

    def test_35(self):
        assert parse_time_references('35 hours ago')[0].cardinality == 35

    def test_36(self):
        assert parse_time_references('36 hours ago')[0].cardinality == 36

    def test_37(self):
        assert parse_time_references('37 hours ago')[0].cardinality == 37

    def test_38(self):
        assert parse_time_references('38 hours ago')[0].cardinality == 38

    def test_39(self):
        assert parse_time_references('39 hours ago')[0].cardinality == 39

    def test_40(self):
        assert parse_time_references('40 hours ago')[0].cardinality == 40


# ============================================================================
# Group 19: Minutes -- granular gap coverage (61-75)
# ============================================================================
