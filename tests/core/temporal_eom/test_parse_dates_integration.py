#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from datetime import timedelta

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


# ============================================================================
# Group 1: Bare 'eod' -- basic attribute checks
# ============================================================================


class TestParseDatesIntegration:
    """parse_dates picks up eod/eom/eoy in combined results."""

    def test_eod_parse_dates_has_dates(self):
        result = parse_dates('eod')
        assert result.has_dates is True

    def test_eom_parse_dates_has_dates(self):
        result = parse_dates('eom')
        assert result.has_dates is True

    def test_eoy_parse_dates_has_dates(self):
        result = parse_dates('eoy')
        assert result.has_dates is True

    def test_eod_parse_dates_relative_times(self):
        result = parse_dates('meeting eod')
        assert len(result.relative_times) == 1
        assert result.relative_times[0].frame == 'day'

    def test_eom_parse_dates_relative_times(self):
        result = parse_dates('meeting eom')
        assert len(result.relative_times) == 1
        assert result.relative_times[0].frame == 'month'

    def test_eoy_parse_dates_relative_times(self):
        result = parse_dates('meeting eoy')
        assert len(result.relative_times) == 1
        assert result.relative_times[0].frame == 'year'

    def test_eod_uppercase_parse_dates(self):
        result = parse_dates('EOD')
        assert result.has_dates is True
        assert result.relative_times[0].frame == 'day'

    def test_eom_uppercase_parse_dates(self):
        result = parse_dates('EOM')
        assert result.has_dates is True
        assert result.relative_times[0].frame == 'month'

    def test_eoy_uppercase_parse_dates(self):
        result = parse_dates('EOY')
        assert result.has_dates is True
        assert result.relative_times[0].frame == 'year'


# ============================================================================
# Group 16: Multiple abbreviations in one sentence
# ============================================================================
