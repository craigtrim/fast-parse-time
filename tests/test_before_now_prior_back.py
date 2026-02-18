#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Tests for past-tense suffix aliases: 'before now', 'prior', and 'back'.

Related GitHub Issue:
    #8 - Gap: 'before now' pattern not recognized for past tense
    https://github.com/craigtrim/fast-parse-time/issues/8

Semantics:
    'N unit before now' == 'N unit ago' == RelativeTime(cardinality=N, frame=unit, tense='past')
    'N unit prior'      == 'N unit ago' == RelativeTime(cardinality=N, frame=unit, tense='past')
    'N unit back'       == 'N unit ago' == RelativeTime(cardinality=N, frame=unit, tense='past')

Note on 'prior to now': excluded because 'to' cannot be added as a keyterm
(too common; would break unrelated sequences). 'N unit prior to now' naturally
splits into sequence ['N', 'unit', 'prior'] + standalone ['now'], yielding two
results. Users should use 'N unit prior' or 'N unit before now' instead.

Units covered: seconds/secs/sec, minutes/mins/min, hours/hrs/hr,
               days, weeks/wks/wk, months/mos/mo, years/yrs/yr
"""

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

class TestBeforeNowCoreUnits:
    """N unit before now returns past-tense RelativeTime with correct fields."""

    def test_5_minutes_before_now(self):
        result = parse_time_references('5 minutes before now')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_5_hours_before_now(self):
        result = parse_time_references('5 hours before now')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_7_days_before_now(self):
        result = parse_time_references('7 days before now')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_1_week_before_now(self):
        result = parse_time_references('1 week before now')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_3_months_before_now(self):
        result = parse_time_references('3 months before now')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_2_years_before_now(self):
        result = parse_time_references('2 years before now')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_30_seconds_before_now(self):
        result = parse_time_references('30 seconds before now')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'


# ============================================================================
# Group 2: 'before now' -- abbreviated unit forms
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

class TestPriorCoreUnits:
    """N unit prior returns past-tense RelativeTime with correct fields."""

    def test_5_minutes_prior(self):
        result = parse_time_references('5 minutes prior')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_5_hours_prior(self):
        result = parse_time_references('5 hours prior')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_7_days_prior(self):
        result = parse_time_references('7 days prior')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_1_week_prior(self):
        result = parse_time_references('1 week prior')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_3_months_prior(self):
        result = parse_time_references('3 months prior')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_2_years_prior(self):
        result = parse_time_references('2 years prior')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_30_seconds_prior(self):
        result = parse_time_references('30 seconds prior')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'


# ============================================================================
# Group 4: 'prior' -- abbreviated unit forms
# ============================================================================

class TestPriorAbbreviatedUnits:
    """Abbreviated unit forms work with 'prior'."""

    def test_5_mins_prior(self):
        result = parse_time_references('5 mins prior')
        assert len(result) == 1
        assert result[0].frame == 'minute'

    def test_5_hrs_prior(self):
        result = parse_time_references('5 hrs prior')
        assert len(result) == 1
        assert result[0].frame == 'hour'

    def test_2_wks_prior(self):
        result = parse_time_references('2 wks prior')
        assert len(result) == 1
        assert result[0].frame == 'week'

    def test_3_mos_prior(self):
        result = parse_time_references('3 mos prior')
        assert len(result) == 1
        assert result[0].frame == 'month'

    def test_2_yrs_prior(self):
        result = parse_time_references('2 yrs prior')
        assert len(result) == 1
        assert result[0].frame == 'year'

    def test_10_secs_prior(self):
        result = parse_time_references('10 secs prior')
        assert len(result) == 1
        assert result[0].frame == 'second'


# ============================================================================
# Group 5: 'back' -- core unit coverage
# ============================================================================

class TestBackCoreUnits:
    """N unit back returns past-tense RelativeTime with correct fields."""

    def test_5_minutes_back(self):
        result = parse_time_references('5 minutes back')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_5_hours_back(self):
        result = parse_time_references('5 hours back')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_7_days_back(self):
        result = parse_time_references('7 days back')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_1_week_back(self):
        result = parse_time_references('1 week back')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_3_months_back(self):
        result = parse_time_references('3 months back')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_2_years_back(self):
        result = parse_time_references('2 years back')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_30_seconds_back(self):
        result = parse_time_references('30 seconds back')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'


# ============================================================================
# Group 6: 'back' -- abbreviated unit forms
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

class TestPhraseContext:
    """Expressions are extracted correctly when embedded in sentences."""

    def test_sent_from_5_minutes_before_now(self):
        result = parse_time_references('data from 5 minutes before now')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'minute'

    def test_sent_records_3_days_before_now(self):
        result = parse_time_references('records created 3 days before now')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'day'

    def test_sent_meeting_2_weeks_prior(self):
        result = parse_time_references('meeting scheduled 2 weeks prior')
        assert len(result) == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_sent_report_submitted_6_months_prior(self):
        result = parse_time_references('report submitted 6 months prior')
        assert len(result) == 1
        assert result[0].cardinality == 6
        assert result[0].frame == 'month'

    def test_sent_sent_10_minutes_back(self):
        result = parse_time_references('message sent 10 minutes back')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'minute'

    def test_sent_created_5_days_back(self):
        result = parse_time_references('file created 5 days back')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'day'


# ============================================================================
# Group 8: has_temporal_info
# ============================================================================

class TestHasTemporalInfo:
    """has_temporal_info returns True for texts with the new patterns."""

    def test_before_now_has_temporal_info(self):
        assert has_temporal_info('5 minutes before now') is True

    def test_prior_has_temporal_info(self):
        assert has_temporal_info('3 days prior') is True

    def test_back_has_temporal_info(self):
        assert has_temporal_info('7 hours back') is True

    def test_before_now_in_sentence(self):
        assert has_temporal_info('data from 5 days before now') is True

    def test_prior_in_sentence(self):
        assert has_temporal_info('submitted 2 months prior') is True

    def test_back_in_sentence(self):
        assert has_temporal_info('created 3 weeks back') is True

    def test_non_temporal_false(self):
        assert has_temporal_info('regular text') is False

    def test_another_non_temporal_false(self):
        assert has_temporal_info('hello world') is False


# ============================================================================
# Group 9: extract_past_references
# ============================================================================

class TestExtractPastReferences:
    """All three suffixes produce past-tense references."""

    def test_before_now_is_past(self):
        result = extract_past_references('5 minutes before now')
        assert len(result) == 1
        assert result[0].tense == 'past'

    def test_prior_is_past(self):
        result = extract_past_references('3 days prior')
        assert len(result) == 1
        assert result[0].tense == 'past'

    def test_back_is_past(self):
        result = extract_past_references('7 hours back')
        assert len(result) == 1
        assert result[0].tense == 'past'


# ============================================================================
# Group 10: extract_future_references returns nothing
# ============================================================================

class TestNotFutureReferences:
    """Past-tense expressions must not appear in future results."""

    def test_before_now_not_future(self):
        result = extract_future_references('5 minutes before now')
        assert len(result) == 0

    def test_prior_not_future(self):
        result = extract_future_references('3 days prior')
        assert len(result) == 0

    def test_back_not_future(self):
        result = extract_future_references('7 hours back')
        assert len(result) == 0


# ============================================================================
# Group 11: resolve_to_timedelta -- negative delta (past)
# ============================================================================

class TestResolveToTimedelta:
    """Past-tense results resolve to negative timedeltas."""

    def test_before_now_timedelta_is_timedelta(self):
        result = resolve_to_timedelta('5 days before now')
        assert len(result) == 1
        assert isinstance(result[0], timedelta)

    def test_before_now_timedelta_negative(self):
        result = resolve_to_timedelta('5 days before now')
        assert result[0] < timedelta(0)

    def test_prior_timedelta_negative(self):
        result = resolve_to_timedelta('3 months prior')
        assert len(result) == 1
        assert result[0] < timedelta(0)

    def test_back_timedelta_negative(self):
        result = resolve_to_timedelta('2 weeks back')
        assert len(result) == 1
        assert result[0] < timedelta(0)

    def test_before_now_5_days_delta_value(self):
        result = resolve_to_timedelta('5 days before now')
        assert result[0] == timedelta(days=-5)

    def test_prior_2_weeks_delta_value(self):
        result = resolve_to_timedelta('2 weeks prior')
        assert result[0] == timedelta(days=-14)


# ============================================================================
# Group 12: parse_dates integration
# ============================================================================

class TestParseDatesIntegration:
    """parse_dates picks up the new patterns in combined results."""

    def test_before_now_parse_dates_has_dates(self):
        result = parse_dates('5 minutes before now')
        assert result.has_dates is True

    def test_prior_parse_dates_has_dates(self):
        result = parse_dates('3 days prior')
        assert result.has_dates is True

    def test_back_parse_dates_has_dates(self):
        result = parse_dates('7 hours back')
        assert result.has_dates is True

    def test_before_now_relative_times(self):
        result = parse_dates('5 minutes before now')
        assert len(result.relative_times) == 1
        assert result.relative_times[0].tense == 'past'

    def test_prior_relative_times(self):
        result = parse_dates('3 days prior')
        assert len(result.relative_times) == 1
        assert result.relative_times[0].frame == 'day'

    def test_back_relative_times(self):
        result = parse_dates('7 hours back')
        assert len(result.relative_times) == 1
        assert result.relative_times[0].frame == 'hour'


# ============================================================================
# Group 13: Case insensitivity
# ============================================================================

class TestCaseInsensitivity:
    """All patterns are case-insensitive (input is lowercased)."""

    def test_BEFORE_NOW_uppercase(self):
        result = parse_time_references('5 DAYS BEFORE NOW')
        assert len(result) == 1
        assert result[0].tense == 'past'

    def test_PRIOR_uppercase(self):
        result = parse_time_references('3 MONTHS PRIOR')
        assert len(result) == 1
        assert result[0].tense == 'past'

    def test_BACK_uppercase(self):
        result = parse_time_references('7 HOURS BACK')
        assert len(result) == 1
        assert result[0].tense == 'past'


# ============================================================================
# Group 14: Regression -- existing patterns unaffected
# ============================================================================

class TestRegression:
    """Existing patterns still work after adding before now / prior / back."""

    def test_5_days_ago_still_works(self):
        result = parse_time_references('5 days ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].tense == 'past'

    def test_last_week_still_works(self):
        result = parse_time_references('last week')
        assert len(result) == 1
        assert result[0].tense == 'past'

    def test_3_months_ago_still_works(self):
        result = parse_time_references('3 months ago')
        assert len(result) == 1
        assert result[0].cardinality == 3

    def test_tomorrow_still_works(self):
        result = parse_time_references('tomorrow')
        assert len(result) == 1
        assert result[0].tense == 'future'

    def test_5_days_from_now_still_works(self):
        result = parse_time_references('5 days from now')
        assert len(result) == 1
        assert result[0].tense == 'future'
        assert result[0].cardinality == 5

    def test_now_still_works(self):
        result = parse_time_references('now')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_eod_still_works(self):
        result = parse_time_references('eod')
        assert len(result) == 1
        assert result[0].tense == 'future'

    def test_yesterday_still_works(self):
        result = parse_time_references('yesterday')
        assert len(result) == 1
        assert result[0].tense == 'past'

    def test_half_an_hour_ago_still_works(self):
        result = parse_time_references('half an hour ago')
        assert len(result) == 1
        assert result[0].cardinality == 30

    def test_several_weeks_ago_still_works(self):
        result = parse_time_references('several weeks ago')
        assert len(result) == 1
        assert result[0].cardinality == 3

    def test_right_now_still_works(self):
        result = parse_time_references('right now')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_2_years_from_now_still_works(self):
        result = parse_time_references('2 years from now')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].tense == 'future'

    def test_has_temporal_info_regression_true(self):
        assert has_temporal_info('5 days ago') is True

    def test_has_temporal_info_regression_false(self):
        assert has_temporal_info('hello world') is False

    def test_10_hours_ago_still_works(self):
        result = parse_time_references('10 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'hour'

    def test_next_week_still_works(self):
        result = parse_time_references('next week')
        assert len(result) == 1
        assert result[0].tense == 'future'

    def test_eom_still_works(self):
        result = parse_time_references('eom')
        assert len(result) == 1
        assert result[0].frame == 'month'


# ============================================================================
# Group 15: Cardinality accuracy across all three patterns
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
