#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Tests for Issues #11 and #12: named weekday references.

Covers 'next <weekday>' (future) and 'last <weekday>' (past) for all 7 days,
plus abbreviations, sentence contexts, capitalization variants, and all public APIs.

Cardinality is date-dependent (1-7 days to/from target weekday), so assertions
use range checks rather than exact values.

Related GitHub Issues:
    #11 - Gap: named weekday references not supported (next friday, last monday)
          https://github.com/craigtrim/fast-parse-time/issues/11
    #12 - feat: Support forward day-of-week references (e.g. 'next Friday', 'next Monday')
          https://github.com/craigtrim/fast-parse-time/issues/12
"""

import pytest
from fast_parse_time import (
    parse_time_references,
    extract_past_references,
    extract_future_references,
    has_temporal_info,
    resolve_to_timedelta,
    parse_dates,
)
from datetime import timedelta


# =============================================================================
# Section 1: 'next <weekday>' — all 7 days, bare form
# =============================================================================

def test_next_monday_bare():
    result = parse_time_references('next monday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'
    assert 1 <= result[0].cardinality <= 7


def test_next_tuesday_bare():
    result = parse_time_references('next tuesday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'
    assert 1 <= result[0].cardinality <= 7


def test_next_wednesday_bare():
    result = parse_time_references('next wednesday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'
    assert 1 <= result[0].cardinality <= 7


def test_next_thursday_bare():
    result = parse_time_references('next thursday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'
    assert 1 <= result[0].cardinality <= 7


def test_next_friday_bare():
    result = parse_time_references('next friday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'
    assert 1 <= result[0].cardinality <= 7


def test_next_saturday_bare():
    result = parse_time_references('next saturday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'
    assert 1 <= result[0].cardinality <= 7


def test_next_sunday_bare():
    result = parse_time_references('next sunday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'
    assert 1 <= result[0].cardinality <= 7


# =============================================================================
# Section 2: 'last <weekday>' — all 7 days, bare form
# =============================================================================

def test_last_monday_bare():
    result = parse_time_references('last monday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'
    assert 1 <= result[0].cardinality <= 7


def test_last_tuesday_bare():
    result = parse_time_references('last tuesday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'
    assert 1 <= result[0].cardinality <= 7


def test_last_wednesday_bare():
    result = parse_time_references('last wednesday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'
    assert 1 <= result[0].cardinality <= 7


def test_last_thursday_bare():
    result = parse_time_references('last thursday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'
    assert 1 <= result[0].cardinality <= 7


def test_last_friday_bare():
    result = parse_time_references('last friday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'
    assert 1 <= result[0].cardinality <= 7


def test_last_saturday_bare():
    result = parse_time_references('last saturday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'
    assert 1 <= result[0].cardinality <= 7


def test_last_sunday_bare():
    result = parse_time_references('last sunday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'
    assert 1 <= result[0].cardinality <= 7


# =============================================================================
# Section 3: 'next <weekday>' — capitalization variants
# =============================================================================

def test_next_Friday_titlecase():
    result = parse_time_references('next Friday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_Next_friday_leading_cap():
    result = parse_time_references('Next friday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_Next_Friday_both_caps():
    result = parse_time_references('Next Friday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_next_FRIDAY_uppercase():
    result = parse_time_references('next FRIDAY')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_next_Monday_titlecase():
    result = parse_time_references('next Monday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_next_Wednesday_titlecase():
    result = parse_time_references('next Wednesday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_next_Sunday_titlecase():
    result = parse_time_references('next Sunday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


# =============================================================================
# Section 4: 'last <weekday>' — capitalization variants
# =============================================================================

def test_last_Friday_titlecase():
    result = parse_time_references('last Friday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_Last_friday_leading_cap():
    result = parse_time_references('Last friday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_Last_Friday_both_caps():
    result = parse_time_references('Last Friday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_last_MONDAY_uppercase():
    result = parse_time_references('last MONDAY')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_last_Monday_titlecase():
    result = parse_time_references('last Monday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_last_Wednesday_titlecase():
    result = parse_time_references('last Wednesday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_last_Sunday_titlecase():
    result = parse_time_references('last Sunday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


# =============================================================================
# Section 5: 'next <weekday>' — sentence context
# =============================================================================

def test_next_friday_in_meeting_sentence():
    result = parse_time_references('meeting next friday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_next_monday_lets_meet():
    result = parse_time_references("let's meet next monday")
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_next_tuesday_call_scheduled():
    result = parse_time_references('call scheduled next tuesday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_next_wednesday_deadline():
    result = parse_time_references('deadline is next wednesday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_next_thursday_review():
    result = parse_time_references('code review next thursday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_next_saturday_event():
    result = parse_time_references('event is next saturday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_next_sunday_brunch():
    result = parse_time_references('brunch next sunday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


# =============================================================================
# Section 6: 'last <weekday>' — sentence context
# =============================================================================

def test_last_friday_saw_it():
    result = parse_time_references('I saw it last friday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_last_monday_deployment():
    result = parse_time_references('deployment happened last monday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_last_tuesday_meeting():
    result = parse_time_references('we discussed this last tuesday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_last_wednesday_broke():
    result = parse_time_references('it broke last wednesday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_last_thursday_incident():
    result = parse_time_references('incident occurred last thursday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_last_saturday_party():
    result = parse_time_references('party was last saturday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_last_sunday_game():
    result = parse_time_references('game was last sunday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


# =============================================================================
# Section 7: 'this <weekday>' — treated as future (upcoming)
# =============================================================================

def test_this_monday():
    result = parse_time_references('this monday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'
    assert 1 <= result[0].cardinality <= 7


def test_this_tuesday():
    result = parse_time_references('this tuesday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_this_wednesday():
    result = parse_time_references('this wednesday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_this_thursday():
    result = parse_time_references('this thursday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_this_friday():
    result = parse_time_references('this friday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_this_saturday():
    result = parse_time_references('this saturday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_this_sunday():
    result = parse_time_references('this sunday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


# =============================================================================
# Section 8: 'next <abbrev>' — abbreviated day names
# =============================================================================

def test_next_mon():
    result = parse_time_references('next mon')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_next_tue():
    result = parse_time_references('next tue')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_next_wed():
    result = parse_time_references('next wed')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_next_thu():
    result = parse_time_references('next thu')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_next_fri():
    result = parse_time_references('next fri')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_next_sat():
    result = parse_time_references('next sat')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_next_sun():
    result = parse_time_references('next sun')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


# =============================================================================
# Section 9: 'last <abbrev>' — abbreviated day names
# =============================================================================

def test_last_mon():
    result = parse_time_references('last mon')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_last_tue():
    result = parse_time_references('last tue')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_last_wed():
    result = parse_time_references('last wed')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_last_thu():
    result = parse_time_references('last thu')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_last_fri():
    result = parse_time_references('last fri')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_last_sat():
    result = parse_time_references('last sat')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_last_sun():
    result = parse_time_references('last sun')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


# =============================================================================
# Section 10: has_temporal_info — next/last weekdays detected
# =============================================================================

def test_has_temporal_info_next_monday():
    assert has_temporal_info('next monday') is True


def test_has_temporal_info_next_friday():
    assert has_temporal_info('next friday') is True


def test_has_temporal_info_next_wednesday():
    assert has_temporal_info('next wednesday') is True


def test_has_temporal_info_last_monday():
    assert has_temporal_info('last monday') is True


def test_has_temporal_info_last_friday():
    assert has_temporal_info('last friday') is True


def test_has_temporal_info_last_wednesday():
    assert has_temporal_info('last wednesday') is True


def test_has_temporal_info_this_friday():
    assert has_temporal_info('this friday') is True


def test_has_temporal_info_next_fri():
    assert has_temporal_info('next fri') is True


def test_has_temporal_info_last_fri():
    assert has_temporal_info('last fri') is True


def test_has_temporal_info_no_weekday():
    assert has_temporal_info('just checking') is False


# =============================================================================
# Section 11: extract_future_references — next weekdays
# =============================================================================

def test_extract_future_next_monday():
    result = extract_future_references('next monday')
    assert len(result) == 1
    assert result[0].tense == 'future'
    assert result[0].frame == 'day'


def test_extract_future_next_tuesday():
    result = extract_future_references('next tuesday')
    assert len(result) == 1
    assert result[0].tense == 'future'


def test_extract_future_next_friday():
    result = extract_future_references('next friday')
    assert len(result) == 1
    assert result[0].tense == 'future'
    assert result[0].frame == 'day'


def test_extract_future_next_saturday():
    result = extract_future_references('next saturday')
    assert len(result) == 1
    assert result[0].tense == 'future'


def test_extract_future_this_friday():
    result = extract_future_references('this friday')
    assert len(result) == 1
    assert result[0].tense == 'future'


def test_extract_future_next_fri_abbrev():
    result = extract_future_references('next fri')
    assert len(result) == 1
    assert result[0].tense == 'future'


def test_extract_future_next_monday_in_sentence():
    result = extract_future_references('meeting next monday')
    assert len(result) == 1
    assert result[0].tense == 'future'


# =============================================================================
# Section 12: extract_past_references — last weekdays
# =============================================================================

def test_extract_past_last_monday():
    result = extract_past_references('last monday')
    assert len(result) == 1
    assert result[0].tense == 'past'
    assert result[0].frame == 'day'


def test_extract_past_last_tuesday():
    result = extract_past_references('last tuesday')
    assert len(result) == 1
    assert result[0].tense == 'past'


def test_extract_past_last_friday():
    result = extract_past_references('last friday')
    assert len(result) == 1
    assert result[0].tense == 'past'
    assert result[0].frame == 'day'


def test_extract_past_last_saturday():
    result = extract_past_references('last saturday')
    assert len(result) == 1
    assert result[0].tense == 'past'


def test_extract_past_last_fri_abbrev():
    result = extract_past_references('last fri')
    assert len(result) == 1
    assert result[0].tense == 'past'


def test_extract_past_last_monday_in_sentence():
    result = extract_past_references('deployment last monday')
    assert len(result) == 1
    assert result[0].tense == 'past'


def test_extract_past_last_wednesday_in_sentence():
    result = extract_past_references('it broke last wednesday')
    assert len(result) == 1
    assert result[0].tense == 'past'


# =============================================================================
# Section 13: Tense isolation — 'next' weekdays must NOT appear in past bucket
# =============================================================================

def test_next_monday_not_in_past():
    result = extract_past_references('next monday')
    assert len(result) == 0


def test_next_tuesday_not_in_past():
    result = extract_past_references('next tuesday')
    assert len(result) == 0


def test_next_friday_not_in_past():
    result = extract_past_references('next friday')
    assert len(result) == 0


def test_next_saturday_not_in_past():
    result = extract_past_references('next saturday')
    assert len(result) == 0


def test_this_friday_not_in_past():
    result = extract_past_references('this friday')
    assert len(result) == 0


def test_next_mon_abbrev_not_in_past():
    result = extract_past_references('next mon')
    assert len(result) == 0


def test_next_sunday_not_in_past():
    result = extract_past_references('next sunday')
    assert len(result) == 0


# =============================================================================
# Section 14: Tense isolation — 'last' weekdays must NOT appear in future bucket
# =============================================================================

def test_last_monday_not_in_future():
    result = extract_future_references('last monday')
    assert len(result) == 0


def test_last_tuesday_not_in_future():
    result = extract_future_references('last tuesday')
    assert len(result) == 0


def test_last_friday_not_in_future():
    result = extract_future_references('last friday')
    assert len(result) == 0


def test_last_saturday_not_in_future():
    result = extract_future_references('last saturday')
    assert len(result) == 0


def test_last_fri_abbrev_not_in_future():
    result = extract_future_references('last fri')
    assert len(result) == 0


def test_last_wednesday_not_in_future():
    result = extract_future_references('last wednesday')
    assert len(result) == 0


def test_last_sunday_not_in_future():
    result = extract_future_references('last sunday')
    assert len(result) == 0


# =============================================================================
# Section 15: parse_dates integrated API
# =============================================================================

def test_parse_dates_next_friday():
    result = parse_dates('meeting next friday')
    assert result.has_dates is True
    assert len(result.relative_times) == 1
    assert result.relative_times[0].frame == 'day'
    assert result.relative_times[0].tense == 'future'


def test_parse_dates_last_monday():
    result = parse_dates('deployment last monday')
    assert result.has_dates is True
    assert len(result.relative_times) == 1
    assert result.relative_times[0].frame == 'day'
    assert result.relative_times[0].tense == 'past'


def test_parse_dates_next_monday_bare():
    result = parse_dates('next monday')
    assert result.has_dates is True
    assert result.relative_times[0].tense == 'future'


def test_parse_dates_last_friday_bare():
    result = parse_dates('last friday')
    assert result.has_dates is True
    assert result.relative_times[0].tense == 'past'


def test_parse_dates_this_friday():
    result = parse_dates('this friday')
    assert result.has_dates is True
    assert result.relative_times[0].tense == 'future'


def test_parse_dates_next_wednesday():
    result = parse_dates('deadline next wednesday')
    assert result.has_dates is True
    assert result.relative_times[0].frame == 'day'
    assert result.relative_times[0].tense == 'future'


def test_parse_dates_last_thursday():
    result = parse_dates('incident last thursday')
    assert result.has_dates is True
    assert result.relative_times[0].frame == 'day'
    assert result.relative_times[0].tense == 'past'


def test_parse_dates_next_fri_abbrev():
    result = parse_dates('call next fri')
    assert result.has_dates is True
    assert result.relative_times[0].tense == 'future'


def test_parse_dates_last_fri_abbrev():
    result = parse_dates('event last fri')
    assert result.has_dates is True
    assert result.relative_times[0].tense == 'past'


# =============================================================================
# Section 16: Cardinality range validation (1-7 days)
# =============================================================================

def test_next_monday_cardinality_range():
    result = parse_time_references('next monday')
    assert 1 <= result[0].cardinality <= 7


def test_next_friday_cardinality_range():
    result = parse_time_references('next friday')
    assert 1 <= result[0].cardinality <= 7


def test_next_sunday_cardinality_range():
    result = parse_time_references('next sunday')
    assert 1 <= result[0].cardinality <= 7


def test_last_monday_cardinality_range():
    result = parse_time_references('last monday')
    assert 1 <= result[0].cardinality <= 7


def test_last_friday_cardinality_range():
    result = parse_time_references('last friday')
    assert 1 <= result[0].cardinality <= 7


def test_last_sunday_cardinality_range():
    result = parse_time_references('last sunday')
    assert 1 <= result[0].cardinality <= 7


def test_this_friday_cardinality_range():
    result = parse_time_references('this friday')
    assert 1 <= result[0].cardinality <= 7


# =============================================================================
# Section 17: resolve_to_timedelta — sign validation
# (next/this = positive, last = negative)
# =============================================================================

def test_timedelta_next_monday_positive():
    deltas = resolve_to_timedelta('next monday')
    assert len(deltas) == 1
    assert deltas[0] > timedelta(0)


def test_timedelta_next_friday_positive():
    deltas = resolve_to_timedelta('next friday')
    assert len(deltas) == 1
    assert deltas[0] > timedelta(0)


def test_timedelta_next_wednesday_positive():
    deltas = resolve_to_timedelta('next wednesday')
    assert len(deltas) == 1
    assert deltas[0] > timedelta(0)


def test_timedelta_this_friday_positive():
    deltas = resolve_to_timedelta('this friday')
    assert len(deltas) == 1
    assert deltas[0] > timedelta(0)


def test_timedelta_last_monday_negative():
    deltas = resolve_to_timedelta('last monday')
    assert len(deltas) == 1
    assert deltas[0] < timedelta(0)


def test_timedelta_last_friday_negative():
    deltas = resolve_to_timedelta('last friday')
    assert len(deltas) == 1
    assert deltas[0] < timedelta(0)


def test_timedelta_last_wednesday_negative():
    deltas = resolve_to_timedelta('last wednesday')
    assert len(deltas) == 1
    assert deltas[0] < timedelta(0)


def test_timedelta_next_friday_within_week():
    """Next friday should be at most 7 days away."""
    deltas = resolve_to_timedelta('next friday')
    assert timedelta(days=1) <= deltas[0] <= timedelta(days=7)


def test_timedelta_last_friday_within_week():
    """Last friday should be at most 7 days ago."""
    deltas = resolve_to_timedelta('last friday')
    assert timedelta(days=-7) <= deltas[0] <= timedelta(days=-1)


# =============================================================================
# Section 18: Additional sentence context variations
# =============================================================================

def test_next_friday_sentence_starts_with():
    result = parse_time_references('next friday is the deadline')
    assert len(result) == 1
    assert result[0].tense == 'future'


def test_last_monday_sentence_starts_with():
    result = parse_time_references('last monday we shipped it')
    assert len(result) == 1
    assert result[0].tense == 'past'


def test_next_tuesday_after_the():
    result = parse_time_references('report due next tuesday')
    assert len(result) == 1
    assert result[0].tense == 'future'


def test_last_thursday_after_word():
    result = parse_time_references('PR merged last thursday')
    assert len(result) == 1
    assert result[0].tense == 'past'


def test_next_saturday_long_sentence():
    result = parse_time_references('the team is going hiking next saturday morning')
    assert len(result) == 1
    assert result[0].tense == 'future'


def test_last_sunday_long_sentence():
    result = parse_time_references('the server went down last sunday evening')
    assert len(result) == 1
    assert result[0].tense == 'past'


def test_next_wednesday_with_context():
    result = parse_time_references('our sprint ends next wednesday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_last_tuesday_with_context():
    result = parse_time_references('the bug was introduced last tuesday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


# =============================================================================
# Section 19: 'past <weekday>' — alias for 'last'
# =============================================================================

def test_past_monday():
    result = parse_time_references('past monday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_past_friday():
    result = parse_time_references('past friday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_past_wednesday():
    result = parse_time_references('past wednesday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_past_tuesday():
    result = parse_time_references('past tuesday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_past_thursday():
    result = parse_time_references('past thursday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_past_saturday():
    result = parse_time_references('past saturday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_past_sunday():
    result = parse_time_references('past sunday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


# =============================================================================
# Section 20: Regression — existing 'next week' / 'last week' still work
# (weekday additions must not break existing generic week patterns)
# =============================================================================

def test_regression_next_week():
    result = parse_time_references('next week')
    assert len(result) == 1
    assert result[0].frame == 'week'
    assert result[0].tense == 'future'


def test_regression_last_week():
    result = parse_time_references('last week')
    assert len(result) == 1
    assert result[0].frame == 'week'
    assert result[0].tense == 'past'


def test_regression_next_month():
    result = parse_time_references('next month')
    assert len(result) == 1
    assert result[0].frame == 'month'
    assert result[0].tense == 'future'


def test_regression_last_month():
    result = parse_time_references('last month')
    assert len(result) == 1
    assert result[0].frame == 'month'
    assert result[0].tense == 'past'


def test_regression_next_year():
    result = parse_time_references('next year')
    assert len(result) == 1
    assert result[0].frame == 'year'
    assert result[0].tense == 'future'


def test_regression_yesterday():
    result = parse_time_references('yesterday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_regression_tomorrow():
    result = parse_time_references('tomorrow')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


# =============================================================================
# Section 21: 'coming <weekday>' — forward-looking alias
# =============================================================================

def test_coming_friday():
    result = parse_time_references('coming friday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_coming_monday():
    result = parse_time_references('coming monday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_coming_tuesday():
    result = parse_time_references('coming tuesday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_coming_wednesday():
    result = parse_time_references('coming wednesday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_coming_thursday():
    result = parse_time_references('coming thursday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_coming_saturday():
    result = parse_time_references('coming saturday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_coming_sunday():
    result = parse_time_references('coming sunday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


# =============================================================================
# Section 22: Additional has_temporal_info coverage
# =============================================================================

def test_has_temporal_info_this_monday():
    assert has_temporal_info('this monday') is True


def test_has_temporal_info_last_thursday():
    assert has_temporal_info('last thursday') is True


def test_has_temporal_info_next_sat():
    assert has_temporal_info('next sat') is True


def test_has_temporal_info_last_sat():
    assert has_temporal_info('last sat') is True


def test_has_temporal_info_coming_friday():
    assert has_temporal_info('coming friday') is True


def test_has_temporal_info_past_tuesday():
    assert has_temporal_info('past tuesday') is True


def test_has_temporal_info_next_thu():
    assert has_temporal_info('next thu') is True


def test_has_temporal_info_last_wed():
    assert has_temporal_info('last wed') is True


# =============================================================================
# Section 23: Frame is always 'day' for all weekday forms
# =============================================================================

def test_frame_day_next_monday():
    assert parse_time_references('next monday')[0].frame == 'day'


def test_frame_day_last_monday():
    assert parse_time_references('last monday')[0].frame == 'day'


def test_frame_day_next_friday():
    assert parse_time_references('next friday')[0].frame == 'day'


def test_frame_day_last_friday():
    assert parse_time_references('last friday')[0].frame == 'day'


def test_frame_day_this_wednesday():
    assert parse_time_references('this wednesday')[0].frame == 'day'


def test_frame_day_coming_saturday():
    assert parse_time_references('coming saturday')[0].frame == 'day'


def test_frame_day_past_thursday():
    assert parse_time_references('past thursday')[0].frame == 'day'


def test_frame_day_next_sun_abbrev():
    assert parse_time_references('next sun')[0].frame == 'day'


def test_frame_day_last_mon_abbrev():
    assert parse_time_references('last mon')[0].frame == 'day'


# =============================================================================
# Section 24: Extended abbreviations (tues, weds, thurs)
# =============================================================================

def test_next_tues():
    result = parse_time_references('next tues')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_last_tues():
    result = parse_time_references('last tues')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_next_weds():
    result = parse_time_references('next weds')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_last_weds():
    result = parse_time_references('last weds')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


def test_next_thurs():
    result = parse_time_references('next thurs')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'future'


def test_last_thurs():
    result = parse_time_references('last thurs')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'


# =============================================================================
# Section 25: Result count — exactly one result per weekday expression
# =============================================================================

def test_exactly_one_result_next_monday():
    assert len(parse_time_references('next monday')) == 1


def test_exactly_one_result_next_tuesday():
    assert len(parse_time_references('next tuesday')) == 1


def test_exactly_one_result_next_wednesday():
    assert len(parse_time_references('next wednesday')) == 1


def test_exactly_one_result_next_thursday():
    assert len(parse_time_references('next thursday')) == 1


def test_exactly_one_result_next_saturday():
    assert len(parse_time_references('next saturday')) == 1


def test_exactly_one_result_last_tuesday():
    assert len(parse_time_references('last tuesday')) == 1


def test_exactly_one_result_last_thursday():
    assert len(parse_time_references('last thursday')) == 1


def test_exactly_one_result_last_saturday():
    assert len(parse_time_references('last saturday')) == 1


# =============================================================================
# Section 26: Upcoming/next + abbrev in sentence context
# =============================================================================

def test_next_fri_sentence():
    result = parse_time_references('call is next fri')
    assert len(result) == 1
    assert result[0].tense == 'future'


def test_last_fri_sentence():
    result = parse_time_references('shipped last fri')
    assert len(result) == 1
    assert result[0].tense == 'past'


def test_next_mon_sentence():
    result = parse_time_references('standup next mon')
    assert len(result) == 1
    assert result[0].tense == 'future'


def test_last_wed_sentence():
    result = parse_time_references('merged last wed')
    assert len(result) == 1
    assert result[0].tense == 'past'


def test_next_thu_sentence():
    result = parse_time_references('retro next thu')
    assert len(result) == 1
    assert result[0].tense == 'future'


def test_last_thu_sentence():
    result = parse_time_references('deployed last thu')
    assert len(result) == 1
    assert result[0].tense == 'past'


def test_next_sat_sentence():
    result = parse_time_references('release party next sat')
    assert len(result) == 1
    assert result[0].tense == 'future'


# =============================================================================
# Section 27: Timedelta sign — all remaining days
# =============================================================================

def test_timedelta_next_tuesday_positive():
    deltas = resolve_to_timedelta('next tuesday')
    assert len(deltas) == 1
    assert deltas[0] > timedelta(0)


def test_timedelta_next_thursday_positive():
    deltas = resolve_to_timedelta('next thursday')
    assert len(deltas) == 1
    assert deltas[0] > timedelta(0)


def test_timedelta_next_saturday_positive():
    deltas = resolve_to_timedelta('next saturday')
    assert len(deltas) == 1
    assert deltas[0] > timedelta(0)


def test_timedelta_next_sunday_positive():
    deltas = resolve_to_timedelta('next sunday')
    assert len(deltas) == 1
    assert deltas[0] > timedelta(0)


def test_timedelta_last_tuesday_negative():
    deltas = resolve_to_timedelta('last tuesday')
    assert len(deltas) == 1
    assert deltas[0] < timedelta(0)


def test_timedelta_last_thursday_negative():
    deltas = resolve_to_timedelta('last thursday')
    assert len(deltas) == 1
    assert deltas[0] < timedelta(0)


def test_timedelta_last_saturday_negative():
    deltas = resolve_to_timedelta('last saturday')
    assert len(deltas) == 1
    assert deltas[0] < timedelta(0)


def test_timedelta_last_sunday_negative():
    deltas = resolve_to_timedelta('last sunday')
    assert len(deltas) == 1
    assert deltas[0] < timedelta(0)
