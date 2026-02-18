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


class TestBeforeNowAbbreviatedUnits:
    """Abbreviated unit forms work with 'before now'."""

    def test_5_mins_before_now(self):
        result = parse_time_references('5 mins before now')
        assert len(result) == 1
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_1_min_before_now(self):
        """min/hr/sec/wk/mo/yr singular abbrevs only present with cardinality 1."""
        result = parse_time_references('1 min before now')
        assert len(result) == 1
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_5_hrs_before_now(self):
        result = parse_time_references('5 hrs before now')
        assert len(result) == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_1_hr_before_now(self):
        result = parse_time_references('1 hr before now')
        assert len(result) == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_2_wks_before_now(self):
        result = parse_time_references('2 wks before now')
        assert len(result) == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_1_wk_before_now(self):
        result = parse_time_references('1 wk before now')
        assert len(result) == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_3_mos_before_now(self):
        result = parse_time_references('3 mos before now')
        assert len(result) == 1
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_1_mo_before_now(self):
        result = parse_time_references('1 mo before now')
        assert len(result) == 1
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_2_yrs_before_now(self):
        result = parse_time_references('2 yrs before now')
        assert len(result) == 1
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_1_yr_before_now(self):
        result = parse_time_references('1 yr before now')
        assert len(result) == 1
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_10_secs_before_now(self):
        result = parse_time_references('10 secs before now')
        assert len(result) == 1
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_1_sec_before_now(self):
        result = parse_time_references('1 sec before now')
        assert len(result) == 1
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'


# ============================================================================
# Group 3: 'prior' -- core unit coverage
# ============================================================================
