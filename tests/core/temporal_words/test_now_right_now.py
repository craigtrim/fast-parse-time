#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Tests for present-tense temporal expressions: 'now' and 'right now'.

Related GitHub Issue:
    #16 - Gap: 'now' and 'right now' not recognized as present-tense references
    https://github.com/craigtrim/fast-parse-time/issues/16

Semantics:
    now       -> RelativeTime(cardinality=0, frame='second', tense='present')
    right now -> RelativeTime(cardinality=0, frame='second', tense='present')

Both are zero-offset anchors to the current moment, modelled identically to how
'today', 'tonight', and 'this morning' are anchors to the current day.

Critical disambiguation: 'now' appearing inside an existing pattern like
'5 days from now' must NOT produce an extra present-tense result. The
set-intersection algorithm handles this naturally - 'now' as a standalone
pattern only wins when the entire sequence is ['now'].
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
# Group 1: Bare 'now' -- basic attribute checks
# ============================================================================

class TestNowBare:
    """Bare 'now' returns exactly one present-tense RelativeTime."""

    def test_now_returns_one_result(self):
        result = parse_time_references('now')
        assert len(result) == 1

    def test_now_cardinality(self):
        result = parse_time_references('now')
        assert result[0].cardinality == 0

    def test_now_frame(self):
        result = parse_time_references('now')
        assert result[0].frame == 'second'

    def test_now_tense(self):
        result = parse_time_references('now')
        assert result[0].tense == 'present'

    def test_now_is_relative_time(self):
        result = parse_time_references('now')
        assert isinstance(result[0], RelativeTime)


# ============================================================================
# Group 2: Bare 'right now' -- basic attribute checks
# ============================================================================

class TestRightNowBare:
    """Bare 'right now' returns exactly one present-tense RelativeTime."""

    def test_right_now_returns_one_result(self):
        result = parse_time_references('right now')
        assert len(result) == 1

    def test_right_now_cardinality(self):
        result = parse_time_references('right now')
        assert result[0].cardinality == 0

    def test_right_now_frame(self):
        result = parse_time_references('right now')
        assert result[0].frame == 'second'

    def test_right_now_tense(self):
        result = parse_time_references('right now')
        assert result[0].tense == 'present'

    def test_right_now_is_relative_time(self):
        result = parse_time_references('right now')
        assert isinstance(result[0], RelativeTime)


# ============================================================================
# Group 3: Case insensitivity
# ============================================================================

class TestCaseInsensitivity:
    """now and right now are case-insensitive (input is lowercased)."""

    def test_NOW_uppercase(self):
        result = parse_time_references('NOW')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_Now_mixed_case(self):
        result = parse_time_references('Now')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_RIGHT_NOW_uppercase(self):
        result = parse_time_references('RIGHT NOW')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_Right_Now_mixed_case(self):
        result = parse_time_references('Right Now')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_NOW_frame(self):
        result = parse_time_references('NOW')
        assert result[0].frame == 'second'

    def test_RIGHT_NOW_frame(self):
        result = parse_time_references('RIGHT NOW')
        assert result[0].frame == 'second'


# ============================================================================
# Group 4: 'now' in phrase context -- leading non-time words
# ============================================================================

class TestNowInPhrase:
    """'now' is extracted when preceded by non-time words."""

    def test_meeting_now(self):
        result = parse_time_references('meeting now')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_do_it_now(self):
        result = parse_time_references('do it now')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_check_now(self):
        result = parse_time_references('check now')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_status_now(self):
        result = parse_time_references('status now')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_call_now(self):
        result = parse_time_references('call now')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_available_now(self):
        result = parse_time_references('available now')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_happening_now(self):
        result = parse_time_references('happening now')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_starting_now(self):
        result = parse_time_references('starting now')
        assert len(result) == 1
        assert result[0].tense == 'present'


# ============================================================================
# Group 5: 'now' in phrase context -- trailing non-time words
# ============================================================================

class TestNowTrailing:
    """'now' is extracted when followed by non-time words."""

    def test_now_please(self):
        result = parse_time_references('now please')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_now_meeting(self):
        result = parse_time_references('now meeting')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_now_call(self):
        result = parse_time_references('now call')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_now_available(self):
        result = parse_time_references('now available')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_now_starting(self):
        result = parse_time_references('now starting')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_now_or_later(self):
        result = parse_time_references('now or later')
        assert len(result) == 1
        assert result[0].tense == 'present'


# ============================================================================
# Group 6: 'right now' in phrase context -- leading non-time words
# ============================================================================

class TestRightNowInPhrase:
    """'right now' is extracted when preceded by non-time words."""

    def test_meeting_right_now(self):
        result = parse_time_references('meeting right now')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_do_it_right_now(self):
        result = parse_time_references('do it right now')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_check_right_now(self):
        result = parse_time_references('check right now')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_status_right_now(self):
        result = parse_time_references('status right now')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_call_right_now(self):
        result = parse_time_references('call right now')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_available_right_now(self):
        result = parse_time_references('available right now')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_happening_right_now(self):
        result = parse_time_references('happening right now')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_starting_right_now(self):
        result = parse_time_references('starting right now')
        assert len(result) == 1
        assert result[0].tense == 'present'


