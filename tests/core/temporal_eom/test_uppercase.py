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


class TestUppercase:
    """EOD, EOM, EOY (uppercase) should work identically to lowercase."""

    def test_EOD_uppercase(self):
        result = parse_time_references('EOD')
        assert len(result) == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'future'

    def test_EOM_uppercase(self):
        result = parse_time_references('EOM')
        assert len(result) == 1
        assert result[0].frame == 'month'
        assert result[0].tense == 'future'

    def test_EOY_uppercase(self):
        result = parse_time_references('EOY')
        assert len(result) == 1
        assert result[0].frame == 'year'
        assert result[0].tense == 'future'


# ============================================================================
# Group 5: Mixed-case variants
# ============================================================================
