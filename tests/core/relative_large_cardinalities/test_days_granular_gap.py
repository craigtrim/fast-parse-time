#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
from fast_parse_time import parse_time_references, has_temporal_info


# ============================================================================
# Group 1: hours -- gap range 25-168 (above current max of 24)
# ============================================================================


class TestDaysGranularGap:
    """Values from 366-380 work for 'N days ago'."""

    def test_366(self):
        assert parse_time_references('366 days ago')[0].cardinality == 366

    def test_367(self):
        assert parse_time_references('367 days ago')[0].cardinality == 367

    def test_370(self):
        assert parse_time_references('370 days ago')[0].cardinality == 370

    def test_400(self):
        assert parse_time_references('400 days ago')[0].cardinality == 400

    def test_500(self):
        assert parse_time_references('500 days ago')[0].cardinality == 500

    def test_600(self):
        assert parse_time_references('600 days ago')[0].cardinality == 600

    def test_730(self):
        assert parse_time_references('730 days ago')[0].cardinality == 730

    def test_1000(self):
        assert parse_time_references('1000 days ago')[0].cardinality == 1000