# ============================================================================
# Group 7: 'right now' in phrase context -- trailing non-time words
# ============================================================================

class TestRightNowTrailing:
    """'right now' is extracted when followed by non-time words."""

    def test_right_now_please(self):
        result = parse_time_references('right now please')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_right_now_meeting(self):
        result = parse_time_references('right now meeting')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_right_now_call(self):
        result = parse_time_references('right now call')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_right_now_available(self):
        result = parse_time_references('right now available')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_right_now_or_later(self):
        result = parse_time_references('right now or later')
        assert len(result) == 1
        assert result[0].tense == 'present'


# ============================================================================
# Group 8: has_temporal_info
# ============================================================================

class TestHasTemporalInfo:
    """has_temporal_info returns True for texts containing now/right now."""

    def test_now_has_temporal_info(self):
        assert has_temporal_info('now') is True

    def test_right_now_has_temporal_info(self):
        assert has_temporal_info('right now') is True

    def test_NOW_has_temporal_info(self):
        assert has_temporal_info('NOW') is True

    def test_RIGHT_NOW_has_temporal_info(self):
        assert has_temporal_info('RIGHT NOW') is True

    def test_meeting_now_has_temporal_info(self):
        assert has_temporal_info('meeting now') is True

    def test_meeting_right_now_has_temporal_info(self):
        assert has_temporal_info('meeting right now') is True

    def test_non_temporal_false(self):
        assert has_temporal_info('regular sentence') is False

    def test_another_non_temporal_false(self):
        assert has_temporal_info('hello world') is False


# ============================================================================
# Group 9: extract_relative_times
# ============================================================================

class TestExtractRelativeTimes:
    """extract_relative_times returns RelativeTime for now/right now."""

    def test_now_is_relative_time_instance(self):
        result = extract_relative_times('now')
        assert len(result) == 1
        assert isinstance(result[0], RelativeTime)

    def test_right_now_is_relative_time_instance(self):
        result = extract_relative_times('right now')
        assert len(result) == 1
        assert isinstance(result[0], RelativeTime)

    def test_now_frame_via_extract(self):
        result = extract_relative_times('now')
        assert result[0].frame == 'second'

    def test_right_now_frame_via_extract(self):
        result = extract_relative_times('right now')
        assert result[0].frame == 'second'

    def test_now_tense_via_extract(self):
        result = extract_relative_times('now')
        assert result[0].tense == 'present'

    def test_right_now_tense_via_extract(self):
        result = extract_relative_times('right now')
        assert result[0].tense == 'present'


# ============================================================================
# Group 10: Not a past or future reference
# ============================================================================

class TestNotPastOrFuture:
    """now/right now are present-tense and must not appear in past/future results."""

    def test_now_not_in_past(self):
        result = extract_past_references('now')
        assert len(result) == 0

    def test_right_now_not_in_past(self):
        result = extract_past_references('right now')
        assert len(result) == 0

    def test_now_not_in_future(self):
        result = extract_future_references('now')
        assert len(result) == 0

    def test_right_now_not_in_future(self):
        result = extract_future_references('right now')
        assert len(result) == 0


# ============================================================================
# Group 11: resolve_to_timedelta
# ============================================================================

class TestResolveToTimedelta:
    """resolve_to_timedelta returns timedelta(0) for now/right now."""

    def test_now_timedelta_is_timedelta(self):
        result = resolve_to_timedelta('now')
        assert len(result) == 1
        assert isinstance(result[0], timedelta)

    def test_right_now_timedelta_is_timedelta(self):
        result = resolve_to_timedelta('right now')
        assert len(result) == 1
        assert isinstance(result[0], timedelta)

    def test_now_timedelta_is_zero(self):
        """Zero cardinality present-tense = no offset."""
        result = resolve_to_timedelta('now')
        assert result[0] == timedelta(0)

    def test_right_now_timedelta_is_zero(self):
        result = resolve_to_timedelta('right now')
        assert result[0] == timedelta(0)

    def test_now_timedelta_not_negative(self):
        result = resolve_to_timedelta('now')
        assert result[0] >= timedelta(0)

    def test_right_now_timedelta_not_negative(self):
        result = resolve_to_timedelta('right now')
        assert result[0] >= timedelta(0)


# ============================================================================
# Group 12: parse_dates integration
# ============================================================================

