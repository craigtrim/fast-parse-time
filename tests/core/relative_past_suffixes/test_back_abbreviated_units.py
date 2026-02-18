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


class TestBackAbbreviatedUnits:
    """Abbreviated unit forms work with 'back'."""

    def test_5_mins_back(self):
        result = parse_time_references('5 mins back')
        assert len(result) == 1
        assert result[0].frame == 'minute'

    def test_5_hrs_back(self):
        result = parse_time_references('5 hrs back')
        assert len(result) == 1
        assert result[0].frame == 'hour'

    def test_2_wks_back(self):
        result = parse_time_references('2 wks back')
        assert len(result) == 1
        assert result[0].frame == 'week'

    def test_3_mos_back(self):
        result = parse_time_references('3 mos back')
        assert len(result) == 1
        assert result[0].frame == 'month'

    def test_2_yrs_back(self):
        result = parse_time_references('2 yrs back')
        assert len(result) == 1
        assert result[0].frame == 'year'

    def test_10_secs_back(self):
        result = parse_time_references('10 secs back')
        assert len(result) == 1
        assert result[0].frame == 'second'


# ============================================================================
# Group 7: Phrase context (embedded in sentences)
# ============================================================================
