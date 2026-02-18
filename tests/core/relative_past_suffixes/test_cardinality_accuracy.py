#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest

from fast_parse_time import (
    RelativeTime,
    extract_future_references,
    extract_past_references,
    extract_relative_times,
    has_temporal_info,
    parse_dates,
    parse_time_references,
    resolve_to_timedelta,
)
from datetime import timedelta


# ============================================================================
# Group 1: 'before now' -- core unit coverage
# ============================================================================


class TestCardinalityAccuracy:
    """Cardinality values are accurately preserved for all three suffixes."""

    def test_before_now_cardinality_1(self):
        result = parse_time_references('1 day before now')
        assert result[0].cardinality == 1

    def test_before_now_cardinality_10(self):
        result = parse_time_references('10 days before now')
        assert result[0].cardinality == 10

    def test_prior_cardinality_1(self):
        result = parse_time_references('1 week prior')
        assert result[0].cardinality == 1

    def test_prior_cardinality_12(self):
        result = parse_time_references('12 months prior')
        assert result[0].cardinality == 12

    def test_back_cardinality_1(self):
        result = parse_time_references('1 hour back')
        assert result[0].cardinality == 1

    def test_back_cardinality_24(self):
        result = parse_time_references('24 hours back')
        assert result[0].cardinality == 24
