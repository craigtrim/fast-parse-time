#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Tests for end-of-period abbreviations: eod, eom, eoy.

Related GitHub Issue:
    #17 - Gap: end-of-period abbreviations not supported (eod, eom, eoy)
    https://github.com/craigtrim/fast-parse-time/issues/17

Semantics:
    eod -> RelativeTime(cardinality=0, frame='day',   tense='future')
    eom -> RelativeTime(cardinality=0, frame='month', tense='future')
    eoy -> RelativeTime(cardinality=0, frame='year',  tense='future')

All abbreviations are case-insensitive (input is lowercased before processing).
Single-token patterns: the sequence extractor picks up 'eod'/'eom'/'eoy'
from any phrase even when surrounded by non-time words.
"""

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

class TestEodBare:
    """Bare 'eod' returns exactly one RelativeTime with correct attributes."""

    def test_eod_returns_one_result(self):
        result = parse_time_references('eod')
        assert len(result) == 1

    def test_eod_cardinality(self):
        result = parse_time_references('eod')
        assert result[0].cardinality == 0

    def test_eod_frame(self):
        result = parse_time_references('eod')
        assert result[0].frame == 'day'

    def test_eod_tense(self):
        result = parse_time_references('eod')
        assert result[0].tense == 'future'

    def test_eod_is_relative_time(self):
        result = parse_time_references('eod')
        assert isinstance(result[0], RelativeTime)


# ============================================================================
# Group 2: Bare 'eom' -- basic attribute checks
# ============================================================================

class TestEomBare:
    """Bare 'eom' returns exactly one RelativeTime with correct attributes."""

    def test_eom_returns_one_result(self):
        result = parse_time_references('eom')
        assert len(result) == 1

    def test_eom_cardinality(self):
        result = parse_time_references('eom')
        assert result[0].cardinality == 0

    def test_eom_frame(self):
        result = parse_time_references('eom')
        assert result[0].frame == 'month'

    def test_eom_tense(self):
        result = parse_time_references('eom')
        assert result[0].tense == 'future'

    def test_eom_is_relative_time(self):
        result = parse_time_references('eom')
        assert isinstance(result[0], RelativeTime)


# ============================================================================
# Group 3: Bare 'eoy' -- basic attribute checks
# ============================================================================

class TestEoyBare:
    """Bare 'eoy' returns exactly one RelativeTime with correct attributes."""

    def test_eoy_returns_one_result(self):
        result = parse_time_references('eoy')
        assert len(result) == 1

    def test_eoy_cardinality(self):
        result = parse_time_references('eoy')
        assert result[0].cardinality == 0

    def test_eoy_frame(self):
        result = parse_time_references('eoy')
        assert result[0].frame == 'year'

    def test_eoy_tense(self):
        result = parse_time_references('eoy')
        assert result[0].tense == 'future'

    def test_eoy_is_relative_time(self):
        result = parse_time_references('eoy')
        assert isinstance(result[0], RelativeTime)


# ============================================================================
# Group 4: Uppercase variants (input is lowercased before processing)
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

class TestMixedCase:
    """Eod, Eom, Eoy (title case) should work identically to lowercase."""

    def test_Eod_mixed_case(self):
        result = parse_time_references('Eod')
        assert len(result) == 1
        assert result[0].frame == 'day'

    def test_Eom_mixed_case(self):
        result = parse_time_references('Eom')
        assert len(result) == 1
        assert result[0].frame == 'month'

    def test_Eoy_mixed_case(self):
        result = parse_time_references('Eoy')
        assert len(result) == 1
        assert result[0].frame == 'year'


# ============================================================================
# Group 6: Phrase context -- leading non-time words + eod
# ============================================================================

class TestEodInPhrase:
    """eod is extracted correctly when preceded by non-time words."""

    def test_meeting_eod(self):
        result = parse_time_references('meeting eod')
        assert len(result) == 1
        assert result[0].frame == 'day'

    def test_call_eod(self):
        result = parse_time_references('call eod')
        assert len(result) == 1
        assert result[0].frame == 'day'

    def test_reminder_eod(self):
        result = parse_time_references('reminder eod')
        assert len(result) == 1
        assert result[0].frame == 'day'

    def test_deadline_eod(self):
        result = parse_time_references('deadline eod')
        assert len(result) == 1
        assert result[0].frame == 'day'

    def test_submit_report_eod(self):
        result = parse_time_references('submit report eod')
        assert len(result) == 1
        assert result[0].frame == 'day'

    def test_status_update_eod(self):
        result = parse_time_references('status update eod')
        assert len(result) == 1
        assert result[0].frame == 'day'

    def test_project_eod(self):
        result = parse_time_references('project eod')
        assert len(result) == 1
        assert result[0].frame == 'day'

    def test_please_do_eod(self):
        result = parse_time_references('please do eod')
        assert len(result) == 1
        assert result[0].frame == 'day'


# ============================================================================
# Group 7: Phrase context -- leading non-time words + eom
# ============================================================================

class TestEomInPhrase:
    """eom is extracted correctly when preceded by non-time words."""

    def test_meeting_eom(self):
        result = parse_time_references('meeting eom')
        assert len(result) == 1
        assert result[0].frame == 'month'

    def test_call_eom(self):
        result = parse_time_references('call eom')
        assert len(result) == 1
        assert result[0].frame == 'month'

    def test_reminder_eom(self):
        result = parse_time_references('reminder eom')
        assert len(result) == 1
        assert result[0].frame == 'month'

    def test_deadline_eom(self):
        result = parse_time_references('deadline eom')
        assert len(result) == 1
        assert result[0].frame == 'month'

    def test_submit_report_eom(self):
        result = parse_time_references('submit report eom')
        assert len(result) == 1
        assert result[0].frame == 'month'

    def test_status_update_eom(self):
        result = parse_time_references('status update eom')
        assert len(result) == 1
        assert result[0].frame == 'month'

    def test_project_eom(self):
        result = parse_time_references('project eom')
        assert len(result) == 1
        assert result[0].frame == 'month'

    def test_please_do_eom(self):
        result = parse_time_references('please do eom')
        assert len(result) == 1
        assert result[0].frame == 'month'


# ============================================================================
# Group 8: Phrase context -- leading non-time words + eoy
# ============================================================================

class TestEoyInPhrase:
    """eoy is extracted correctly when preceded by non-time words."""

    def test_meeting_eoy(self):
        result = parse_time_references('meeting eoy')
        assert len(result) == 1
        assert result[0].frame == 'year'

    def test_call_eoy(self):
        result = parse_time_references('call eoy')
        assert len(result) == 1
        assert result[0].frame == 'year'

    def test_reminder_eoy(self):
        result = parse_time_references('reminder eoy')
        assert len(result) == 1
        assert result[0].frame == 'year'

    def test_deadline_eoy(self):
        result = parse_time_references('deadline eoy')
        assert len(result) == 1
        assert result[0].frame == 'year'

    def test_submit_report_eoy(self):
        result = parse_time_references('submit report eoy')
        assert len(result) == 1
        assert result[0].frame == 'year'

    def test_status_update_eoy(self):
        result = parse_time_references('status update eoy')
        assert len(result) == 1
        assert result[0].frame == 'year'

    def test_project_eoy(self):
        result = parse_time_references('project eoy')
        assert len(result) == 1
        assert result[0].frame == 'year'

    def test_please_do_eoy(self):
        result = parse_time_references('please do eoy')
        assert len(result) == 1
        assert result[0].frame == 'year'


# ============================================================================
# Group 9: Phrase context -- eod/eom/eoy followed by trailing non-time words
# ============================================================================

class TestAbbrevTrailing:
    """Abbreviations followed by non-time words are still extracted."""

    def test_eod_meeting(self):
        result = parse_time_references('eod meeting')
        assert len(result) == 1
        assert result[0].frame == 'day'

    def test_eod_call(self):
        result = parse_time_references('eod call')
        assert len(result) == 1
        assert result[0].frame == 'day'

    def test_eod_deadline(self):
        result = parse_time_references('eod deadline')
        assert len(result) == 1
        assert result[0].frame == 'day'

    def test_eom_meeting(self):
        result = parse_time_references('eom meeting')
        assert len(result) == 1
        assert result[0].frame == 'month'

    def test_eom_close(self):
        result = parse_time_references('eom close')
        assert len(result) == 1
        assert result[0].frame == 'month'

    def test_eoy_meeting(self):
        result = parse_time_references('eoy meeting')
        assert len(result) == 1
        assert result[0].frame == 'year'

    def test_eoy_close(self):
        result = parse_time_references('eoy close')
        assert len(result) == 1
        assert result[0].frame == 'year'


# ============================================================================
# Group 10: has_temporal_info
# ============================================================================

class TestHasTemporalInfo:
    """has_temporal_info returns True for texts containing eod/eom/eoy."""

    def test_eod_has_temporal_info(self):
        assert has_temporal_info('eod') is True

    def test_eom_has_temporal_info(self):
        assert has_temporal_info('eom') is True

    def test_eoy_has_temporal_info(self):
        assert has_temporal_info('eoy') is True

    def test_meeting_eod_has_temporal_info(self):
        assert has_temporal_info('meeting eod') is True

    def test_meeting_eom_has_temporal_info(self):
        assert has_temporal_info('meeting eom') is True

    def test_meeting_eoy_has_temporal_info(self):
        assert has_temporal_info('meeting eoy') is True

    def test_non_temporal_text_false(self):
        assert has_temporal_info('regular sentence with no dates') is False

    def test_another_non_temporal_false(self):
        assert has_temporal_info('just a random phrase') is False


# ============================================================================
# Group 11: extract_future_references
# ============================================================================

class TestExtractFutureReferences:
    """eod/eom/eoy are classified as future references."""

    def test_eod_is_future(self):
        result = extract_future_references('eod')
        assert len(result) == 1
        assert result[0].frame == 'day'

    def test_eom_is_future(self):
        result = extract_future_references('eom')
        assert len(result) == 1
        assert result[0].frame == 'month'

    def test_eoy_is_future(self):
        result = extract_future_references('eoy')
        assert len(result) == 1
        assert result[0].frame == 'year'

    def test_eod_in_phrase_is_future(self):
        result = extract_future_references('meeting eod')
        assert len(result) == 1

    def test_eom_in_phrase_is_future(self):
        result = extract_future_references('meeting eom')
        assert len(result) == 1

    def test_eoy_in_phrase_is_future(self):
        result = extract_future_references('meeting eoy')
        assert len(result) == 1


# ============================================================================
# Group 12: extract_past_references returns nothing for eod/eom/eoy
# ============================================================================

class TestNoPastReferences:
    """eod/eom/eoy are future references and should not appear in past results."""

    def test_eod_not_past(self):
        result = extract_past_references('eod')
        assert len(result) == 0

    def test_eom_not_past(self):
        result = extract_past_references('eom')
        assert len(result) == 0

    def test_eoy_not_past(self):
        result = extract_past_references('eoy')
        assert len(result) == 0


# ============================================================================
# Group 13: extract_relative_times
# ============================================================================

class TestExtractRelativeTimes:
    """extract_relative_times returns RelativeTime instances for eod/eom/eoy."""

    def test_eod_relative_time_instance(self):
        result = extract_relative_times('eod')
        assert len(result) == 1
        assert isinstance(result[0], RelativeTime)

    def test_eom_relative_time_instance(self):
        result = extract_relative_times('eom')
        assert len(result) == 1
        assert isinstance(result[0], RelativeTime)

    def test_eoy_relative_time_instance(self):
        result = extract_relative_times('eoy')
        assert len(result) == 1
        assert isinstance(result[0], RelativeTime)

    def test_eod_relative_time_frame(self):
        result = extract_relative_times('eod')
        assert result[0].frame == 'day'

    def test_eom_relative_time_frame(self):
        result = extract_relative_times('eom')
        assert result[0].frame == 'month'

    def test_eoy_relative_time_frame(self):
        result = extract_relative_times('eoy')
        assert result[0].frame == 'year'


# ============================================================================
# Group 14: resolve_to_timedelta
# ============================================================================

class TestResolveToTimedelta:
    """resolve_to_timedelta returns a timedelta for eod/eom/eoy."""

    def test_eod_timedelta_is_timedelta(self):
        result = resolve_to_timedelta('eod')
        assert len(result) == 1
        assert isinstance(result[0], timedelta)

    def test_eom_timedelta_is_timedelta(self):
        result = resolve_to_timedelta('eom')
        assert len(result) == 1
        assert isinstance(result[0], timedelta)

    def test_eoy_timedelta_is_timedelta(self):
        result = resolve_to_timedelta('eoy')
        assert len(result) == 1
        assert isinstance(result[0], timedelta)

    def test_eod_timedelta_not_negative(self):
        """eod is a future reference so delta should not be negative."""
        result = resolve_to_timedelta('eod')
        assert result[0] >= timedelta(0)

    def test_eom_timedelta_not_negative(self):
        result = resolve_to_timedelta('eom')
        assert result[0] >= timedelta(0)

    def test_eoy_timedelta_not_negative(self):
        result = resolve_to_timedelta('eoy')
        assert result[0] >= timedelta(0)


# ============================================================================
# Group 15: parse_dates integration
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

class TestMultipleAbbreviations:
    """Multiple end-of-period abbreviations in one sentence are all extracted."""

    def test_eod_and_eom(self):
        """Text with both eod and eom should return 2 results."""
        result = parse_time_references('eod and eom')
        assert len(result) == 2
        frames = {r.frame for r in result}
        assert 'day' in frames
        assert 'month' in frames

    def test_eod_and_eoy(self):
        result = parse_time_references('eod and eoy')
        assert len(result) == 2
        frames = {r.frame for r in result}
        assert 'day' in frames
        assert 'year' in frames

    def test_eom_and_eoy(self):
        result = parse_time_references('eom and eoy')
        assert len(result) == 2
        frames = {r.frame for r in result}
        assert 'month' in frames
        assert 'year' in frames

    def test_all_three_abbreviations(self):
        """Three abbreviations separated by non-time words produce 3 results."""
        result = parse_time_references('eod and eom and eoy')
        assert len(result) == 3
        frames = {r.frame for r in result}
        assert frames == {'day', 'month', 'year'}


# ============================================================================
# Group 17: RelativeTime.to_timedelta via dataclass method
# ============================================================================

class TestRelativeTimeDataclass:
    """RelativeTime instances created for eod/eom/eoy support all methods."""

    def test_eod_to_timedelta(self):
        rt = RelativeTime(cardinality=0, frame='day', tense='future')
        delta = rt.to_timedelta()
        assert isinstance(delta, timedelta)

    def test_eom_to_timedelta(self):
        rt = RelativeTime(cardinality=0, frame='month', tense='future')
        delta = rt.to_timedelta()
        assert isinstance(delta, timedelta)

    def test_eoy_to_timedelta(self):
        rt = RelativeTime(cardinality=0, frame='year', tense='future')
        delta = rt.to_timedelta()
        assert isinstance(delta, timedelta)

    def test_eod_cardinality_zero(self):
        rt = RelativeTime(cardinality=0, frame='day', tense='future')
        assert rt.cardinality == 0

    def test_eom_cardinality_zero(self):
        rt = RelativeTime(cardinality=0, frame='month', tense='future')
        assert rt.cardinality == 0

    def test_eoy_cardinality_zero(self):
        rt = RelativeTime(cardinality=0, frame='year', tense='future')
        assert rt.cardinality == 0


# ============================================================================
# Group 18: Regression -- existing patterns unaffected
# ============================================================================

class TestRegression:
    """Existing time reference patterns still work after adding eod/eom/eoy."""

    def test_yesterday_still_works(self):
        result = parse_time_references('yesterday')
        assert len(result) == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_tomorrow_still_works(self):
        result = parse_time_references('tomorrow')
        assert len(result) == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'future'

    def test_5_days_ago(self):
        result = parse_time_references('5 days ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_last_week(self):
        result = parse_time_references('last week')
        assert len(result) == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_next_week(self):
        result = parse_time_references('next week')
        assert len(result) == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'future'

    def test_3_months_ago(self):
        result = parse_time_references('3 months ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_2_years_from_now(self):
        result = parse_time_references('2 years from now')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'year'
        assert result[0].tense == 'future'

    def test_1_hour_ago(self):
        result = parse_time_references('1 hour ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'

    def test_10_minutes_from_now(self):
        result = parse_time_references('10 minutes from now')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'minute'

    def test_30_seconds_ago(self):
        result = parse_time_references('30 seconds ago')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'second'

    def test_half_an_hour_ago(self):
        result = parse_time_references('half an hour ago')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'minute'

    def test_several_days_ago(self):
        result = parse_time_references('several days ago')
        assert len(result) == 1
        assert result[0].cardinality == 3

    def test_has_temporal_info_regression(self):
        assert has_temporal_info('5 days ago') is True

    def test_no_temporal_info_regression(self):
        assert has_temporal_info('hello world') is False
