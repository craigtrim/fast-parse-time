#!/usr/bin/env python
# -*- coding: UTF-8 -*-


"""
Test suite for short unit abbreviations in relative time parsing.

Related GitHub Issue:
    #56 - Support short unit abbreviations (hr, hrs, min, mins, sec) in relative time parsing
    https://github.com/craigtrim/fast-parse-time/issues/56

Tests cover:
- Short unit forms: hr, hrs → hour; min, mins → minute; sec, secs → second
- With and without 'ago': implicit past tense support
- Numeric cardinalities (1-60, boundary values)
- Written-number cardinalities
- Hedges (about, roughly)
- Sentence embedding contexts
- Mixed case variations
- Negative cases (no match scenarios)
"""


import pytest

from fast_parse_time import parse_time_references


# =============================================================================
# Hours: hr/hrs abbreviations with numeric cardinalities
# =============================================================================

class TestHoursHrNumeric:
    """Test 'hr' abbreviation with numeric cardinalities."""

    def test_1_hr_ago(self):
        result = parse_time_references('1 hr ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_1_hr(self):
        """Implicit past tense: '1 hr' → past."""
        result = parse_time_references('1 hr')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_2_hr_ago(self):
        result = parse_time_references('2 hr ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_2_hr(self):
        result = parse_time_references('2 hr')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_5_hr_ago(self):
        result = parse_time_references('5 hr ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_5_hr(self):
        result = parse_time_references('5 hr')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_10_hr_ago(self):
        result = parse_time_references('10 hr ago')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_10_hr(self):
        result = parse_time_references('10 hr')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_15_hr_ago(self):
        result = parse_time_references('15 hr ago')
        assert len(result) == 1
        assert result[0].cardinality == 15
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_15_hr(self):
        result = parse_time_references('15 hr')
        assert len(result) == 1
        assert result[0].cardinality == 15
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_24_hr_ago(self):
        result = parse_time_references('24 hr ago')
        assert len(result) == 1
        assert result[0].cardinality == 24
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_24_hr(self):
        result = parse_time_references('24 hr')
        assert len(result) == 1
        assert result[0].cardinality == 24
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_48_hr_ago(self):
        result = parse_time_references('48 hr ago')
        assert len(result) == 1
        assert result[0].cardinality == 48
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_48_hr(self):
        result = parse_time_references('48 hr')
        assert len(result) == 1
        assert result[0].cardinality == 48
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'


class TestHoursHrsNumeric:
    """Test 'hrs' abbreviation with numeric cardinalities."""

    def test_1_hrs_ago(self):
        result = parse_time_references('1 hrs ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_1_hrs(self):
        result = parse_time_references('1 hrs')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_2_hrs_ago(self):
        result = parse_time_references('2 hrs ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_2_hrs(self):
        result = parse_time_references('2 hrs')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_5_hrs_ago(self):
        result = parse_time_references('5 hrs ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_5_hrs(self):
        result = parse_time_references('5 hrs')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_10_hrs_ago(self):
        result = parse_time_references('10 hrs ago')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_10_hrs(self):
        result = parse_time_references('10 hrs')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_15_hrs_ago(self):
        result = parse_time_references('15 hrs ago')
        assert len(result) == 1
        assert result[0].cardinality == 15
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_15_hrs(self):
        result = parse_time_references('15 hrs')
        assert len(result) == 1
        assert result[0].cardinality == 15
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_24_hrs_ago(self):
        result = parse_time_references('24 hrs ago')
        assert len(result) == 1
        assert result[0].cardinality == 24
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_24_hrs(self):
        result = parse_time_references('24 hrs')
        assert len(result) == 1
        assert result[0].cardinality == 24
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_48_hrs_ago(self):
        result = parse_time_references('48 hrs ago')
        assert len(result) == 1
        assert result[0].cardinality == 48
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_48_hrs(self):
        result = parse_time_references('48 hrs')
        assert len(result) == 1
        assert result[0].cardinality == 48
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'


# =============================================================================
# Minutes: min/mins abbreviations with numeric cardinalities
# =============================================================================

class TestMinutesMinNumeric:
    """Test 'min' abbreviation with numeric cardinalities."""

    def test_1_min_ago(self):
        result = parse_time_references('1 min ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_1_min(self):
        result = parse_time_references('1 min')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_2_min_ago(self):
        result = parse_time_references('2 min ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_2_min(self):
        result = parse_time_references('2 min')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_5_min_ago(self):
        result = parse_time_references('5 min ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_5_min(self):
        result = parse_time_references('5 min')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_10_min_ago(self):
        result = parse_time_references('10 min ago')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_10_min(self):
        result = parse_time_references('10 min')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_15_min_ago(self):
        result = parse_time_references('15 min ago')
        assert len(result) == 1
        assert result[0].cardinality == 15
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_15_min(self):
        result = parse_time_references('15 min')
        assert len(result) == 1
        assert result[0].cardinality == 15
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_30_min_ago(self):
        result = parse_time_references('30 min ago')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_30_min(self):
        result = parse_time_references('30 min')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_45_min_ago(self):
        result = parse_time_references('45 min ago')
        assert len(result) == 1
        assert result[0].cardinality == 45
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_45_min(self):
        result = parse_time_references('45 min')
        assert len(result) == 1
        assert result[0].cardinality == 45
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_60_min_ago(self):
        result = parse_time_references('60 min ago')
        assert len(result) == 1
        assert result[0].cardinality == 60
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_60_min(self):
        result = parse_time_references('60 min')
        assert len(result) == 1
        assert result[0].cardinality == 60
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'


class TestMinutesMinsNumeric:
    """Test 'mins' abbreviation with numeric cardinalities."""

    def test_1_mins_ago(self):
        result = parse_time_references('1 mins ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_1_mins(self):
        result = parse_time_references('1 mins')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_2_mins_ago(self):
        result = parse_time_references('2 mins ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_2_mins(self):
        result = parse_time_references('2 mins')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_5_mins_ago(self):
        result = parse_time_references('5 mins ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_5_mins(self):
        result = parse_time_references('5 mins')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_10_mins_ago(self):
        result = parse_time_references('10 mins ago')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_10_mins(self):
        result = parse_time_references('10 mins')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_15_mins_ago(self):
        result = parse_time_references('15 mins ago')
        assert len(result) == 1
        assert result[0].cardinality == 15
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_15_mins(self):
        result = parse_time_references('15 mins')
        assert len(result) == 1
        assert result[0].cardinality == 15
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_30_mins_ago(self):
        result = parse_time_references('30 mins ago')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_30_mins(self):
        result = parse_time_references('30 mins')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_45_mins_ago(self):
        result = parse_time_references('45 mins ago')
        assert len(result) == 1
        assert result[0].cardinality == 45
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_45_mins(self):
        result = parse_time_references('45 mins')
        assert len(result) == 1
        assert result[0].cardinality == 45
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_60_mins_ago(self):
        result = parse_time_references('60 mins ago')
        assert len(result) == 1
        assert result[0].cardinality == 60
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_60_mins(self):
        result = parse_time_references('60 mins')
        assert len(result) == 1
        assert result[0].cardinality == 60
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'


# =============================================================================
# Seconds: sec/secs abbreviations with numeric cardinalities
# =============================================================================

class TestSecondsSecNumeric:
    """Test 'sec' abbreviation with numeric cardinalities."""

    def test_1_sec_ago(self):
        result = parse_time_references('1 sec ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_1_sec(self):
        result = parse_time_references('1 sec')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_3_sec_ago(self):
        result = parse_time_references('3 sec ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_3_sec(self):
        result = parse_time_references('3 sec')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_5_sec_ago(self):
        result = parse_time_references('5 sec ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_5_sec(self):
        result = parse_time_references('5 sec')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_10_sec_ago(self):
        result = parse_time_references('10 sec ago')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_10_sec(self):
        result = parse_time_references('10 sec')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_15_sec_ago(self):
        result = parse_time_references('15 sec ago')
        assert len(result) == 1
        assert result[0].cardinality == 15
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_15_sec(self):
        result = parse_time_references('15 sec')
        assert len(result) == 1
        assert result[0].cardinality == 15
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_30_sec_ago(self):
        result = parse_time_references('30 sec ago')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_30_sec(self):
        result = parse_time_references('30 sec')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_45_sec_ago(self):
        result = parse_time_references('45 sec ago')
        assert len(result) == 1
        assert result[0].cardinality == 45
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_45_sec(self):
        result = parse_time_references('45 sec')
        assert len(result) == 1
        assert result[0].cardinality == 45
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_60_sec_ago(self):
        result = parse_time_references('60 sec ago')
        assert len(result) == 1
        assert result[0].cardinality == 60
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_60_sec(self):
        result = parse_time_references('60 sec')
        assert len(result) == 1
        assert result[0].cardinality == 60
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'


class TestSecondsSecsNumeric:
    """Test 'secs' abbreviation with numeric cardinalities."""

    def test_1_secs_ago(self):
        result = parse_time_references('1 secs ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_1_secs(self):
        result = parse_time_references('1 secs')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_3_secs_ago(self):
        result = parse_time_references('3 secs ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_3_secs(self):
        result = parse_time_references('3 secs')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_5_secs_ago(self):
        result = parse_time_references('5 secs ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_5_secs(self):
        result = parse_time_references('5 secs')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_10_secs_ago(self):
        result = parse_time_references('10 secs ago')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_10_secs(self):
        result = parse_time_references('10 secs')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_15_secs_ago(self):
        result = parse_time_references('15 secs ago')
        assert len(result) == 1
        assert result[0].cardinality == 15
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_15_secs(self):
        result = parse_time_references('15 secs')
        assert len(result) == 1
        assert result[0].cardinality == 15
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_30_secs_ago(self):
        result = parse_time_references('30 secs ago')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_30_secs(self):
        result = parse_time_references('30 secs')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_45_secs_ago(self):
        result = parse_time_references('45 secs ago')
        assert len(result) == 1
        assert result[0].cardinality == 45
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_45_secs(self):
        result = parse_time_references('45 secs')
        assert len(result) == 1
        assert result[0].cardinality == 45
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_60_secs_ago(self):
        result = parse_time_references('60 secs ago')
        assert len(result) == 1
        assert result[0].cardinality == 60
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_60_secs(self):
        result = parse_time_references('60 secs')
        assert len(result) == 1
        assert result[0].cardinality == 60
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'


# =============================================================================
# Written-number cardinalities
# =============================================================================

class TestWrittenNumberCardinalities:
    """Test short abbreviations with written-number cardinalities."""

    def test_one_hr_ago(self):
        result = parse_time_references('one hr ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_one_hr(self):
        result = parse_time_references('one hr')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_two_hrs_ago(self):
        result = parse_time_references('two hrs ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_two_hrs(self):
        result = parse_time_references('two hrs')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_three_min_ago(self):
        result = parse_time_references('three min ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_three_min(self):
        result = parse_time_references('three min')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_four_mins_ago(self):
        result = parse_time_references('four mins ago')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_four_mins(self):
        result = parse_time_references('four mins')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_five_sec_ago(self):
        result = parse_time_references('five sec ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_five_sec(self):
        result = parse_time_references('five sec')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_six_secs_ago(self):
        result = parse_time_references('six secs ago')
        assert len(result) == 1
        assert result[0].cardinality == 6
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_six_secs(self):
        result = parse_time_references('six secs')
        assert len(result) == 1
        assert result[0].cardinality == 6
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'


# =============================================================================
# Hedges: about, roughly
# =============================================================================

class TestHedges:
    """Test short abbreviations with hedge words."""

    def test_about_5_hr_ago(self):
        result = parse_time_references('about 5 hr ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_about_5_hr(self):
        result = parse_time_references('about 5 hr')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_about_5_hrs_ago(self):
        result = parse_time_references('about 5 hrs ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_about_5_hrs(self):
        result = parse_time_references('about 5 hrs')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_roughly_10_min_ago(self):
        result = parse_time_references('roughly 10 min ago')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_roughly_10_min(self):
        result = parse_time_references('roughly 10 min')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_roughly_10_mins_ago(self):
        result = parse_time_references('roughly 10 mins ago')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_roughly_10_mins(self):
        result = parse_time_references('roughly 10 mins')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_about_20_sec_ago(self):
        result = parse_time_references('about 20 sec ago')
        assert len(result) == 1
        assert result[0].cardinality == 20
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_about_20_sec(self):
        result = parse_time_references('about 20 sec')
        assert len(result) == 1
        assert result[0].cardinality == 20
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_about_20_secs_ago(self):
        result = parse_time_references('about 20 secs ago')
        assert len(result) == 1
        assert result[0].cardinality == 20
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_about_20_secs(self):
        result = parse_time_references('about 20 secs')
        assert len(result) == 1
        assert result[0].cardinality == 20
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'


# =============================================================================
# Sentence embedding contexts
# =============================================================================

class TestSentenceEmbedding:
    """Test short abbreviations embedded in sentences."""

    def test_updated_15_hr_ago(self):
        result = parse_time_references('updated 15 hr ago')
        assert len(result) == 1
        assert result[0].cardinality == 15
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_updated_15_hr(self):
        result = parse_time_references('updated 15 hr')
        assert len(result) == 1
        assert result[0].cardinality == 15
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_posted_2_hrs_ago(self):
        result = parse_time_references('posted 2 hrs ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_posted_2_hrs(self):
        result = parse_time_references('posted 2 hrs')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_cached_5_min_ago(self):
        result = parse_time_references('cached 5 min ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_cached_5_min(self):
        result = parse_time_references('cached 5 min')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_sent_10_mins_ago(self):
        result = parse_time_references('sent 10 mins ago')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_sent_10_mins(self):
        result = parse_time_references('sent 10 mins')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_logged_30_sec_ago(self):
        result = parse_time_references('logged 30 sec ago')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_logged_30_sec(self):
        result = parse_time_references('logged 30 sec')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_received_45_secs_ago(self):
        result = parse_time_references('received 45 secs ago')
        assert len(result) == 1
        assert result[0].cardinality == 45
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_received_45_secs(self):
        result = parse_time_references('received 45 secs')
        assert len(result) == 1
        assert result[0].cardinality == 45
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'


# =============================================================================
# Mixed case variations
# =============================================================================

class TestMixedCase:
    """Test case insensitivity for short abbreviations."""

    def test_15_HR_ago(self):
        result = parse_time_references('15 HR ago')
        assert len(result) == 1
        assert result[0].cardinality == 15
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_15_HR(self):
        result = parse_time_references('15 HR')
        assert len(result) == 1
        assert result[0].cardinality == 15
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_15_Hr_ago(self):
        result = parse_time_references('15 Hr ago')
        assert len(result) == 1
        assert result[0].cardinality == 15
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_15_Hr(self):
        result = parse_time_references('15 Hr')
        assert len(result) == 1
        assert result[0].cardinality == 15
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_15_HRS_ago(self):
        result = parse_time_references('15 HRS ago')
        assert len(result) == 1
        assert result[0].cardinality == 15
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_15_HRS(self):
        result = parse_time_references('15 HRS')
        assert len(result) == 1
        assert result[0].cardinality == 15
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_2_MIN_ago(self):
        result = parse_time_references('2 MIN ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_2_MIN(self):
        result = parse_time_references('2 MIN')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_2_Min_ago(self):
        result = parse_time_references('2 Min ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_2_Min(self):
        result = parse_time_references('2 Min')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_2_MINS_ago(self):
        result = parse_time_references('2 MINS ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_2_MINS(self):
        result = parse_time_references('2 MINS')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_3_SEC_ago(self):
        result = parse_time_references('3 SEC ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_3_SEC(self):
        result = parse_time_references('3 SEC')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_3_Sec_ago(self):
        result = parse_time_references('3 Sec ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_3_Sec(self):
        result = parse_time_references('3 Sec')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_3_SECS_ago(self):
        result = parse_time_references('3 SECS ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_3_SECS(self):
        result = parse_time_references('3 SECS')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'


# =============================================================================
# Boundary cardinalities
# =============================================================================

class TestBoundaryCardinalities:
    """Test boundary values for cardinalities."""

    def test_100_hr_ago(self):
        result = parse_time_references('100 hr ago')
        assert len(result) == 1
        assert result[0].cardinality == 100
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_100_hr(self):
        result = parse_time_references('100 hr')
        assert len(result) == 1
        assert result[0].cardinality == 100
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_999_hrs_ago(self):
        result = parse_time_references('999 hrs ago')
        assert len(result) == 1
        assert result[0].cardinality == 999
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_999_hrs(self):
        result = parse_time_references('999 hrs')
        assert len(result) == 1
        assert result[0].cardinality == 999
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_100_min_ago(self):
        result = parse_time_references('100 min ago')
        assert len(result) == 1
        assert result[0].cardinality == 100
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_100_min(self):
        result = parse_time_references('100 min')
        assert len(result) == 1
        assert result[0].cardinality == 100
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_999_mins_ago(self):
        result = parse_time_references('999 mins ago')
        assert len(result) == 1
        assert result[0].cardinality == 999
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_999_mins(self):
        result = parse_time_references('999 mins')
        assert len(result) == 1
        assert result[0].cardinality == 999
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_100_sec_ago(self):
        result = parse_time_references('100 sec ago')
        assert len(result) == 1
        assert result[0].cardinality == 100
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_100_sec(self):
        result = parse_time_references('100 sec')
        assert len(result) == 1
        assert result[0].cardinality == 100
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_999_secs_ago(self):
        result = parse_time_references('999 secs ago')
        assert len(result) == 1
        assert result[0].cardinality == 999
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_999_secs(self):
        result = parse_time_references('999 secs')
        assert len(result) == 1
        assert result[0].cardinality == 999
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'


# =============================================================================
# Negative cases: should NOT match
# =============================================================================

class TestNegativeCases:
    """Test inputs that should NOT match."""

    def test_hr_alone(self):
        """Bare 'hr' without cardinality should not match."""
        result = parse_time_references('hr')
        assert len(result) == 0

    def test_hrs_alone(self):
        """Bare 'hrs' without cardinality should not match."""
        result = parse_time_references('hrs')
        assert len(result) == 0

    def test_min_alone(self):
        """Bare 'min' without cardinality should not match."""
        result = parse_time_references('min')
        assert len(result) == 0

    def test_mins_alone(self):
        """Bare 'mins' without cardinality should not match."""
        result = parse_time_references('mins')
        assert len(result) == 0

    def test_sec_alone(self):
        """Bare 'sec' without cardinality should not match."""
        result = parse_time_references('sec')
        assert len(result) == 0

    def test_secs_alone(self):
        """Bare 'secs' without cardinality should not match."""
        result = parse_time_references('secs')
        assert len(result) == 0

    def test_0_hr(self):
        """Zero cardinality should not match."""
        result = parse_time_references('0 hr')
        assert len(result) == 0

    def test_0_hrs(self):
        """Zero cardinality should not match."""
        result = parse_time_references('0 hrs')
        assert len(result) == 0

    def test_0_min(self):
        """Zero cardinality should not match."""
        result = parse_time_references('0 min')
        assert len(result) == 0

    def test_0_mins(self):
        """Zero cardinality should not match."""
        result = parse_time_references('0 mins')
        assert len(result) == 0

    def test_0_sec(self):
        """Zero cardinality should not match."""
        result = parse_time_references('0 sec')
        assert len(result) == 0

    def test_0_secs(self):
        """Zero cardinality should not match."""
        result = parse_time_references('0 secs')
        assert len(result) == 0


# =============================================================================
# Additional numeric variations for comprehensive coverage
# =============================================================================

class TestHoursAdditionalNumeric:
    """Additional numeric tests for hours to reach 250+ total."""

    def test_3_hr_ago(self):
        result = parse_time_references('3 hr ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'hour'

    def test_3_hr(self):
        result = parse_time_references('3 hr')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'hour'

    def test_4_hrs_ago(self):
        result = parse_time_references('4 hrs ago')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'hour'

    def test_4_hrs(self):
        result = parse_time_references('4 hrs')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'hour'

    def test_6_hr_ago(self):
        result = parse_time_references('6 hr ago')
        assert len(result) == 1
        assert result[0].cardinality == 6
        assert result[0].frame == 'hour'

    def test_6_hr(self):
        result = parse_time_references('6 hr')
        assert len(result) == 1
        assert result[0].cardinality == 6
        assert result[0].frame == 'hour'

    def test_7_hrs_ago(self):
        result = parse_time_references('7 hrs ago')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'hour'

    def test_7_hrs(self):
        result = parse_time_references('7 hrs')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'hour'

    def test_8_hr_ago(self):
        result = parse_time_references('8 hr ago')
        assert len(result) == 1
        assert result[0].cardinality == 8
        assert result[0].frame == 'hour'

    def test_8_hr(self):
        result = parse_time_references('8 hr')
        assert len(result) == 1
        assert result[0].cardinality == 8
        assert result[0].frame == 'hour'

    def test_9_hrs_ago(self):
        result = parse_time_references('9 hrs ago')
        assert len(result) == 1
        assert result[0].cardinality == 9
        assert result[0].frame == 'hour'

    def test_9_hrs(self):
        result = parse_time_references('9 hrs')
        assert len(result) == 1
        assert result[0].cardinality == 9
        assert result[0].frame == 'hour'

    def test_12_hr_ago(self):
        result = parse_time_references('12 hr ago')
        assert len(result) == 1
        assert result[0].cardinality == 12
        assert result[0].frame == 'hour'

    def test_12_hr(self):
        result = parse_time_references('12 hr')
        assert len(result) == 1
        assert result[0].cardinality == 12
        assert result[0].frame == 'hour'

    def test_18_hrs_ago(self):
        result = parse_time_references('18 hrs ago')
        assert len(result) == 1
        assert result[0].cardinality == 18
        assert result[0].frame == 'hour'

    def test_18_hrs(self):
        result = parse_time_references('18 hrs')
        assert len(result) == 1
        assert result[0].cardinality == 18
        assert result[0].frame == 'hour'

    def test_20_hr_ago(self):
        result = parse_time_references('20 hr ago')
        assert len(result) == 1
        assert result[0].cardinality == 20
        assert result[0].frame == 'hour'

    def test_20_hr(self):
        result = parse_time_references('20 hr')
        assert len(result) == 1
        assert result[0].cardinality == 20
        assert result[0].frame == 'hour'

    def test_36_hrs_ago(self):
        result = parse_time_references('36 hrs ago')
        assert len(result) == 1
        assert result[0].cardinality == 36
        assert result[0].frame == 'hour'

    def test_36_hrs(self):
        result = parse_time_references('36 hrs')
        assert len(result) == 1
        assert result[0].cardinality == 36
        assert result[0].frame == 'hour'

    def test_72_hr_ago(self):
        result = parse_time_references('72 hr ago')
        assert len(result) == 1
        assert result[0].cardinality == 72
        assert result[0].frame == 'hour'

    def test_72_hr(self):
        result = parse_time_references('72 hr')
        assert len(result) == 1
        assert result[0].cardinality == 72
        assert result[0].frame == 'hour'


class TestMinutesAdditionalNumeric:
    """Additional numeric tests for minutes."""

    def test_3_min_ago(self):
        result = parse_time_references('3 min ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'minute'

    def test_3_min(self):
        result = parse_time_references('3 min')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'minute'

    def test_4_mins_ago(self):
        result = parse_time_references('4 mins ago')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'minute'

    def test_4_mins(self):
        result = parse_time_references('4 mins')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'minute'

    def test_6_min_ago(self):
        result = parse_time_references('6 min ago')
        assert len(result) == 1
        assert result[0].cardinality == 6
        assert result[0].frame == 'minute'

    def test_6_min(self):
        result = parse_time_references('6 min')
        assert len(result) == 1
        assert result[0].cardinality == 6
        assert result[0].frame == 'minute'

    def test_7_mins_ago(self):
        result = parse_time_references('7 mins ago')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'minute'

    def test_7_mins(self):
        result = parse_time_references('7 mins')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'minute'

    def test_8_min_ago(self):
        result = parse_time_references('8 min ago')
        assert len(result) == 1
        assert result[0].cardinality == 8
        assert result[0].frame == 'minute'

    def test_8_min(self):
        result = parse_time_references('8 min')
        assert len(result) == 1
        assert result[0].cardinality == 8
        assert result[0].frame == 'minute'

    def test_9_mins_ago(self):
        result = parse_time_references('9 mins ago')
        assert len(result) == 1
        assert result[0].cardinality == 9
        assert result[0].frame == 'minute'

    def test_9_mins(self):
        result = parse_time_references('9 mins')
        assert len(result) == 1
        assert result[0].cardinality == 9
        assert result[0].frame == 'minute'

    def test_12_min_ago(self):
        result = parse_time_references('12 min ago')
        assert len(result) == 1
        assert result[0].cardinality == 12
        assert result[0].frame == 'minute'

    def test_12_min(self):
        result = parse_time_references('12 min')
        assert len(result) == 1
        assert result[0].cardinality == 12
        assert result[0].frame == 'minute'

    def test_20_mins_ago(self):
        result = parse_time_references('20 mins ago')
        assert len(result) == 1
        assert result[0].cardinality == 20
        assert result[0].frame == 'minute'

    def test_20_mins(self):
        result = parse_time_references('20 mins')
        assert len(result) == 1
        assert result[0].cardinality == 20
        assert result[0].frame == 'minute'

    def test_25_min_ago(self):
        result = parse_time_references('25 min ago')
        assert len(result) == 1
        assert result[0].cardinality == 25
        assert result[0].frame == 'minute'

    def test_25_min(self):
        result = parse_time_references('25 min')
        assert len(result) == 1
        assert result[0].cardinality == 25
        assert result[0].frame == 'minute'

    def test_35_mins_ago(self):
        result = parse_time_references('35 mins ago')
        assert len(result) == 1
        assert result[0].cardinality == 35
        assert result[0].frame == 'minute'

    def test_35_mins(self):
        result = parse_time_references('35 mins')
        assert len(result) == 1
        assert result[0].cardinality == 35
        assert result[0].frame == 'minute'

    def test_50_min_ago(self):
        result = parse_time_references('50 min ago')
        assert len(result) == 1
        assert result[0].cardinality == 50
        assert result[0].frame == 'minute'

    def test_50_min(self):
        result = parse_time_references('50 min')
        assert len(result) == 1
        assert result[0].cardinality == 50
        assert result[0].frame == 'minute'


class TestSecondsAdditionalNumeric:
    """Additional numeric tests for seconds."""

    def test_2_sec_ago(self):
        result = parse_time_references('2 sec ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'second'

    def test_2_sec(self):
        result = parse_time_references('2 sec')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'second'

    def test_4_secs_ago(self):
        result = parse_time_references('4 secs ago')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'second'

    def test_4_secs(self):
        result = parse_time_references('4 secs')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'second'

    def test_6_sec_ago(self):
        result = parse_time_references('6 sec ago')
        assert len(result) == 1
        assert result[0].cardinality == 6
        assert result[0].frame == 'second'

    def test_6_sec(self):
        result = parse_time_references('6 sec')
        assert len(result) == 1
        assert result[0].cardinality == 6
        assert result[0].frame == 'second'

    def test_7_secs_ago(self):
        result = parse_time_references('7 secs ago')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'second'

    def test_7_secs(self):
        result = parse_time_references('7 secs')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'second'

    def test_8_sec_ago(self):
        result = parse_time_references('8 sec ago')
        assert len(result) == 1
        assert result[0].cardinality == 8
        assert result[0].frame == 'second'

    def test_8_sec(self):
        result = parse_time_references('8 sec')
        assert len(result) == 1
        assert result[0].cardinality == 8
        assert result[0].frame == 'second'

    def test_9_secs_ago(self):
        result = parse_time_references('9 secs ago')
        assert len(result) == 1
        assert result[0].cardinality == 9
        assert result[0].frame == 'second'

    def test_9_secs(self):
        result = parse_time_references('9 secs')
        assert len(result) == 1
        assert result[0].cardinality == 9
        assert result[0].frame == 'second'

    def test_12_sec_ago(self):
        result = parse_time_references('12 sec ago')
        assert len(result) == 1
        assert result[0].cardinality == 12
        assert result[0].frame == 'second'

    def test_12_sec(self):
        result = parse_time_references('12 sec')
        assert len(result) == 1
        assert result[0].cardinality == 12
        assert result[0].frame == 'second'

    def test_20_secs_ago(self):
        result = parse_time_references('20 secs ago')
        assert len(result) == 1
        assert result[0].cardinality == 20
        assert result[0].frame == 'second'

    def test_20_secs(self):
        result = parse_time_references('20 secs')
        assert len(result) == 1
        assert result[0].cardinality == 20
        assert result[0].frame == 'second'

    def test_25_sec_ago(self):
        result = parse_time_references('25 sec ago')
        assert len(result) == 1
        assert result[0].cardinality == 25
        assert result[0].frame == 'second'

    def test_25_sec(self):
        result = parse_time_references('25 sec')
        assert len(result) == 1
        assert result[0].cardinality == 25
        assert result[0].frame == 'second'

    def test_35_secs_ago(self):
        result = parse_time_references('35 secs ago')
        assert len(result) == 1
        assert result[0].cardinality == 35
        assert result[0].frame == 'second'

    def test_35_secs(self):
        result = parse_time_references('35 secs')
        assert len(result) == 1
        assert result[0].cardinality == 35
        assert result[0].frame == 'second'

    def test_50_sec_ago(self):
        result = parse_time_references('50 sec ago')
        assert len(result) == 1
        assert result[0].cardinality == 50
        assert result[0].frame == 'second'

    def test_50_sec(self):
        result = parse_time_references('50 sec')
        assert len(result) == 1
        assert result[0].cardinality == 50
        assert result[0].frame == 'second'


# =============================================================================
# Additional hedge and context variations
# =============================================================================

class TestAdditionalContexts:
    """More sentence contexts and hedge variations to reach 250+."""

    def test_approximately_3_hr_ago(self):
        result = parse_time_references('approximately 3 hr ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'hour'

    def test_around_7_hrs(self):
        result = parse_time_references('around 7 hrs')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'hour'

    def test_almost_15_min_ago(self):
        result = parse_time_references('almost 15 min ago')
        assert len(result) == 1
        assert result[0].cardinality == 15
        assert result[0].frame == 'minute'

    def test_nearly_20_mins(self):
        result = parse_time_references('nearly 20 mins')
        assert len(result) == 1
        assert result[0].cardinality == 20
        assert result[0].frame == 'minute'

    def test_just_30_sec_ago(self):
        result = parse_time_references('just 30 sec ago')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'second'

    def test_only_45_secs(self):
        result = parse_time_references('only 45 secs')
        assert len(result) == 1
        assert result[0].cardinality == 45
        assert result[0].frame == 'second'

    def test_compiled_12_hr_ago(self):
        result = parse_time_references('compiled 12 hr ago')
        assert len(result) == 1
        assert result[0].cardinality == 12
        assert result[0].frame == 'hour'

    def test_deployed_6_hrs(self):
        result = parse_time_references('deployed 6 hrs')
        assert len(result) == 1
        assert result[0].cardinality == 6
        assert result[0].frame == 'hour'

    def test_refreshed_8_min_ago(self):
        result = parse_time_references('refreshed 8 min ago')
        assert len(result) == 1
        assert result[0].cardinality == 8
        assert result[0].frame == 'minute'

    def test_modified_12_mins(self):
        result = parse_time_references('modified 12 mins')
        assert len(result) == 1
        assert result[0].cardinality == 12
        assert result[0].frame == 'minute'

    def test_triggered_15_sec_ago(self):
        result = parse_time_references('triggered 15 sec ago')
        assert len(result) == 1
        assert result[0].cardinality == 15
        assert result[0].frame == 'second'

    def test_executed_25_secs(self):
        result = parse_time_references('executed 25 secs')
        assert len(result) == 1
        assert result[0].cardinality == 25
        assert result[0].frame == 'second'

    def test_published_4_hr(self):
        result = parse_time_references('published 4 hr')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'hour'

    def test_indexed_9_hrs_ago(self):
        result = parse_time_references('indexed 9 hrs ago')
        assert len(result) == 1
        assert result[0].cardinality == 9
        assert result[0].frame == 'hour'

    def test_synced_7_min(self):
        result = parse_time_references('synced 7 min')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'minute'

    def test_backed_up_18_mins_ago(self):
        result = parse_time_references('backed up 18 mins ago')
        assert len(result) == 1
        assert result[0].cardinality == 18
        assert result[0].frame == 'minute'

    def test_scanned_9_sec(self):
        result = parse_time_references('scanned 9 sec')
        assert len(result) == 1
        assert result[0].cardinality == 9
        assert result[0].frame == 'second'

    def test_validated_12_secs_ago(self):
        result = parse_time_references('validated 12 secs ago')
        assert len(result) == 1
        assert result[0].cardinality == 12
        assert result[0].frame == 'second'
