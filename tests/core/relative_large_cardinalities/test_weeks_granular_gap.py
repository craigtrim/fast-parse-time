#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
from fast_parse_time import parse_time_references, has_temporal_info


# ============================================================================
# Group 1: hours -- gap range 25-168 (above current max of 24)
# ============================================================================


class TestWeeksGranularGap:
    """Values from 53-65 work for 'N weeks ago'."""

    def test_53(self):
        assert parse_time_references('53 weeks ago')[0].cardinality == 53

    def test_54(self):
        assert parse_time_references('54 weeks ago')[0].cardinality == 54

    def test_55(self):
        assert parse_time_references('55 weeks ago')[0].cardinality == 55

    def test_60(self):
        assert parse_time_references('60 weeks ago')[0].cardinality == 60

    def test_65(self):
        assert parse_time_references('65 weeks ago')[0].cardinality == 65


# ============================================================================
# Group 22: Cross-unit result isolation -- no spillover
# ============================================================================