class TestParseDatesIntegration:
    """parse_dates picks up now/right now."""

    def test_now_parse_dates_has_dates(self):
        result = parse_dates('now')
        assert result.has_dates is True

    def test_right_now_parse_dates_has_dates(self):
        result = parse_dates('right now')
        assert result.has_dates is True

    def test_now_parse_dates_relative_times(self):
        result = parse_dates('now')
        assert len(result.relative_times) == 1
        assert result.relative_times[0].frame == 'second'

    def test_right_now_parse_dates_relative_times(self):
        result = parse_dates('right now')
        assert len(result.relative_times) == 1
        assert result.relative_times[0].frame == 'second'

    def test_meeting_now_parse_dates(self):
        result = parse_dates('meeting now')
        assert result.has_dates is True
        assert result.relative_times[0].tense == 'present'

    def test_meeting_right_now_parse_dates(self):
        result = parse_dates('meeting right now')
        assert result.has_dates is True
        assert result.relative_times[0].tense == 'present'


# ============================================================================
# Group 13: Disambiguation -- 'now' inside 'X from now' patterns
# ============================================================================

class TestDisambiguation:
    """'now' inside existing patterns must not produce an extra present result."""

    def test_5_days_from_now_is_one_result(self):
        """'5 days from now' → exactly 1 result (future), not 2."""
        result = parse_time_references('5 days from now')
        assert len(result) == 1

    def test_5_days_from_now_is_future(self):
        result = parse_time_references('5 days from now')
        assert result[0].tense == 'future'

    def test_5_days_from_now_cardinality(self):
        result = parse_time_references('5 days from now')
        assert result[0].cardinality == 5

    def test_3_weeks_from_now_is_one_result(self):
        result = parse_time_references('3 weeks from now')
        assert len(result) == 1
        assert result[0].tense == 'future'

    def test_1_hour_from_now_is_one_result(self):
        result = parse_time_references('1 hour from now')
        assert len(result) == 1
        assert result[0].tense == 'future'

    def test_2_months_from_now_is_one_result(self):
        result = parse_time_references('2 months from now')
        assert len(result) == 1
        assert result[0].tense == 'future'

    def test_10_minutes_from_now_is_one_result(self):
        result = parse_time_references('10 minutes from now')
        assert len(result) == 1
        assert result[0].tense == 'future'


# ============================================================================
# Group 14: RelativeTime dataclass methods
# ============================================================================

class TestRelativeTimeDataclass:
    """RelativeTime instances built for now/right now support all methods."""

    def test_now_to_timedelta_type(self):
        rt = RelativeTime(cardinality=0, frame='second', tense='present')
        assert isinstance(rt.to_timedelta(), timedelta)

    def test_now_to_timedelta_zero(self):
        rt = RelativeTime(cardinality=0, frame='second', tense='present')
        assert rt.to_timedelta() == timedelta(0)

    def test_right_now_cardinality_zero(self):
        rt = RelativeTime(cardinality=0, frame='second', tense='present')
        assert rt.cardinality == 0

    def test_right_now_frame_second(self):
        rt = RelativeTime(cardinality=0, frame='second', tense='present')
        assert rt.frame == 'second'

    def test_right_now_tense_present(self):
        rt = RelativeTime(cardinality=0, frame='second', tense='present')
        assert rt.tense == 'present'


# ============================================================================
# Group 15: Regression -- existing patterns unaffected
# ============================================================================

class TestRegression:
    """Existing time reference patterns still work after adding now/right now."""

    def test_today_still_works(self):
        result = parse_time_references('today')
        assert len(result) == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'present'

    def test_tonight_still_works(self):
        result = parse_time_references('tonight')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_yesterday_still_works(self):
        result = parse_time_references('yesterday')
        assert len(result) == 1
        assert result[0].tense == 'past'

    def test_tomorrow_still_works(self):
        result = parse_time_references('tomorrow')
        assert len(result) == 1
        assert result[0].tense == 'future'

    def test_5_days_ago(self):
        result = parse_time_references('5 days ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].tense == 'past'

    def test_last_week(self):
        result = parse_time_references('last week')
        assert len(result) == 1
        assert result[0].tense == 'past'

    def test_next_week(self):
        result = parse_time_references('next week')
        assert len(result) == 1
        assert result[0].tense == 'future'

    def test_3_months_ago(self):
        result = parse_time_references('3 months ago')
        assert len(result) == 1
        assert result[0].cardinality == 3

    def test_2_years_from_now(self):
        result = parse_time_references('2 years from now')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].tense == 'future'

    def test_eod_still_works(self):
        result = parse_time_references('eod')
        assert len(result) == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'future'

    def test_eom_still_works(self):
        result = parse_time_references('eom')
        assert len(result) == 1
        assert result[0].frame == 'month'

    def test_eoy_still_works(self):
        result = parse_time_references('eoy')
        assert len(result) == 1
        assert result[0].frame == 'year'

    def test_this_morning_still_works(self):
        result = parse_time_references('this morning')
        assert len(result) == 1
        assert result[0].tense == 'present'

    def test_half_an_hour_ago(self):
        result = parse_time_references('half an hour ago')
        assert len(result) == 1
        assert result[0].cardinality == 30

    def test_several_days_ago(self):
        result = parse_time_references('several days ago')
        assert len(result) == 1
        assert result[0].cardinality == 3

    def test_no_temporal_info_regression(self):
        assert has_temporal_info('hello world') is False
