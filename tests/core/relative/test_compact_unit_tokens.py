#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Tests for Issue #57: Support compact number+letter unit tokens (1d, 2y) in relative time parsing.

Compact tokens fuse numeric cardinality with single-letter unit abbreviations:
    '1d ago'  → RelativeTime(1, 'day', 'past')
    '2y ago'  → RelativeTime(2, 'year', 'past')
    '5h'      → RelativeTime(5, 'hour', 'past')  # implicit past

Supported compact forms:
    - d  → day
    - w  → week
    - mo → month
    - m  → month (where unambiguous)
    - y  → year
    - h  → hour
    - min → minute
    - s  → second

All tests MUST FAIL before implementation begins (TDD Phase 1).

Related GitHub Issue:
    #57 - Support compact number+letter unit tokens (1d, 2y) in relative time parsing
    https://github.com/craigtrim/fast-parse-time/issues/57
"""

import pytest
from fast_parse_time import (
    parse_time_references,
    extract_relative_times,
    extract_past_references,
    extract_future_references,
)


# =============================================================================
# Section 1: Days (Nd) with 'ago' — cardinalities 1-30
# =============================================================================

def test_1d_ago_returns_one_result():
    result = parse_time_references('1d ago')
    assert len(result) == 1

def test_1d_ago_frame_is_day():
    result = parse_time_references('1d ago')
    assert result[0].frame == 'day'

def test_1d_ago_cardinality_is_1():
    result = parse_time_references('1d ago')
    assert result[0].cardinality == 1

def test_1d_ago_tense_is_past():
    result = parse_time_references('1d ago')
    assert result[0].tense == 'past'

def test_2d_ago():
    result = parse_time_references('2d ago')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].cardinality == 2

def test_3d_ago():
    result = parse_time_references('3d ago')
    assert len(result) == 1
    assert result[0].cardinality == 3

def test_4d_ago():
    result = parse_time_references('4d ago')
    assert result[0].cardinality == 4

def test_5d_ago():
    result = parse_time_references('5d ago')
    assert result[0].cardinality == 5

def test_6d_ago():
    result = parse_time_references('6d ago')
    assert result[0].cardinality == 6

def test_7d_ago():
    result = parse_time_references('7d ago')
    assert result[0].cardinality == 7

def test_8d_ago():
    result = parse_time_references('8d ago')
    assert result[0].cardinality == 8

def test_9d_ago():
    result = parse_time_references('9d ago')
    assert result[0].cardinality == 9

def test_10d_ago():
    result = parse_time_references('10d ago')
    assert result[0].cardinality == 10

def test_15d_ago():
    result = parse_time_references('15d ago')
    assert result[0].cardinality == 15

def test_20d_ago():
    result = parse_time_references('20d ago')
    assert result[0].cardinality == 20

def test_25d_ago():
    result = parse_time_references('25d ago')
    assert result[0].cardinality == 25

def test_30d_ago():
    result = parse_time_references('30d ago')
    assert result[0].cardinality == 30


# =============================================================================
# Section 2: Days (Nd) without 'ago' — implicit past tense
# =============================================================================

def test_1d_implicit_past_returns_result():
    result = parse_time_references('1d')
    assert len(result) == 1

def test_1d_implicit_past_tense_is_past():
    result = parse_time_references('1d')
    assert result[0].tense == 'past'

def test_1d_implicit_past_frame_is_day():
    result = parse_time_references('1d')
    assert result[0].frame == 'day'

def test_2d_implicit_past():
    result = parse_time_references('2d')
    assert len(result) == 1
    assert result[0].tense == 'past'

def test_5d_implicit_past():
    result = parse_time_references('5d')
    assert result[0].cardinality == 5

def test_10d_implicit_past():
    result = parse_time_references('10d')
    assert result[0].cardinality == 10


# =============================================================================
# Section 3: Weeks (Nw) with 'ago'
# =============================================================================

def test_1w_ago_returns_one_result():
    result = parse_time_references('1w ago')
    assert len(result) == 1

def test_1w_ago_frame_is_week():
    result = parse_time_references('1w ago')
    assert result[0].frame == 'week'

def test_1w_ago_cardinality_is_1():
    result = parse_time_references('1w ago')
    assert result[0].cardinality == 1

def test_1w_ago_tense_is_past():
    result = parse_time_references('1w ago')
    assert result[0].tense == 'past'

def test_2w_ago():
    result = parse_time_references('2w ago')
    assert result[0].cardinality == 2

def test_3w_ago():
    result = parse_time_references('3w ago')
    assert result[0].cardinality == 3

def test_4w_ago():
    result = parse_time_references('4w ago')
    assert result[0].cardinality == 4

def test_5w_ago():
    result = parse_time_references('5w ago')
    assert result[0].cardinality == 5

def test_10w_ago():
    result = parse_time_references('10w ago')
    assert result[0].cardinality == 10

def test_20w_ago():
    result = parse_time_references('20w ago')
    assert result[0].cardinality == 20


# =============================================================================
# Section 4: Weeks (Nw) without 'ago' — implicit past
# =============================================================================

def test_1w_implicit_past():
    result = parse_time_references('1w')
    assert len(result) == 1
    assert result[0].tense == 'past'

def test_2w_implicit_past():
    result = parse_time_references('2w')
    assert result[0].cardinality == 2

def test_5w_implicit_past():
    result = parse_time_references('5w')
    assert result[0].cardinality == 5


# =============================================================================
# Section 5: Months (Nmo) with 'ago'
# =============================================================================

def test_1mo_ago_returns_one_result():
    result = parse_time_references('1mo ago')
    assert len(result) == 1

def test_1mo_ago_frame_is_month():
    result = parse_time_references('1mo ago')
    assert result[0].frame == 'month'

def test_1mo_ago_cardinality_is_1():
    result = parse_time_references('1mo ago')
    assert result[0].cardinality == 1

def test_1mo_ago_tense_is_past():
    result = parse_time_references('1mo ago')
    assert result[0].tense == 'past'

def test_2mo_ago():
    result = parse_time_references('2mo ago')
    assert result[0].cardinality == 2

def test_3mo_ago():
    result = parse_time_references('3mo ago')
    assert result[0].cardinality == 3

def test_6mo_ago():
    result = parse_time_references('6mo ago')
    assert result[0].cardinality == 6

def test_12mo_ago():
    result = parse_time_references('12mo ago')
    assert result[0].cardinality == 12

def test_18mo_ago():
    result = parse_time_references('18mo ago')
    assert result[0].cardinality == 18


# =============================================================================
# Section 6: Months (Nm) with 'ago' — using 'm' instead of 'mo'
# =============================================================================

def test_1m_ago_returns_one_result():
    result = parse_time_references('1m ago')
    assert len(result) == 1

def test_1m_ago_frame_is_month():
    result = parse_time_references('1m ago')
    assert result[0].frame == 'month'

def test_2m_ago():
    result = parse_time_references('2m ago')
    assert result[0].cardinality == 2

def test_3m_ago():
    result = parse_time_references('3m ago')
    assert result[0].cardinality == 3

def test_6m_ago():
    result = parse_time_references('6m ago')
    assert result[0].cardinality == 6


# =============================================================================
# Section 7: Years (Ny) with 'ago'
# =============================================================================

def test_1y_ago_returns_one_result():
    result = parse_time_references('1y ago')
    assert len(result) == 1

def test_1y_ago_frame_is_year():
    result = parse_time_references('1y ago')
    assert result[0].frame == 'year'

def test_1y_ago_cardinality_is_1():
    result = parse_time_references('1y ago')
    assert result[0].cardinality == 1

def test_1y_ago_tense_is_past():
    result = parse_time_references('1y ago')
    assert result[0].tense == 'past'

def test_2y_ago():
    result = parse_time_references('2y ago')
    assert result[0].cardinality == 2

def test_3y_ago():
    result = parse_time_references('3y ago')
    assert result[0].cardinality == 3

def test_5y_ago():
    result = parse_time_references('5y ago')
    assert result[0].cardinality == 5

def test_10y_ago():
    result = parse_time_references('10y ago')
    assert result[0].cardinality == 10

def test_20y_ago():
    result = parse_time_references('20y ago')
    assert result[0].cardinality == 20


# =============================================================================
# Section 8: Years (Ny) without 'ago' — implicit past
# =============================================================================

def test_1y_implicit_past():
    result = parse_time_references('1y')
    assert len(result) == 1
    assert result[0].tense == 'past'

def test_2y_implicit_past():
    result = parse_time_references('2y')
    assert result[0].cardinality == 2

def test_5y_implicit_past():
    result = parse_time_references('5y')
    assert result[0].cardinality == 5


# =============================================================================
# Section 9: Hours (Nh) with 'ago'
# =============================================================================

def test_1h_ago_returns_one_result():
    result = parse_time_references('1h ago')
    assert len(result) == 1

def test_1h_ago_frame_is_hour():
    result = parse_time_references('1h ago')
    assert result[0].frame == 'hour'

def test_1h_ago_cardinality_is_1():
    result = parse_time_references('1h ago')
    assert result[0].cardinality == 1

def test_1h_ago_tense_is_past():
    result = parse_time_references('1h ago')
    assert result[0].tense == 'past'

def test_2h_ago():
    result = parse_time_references('2h ago')
    assert result[0].cardinality == 2

def test_3h_ago():
    result = parse_time_references('3h ago')
    assert result[0].cardinality == 3

def test_5h_ago():
    result = parse_time_references('5h ago')
    assert result[0].cardinality == 5

def test_12h_ago():
    result = parse_time_references('12h ago')
    assert result[0].cardinality == 12

def test_24h_ago():
    result = parse_time_references('24h ago')
    assert result[0].cardinality == 24

def test_48h_ago():
    result = parse_time_references('48h ago')
    assert result[0].cardinality == 48


# =============================================================================
# Section 10: Hours (Nh) without 'ago' — implicit past
# =============================================================================

def test_1h_implicit_past():
    result = parse_time_references('1h')
    assert len(result) == 1
    assert result[0].tense == 'past'

def test_2h_implicit_past():
    result = parse_time_references('2h')
    assert result[0].cardinality == 2

def test_5h_implicit_past():
    result = parse_time_references('5h')
    assert result[0].cardinality == 5


# =============================================================================
# Section 11: Minutes (Nmin) with 'ago'
# =============================================================================

def test_1min_ago_returns_one_result():
    result = parse_time_references('1min ago')
    assert len(result) == 1

def test_1min_ago_frame_is_minute():
    result = parse_time_references('1min ago')
    assert result[0].frame == 'minute'

def test_1min_ago_cardinality_is_1():
    result = parse_time_references('1min ago')
    assert result[0].cardinality == 1

def test_1min_ago_tense_is_past():
    result = parse_time_references('1min ago')
    assert result[0].tense == 'past'

def test_5min_ago():
    result = parse_time_references('5min ago')
    assert result[0].cardinality == 5

def test_10min_ago():
    result = parse_time_references('10min ago')
    assert result[0].cardinality == 10

def test_15min_ago():
    result = parse_time_references('15min ago')
    assert result[0].cardinality == 15

def test_30min_ago():
    result = parse_time_references('30min ago')
    assert result[0].cardinality == 30

def test_45min_ago():
    result = parse_time_references('45min ago')
    assert result[0].cardinality == 45

def test_60min_ago():
    result = parse_time_references('60min ago')
    assert result[0].cardinality == 60


# =============================================================================
# Section 12: Minutes (Nmin) without 'ago' — implicit past
# =============================================================================

def test_1min_implicit_past():
    result = parse_time_references('1min')
    assert len(result) == 1
    assert result[0].tense == 'past'

def test_5min_implicit_past():
    result = parse_time_references('5min')
    assert result[0].cardinality == 5

def test_10min_implicit_past():
    result = parse_time_references('10min')
    assert result[0].cardinality == 10


# =============================================================================
# Section 13: Seconds (Ns) with 'ago'
# =============================================================================

def test_1s_ago_returns_one_result():
    result = parse_time_references('1s ago')
    assert len(result) == 1

def test_1s_ago_frame_is_second():
    result = parse_time_references('1s ago')
    assert result[0].frame == 'second'

def test_1s_ago_cardinality_is_1():
    result = parse_time_references('1s ago')
    assert result[0].cardinality == 1

def test_1s_ago_tense_is_past():
    result = parse_time_references('1s ago')
    assert result[0].tense == 'past'

def test_5s_ago():
    result = parse_time_references('5s ago')
    assert result[0].cardinality == 5

def test_10s_ago():
    result = parse_time_references('10s ago')
    assert result[0].cardinality == 10

def test_30s_ago():
    result = parse_time_references('30s ago')
    assert result[0].cardinality == 30

def test_60s_ago():
    result = parse_time_references('60s ago')
    assert result[0].cardinality == 60


# =============================================================================
# Section 14: Seconds (Ns) without 'ago' — implicit past
# =============================================================================

def test_1s_implicit_past():
    result = parse_time_references('1s')
    assert len(result) == 1
    assert result[0].tense == 'past'

def test_5s_implicit_past():
    result = parse_time_references('5s')
    assert result[0].cardinality == 5

def test_30s_implicit_past():
    result = parse_time_references('30s')
    assert result[0].cardinality == 30


# =============================================================================
# Section 15: Sentence embedding — days
# =============================================================================

def test_posted_3d_ago():
    result = parse_time_references('posted 3d ago')
    assert len(result) == 1
    assert result[0].cardinality == 3
    assert result[0].frame == 'day'

def test_updated_5d_ago():
    result = parse_time_references('updated 5d ago')
    assert result[0].cardinality == 5

def test_cached_1d_ago():
    result = parse_time_references('cached 1d ago')
    assert result[0].cardinality == 1

def test_modified_7d_ago():
    result = parse_time_references('modified 7d ago')
    assert result[0].cardinality == 7


# =============================================================================
# Section 16: Sentence embedding — weeks
# =============================================================================

def test_posted_2w_ago():
    result = parse_time_references('posted 2w ago')
    assert len(result) == 1
    assert result[0].cardinality == 2
    assert result[0].frame == 'week'

def test_updated_3w_ago():
    result = parse_time_references('updated 3w ago')
    assert result[0].cardinality == 3

def test_filed_1w_ago():
    result = parse_time_references('filed 1w ago')
    assert result[0].cardinality == 1


# =============================================================================
# Section 17: Sentence embedding — months
# =============================================================================

def test_posted_6mo_ago():
    result = parse_time_references('posted 6mo ago')
    assert len(result) == 1
    assert result[0].cardinality == 6
    assert result[0].frame == 'month'

def test_updated_3mo_ago():
    result = parse_time_references('updated 3mo ago')
    assert result[0].cardinality == 3

def test_filed_1mo_ago():
    result = parse_time_references('filed 1mo ago')
    assert result[0].cardinality == 1


# =============================================================================
# Section 18: Sentence embedding — years
# =============================================================================

def test_filed_1y_ago():
    result = parse_time_references('filed 1y ago')
    assert len(result) == 1
    assert result[0].cardinality == 1
    assert result[0].frame == 'year'

def test_created_2y_ago():
    result = parse_time_references('created 2y ago')
    assert result[0].cardinality == 2

def test_archived_5y_ago():
    result = parse_time_references('archived 5y ago')
    assert result[0].cardinality == 5


# =============================================================================
# Section 19: Sentence embedding — hours
# =============================================================================

def test_posted_3h_ago():
    result = parse_time_references('posted 3h ago')
    assert len(result) == 1
    assert result[0].cardinality == 3
    assert result[0].frame == 'hour'

def test_updated_12h_ago():
    result = parse_time_references('updated 12h ago')
    assert result[0].cardinality == 12


# =============================================================================
# Section 20: Sentence embedding — minutes
# =============================================================================

def test_posted_15min_ago():
    result = parse_time_references('posted 15min ago')
    assert len(result) == 1
    assert result[0].cardinality == 15
    assert result[0].frame == 'minute'

def test_updated_30min_ago():
    result = parse_time_references('updated 30min ago')
    assert result[0].cardinality == 30


# =============================================================================
# Section 21: Sentence embedding — seconds
# =============================================================================

def test_posted_30s_ago():
    result = parse_time_references('posted 30s ago')
    assert len(result) == 1
    assert result[0].cardinality == 30
    assert result[0].frame == 'second'

def test_updated_60s_ago():
    result = parse_time_references('updated 60s ago')
    assert result[0].cardinality == 60


# =============================================================================
# Section 22: Mixed case — uppercase
# =============================================================================

def test_1D_ago_uppercase():
    result = parse_time_references('1D ago')
    assert len(result) == 1
    assert result[0].frame == 'day'

def test_2W_ago_uppercase():
    result = parse_time_references('2W ago')
    assert len(result) == 1
    assert result[0].frame == 'week'

def test_3MO_ago_uppercase():
    result = parse_time_references('3MO ago')
    assert len(result) == 1
    assert result[0].frame == 'month'

def test_2Y_ago_uppercase():
    result = parse_time_references('2Y ago')
    assert len(result) == 1
    assert result[0].frame == 'year'

def test_5H_ago_uppercase():
    result = parse_time_references('5H ago')
    assert len(result) == 1
    assert result[0].frame == 'hour'

def test_10MIN_ago_uppercase():
    result = parse_time_references('10MIN ago')
    assert len(result) == 1
    assert result[0].frame == 'minute'

def test_30S_ago_uppercase():
    result = parse_time_references('30S ago')
    assert len(result) == 1
    assert result[0].frame == 'second'


# =============================================================================
# Section 23: Mixed case — mixed
# =============================================================================

def test_1D_ago_capital_d():
    result = parse_time_references('1D ago')
    assert result[0].cardinality == 1

def test_2w_ago_lowercase_w():
    result = parse_time_references('2w ago')
    assert result[0].cardinality == 2

def test_3Mo_ago_capital_M():
    result = parse_time_references('3Mo ago')
    assert result[0].cardinality == 3


# =============================================================================
# Section 24: Large cardinalities
# =============================================================================

def test_50d_ago():
    result = parse_time_references('50d ago')
    assert result[0].cardinality == 50

def test_99d_ago():
    result = parse_time_references('99d ago')
    assert result[0].cardinality == 99

def test_100d_ago():
    result = parse_time_references('100d ago')
    assert result[0].cardinality == 100

def test_365d_ago():
    result = parse_time_references('365d ago')
    assert result[0].cardinality == 365

def test_1000d_ago():
    result = parse_time_references('1000d ago')
    assert result[0].cardinality == 1000


# =============================================================================
# Section 25: Negative cases — must NOT match (should return empty)
# =============================================================================

def test_d_ago_no_number_returns_empty():
    result = parse_time_references('d ago')
    assert len(result) == 0

def test_w_ago_no_number_returns_empty():
    result = parse_time_references('w ago')
    assert len(result) == 0

def test_mo_ago_no_number_returns_empty():
    result = parse_time_references('mo ago')
    assert len(result) == 0

def test_y_ago_no_number_returns_empty():
    result = parse_time_references('y ago')
    assert len(result) == 0

def test_h_ago_no_number_returns_empty():
    result = parse_time_references('h ago')
    assert len(result) == 0

def test_min_ago_no_number_returns_empty():
    result = parse_time_references('min ago')
    assert len(result) == 0

def test_s_ago_no_number_returns_empty():
    result = parse_time_references('s ago')
    assert len(result) == 0

def test_ad_ago_non_numeric_prefix():
    result = parse_time_references('ad ago')
    assert len(result) == 0

def test_xd_ago_non_numeric_prefix():
    result = parse_time_references('xd ago')
    assert len(result) == 0


# =============================================================================
# Section 26: Zero cardinality — must NOT match
# =============================================================================

def test_0d_ago_returns_empty():
    result = parse_time_references('0d ago')
    assert len(result) == 0

def test_0w_ago_returns_empty():
    result = parse_time_references('0w ago')
    assert len(result) == 0

def test_0mo_ago_returns_empty():
    result = parse_time_references('0mo ago')
    assert len(result) == 0

def test_0y_ago_returns_empty():
    result = parse_time_references('0y ago')
    assert len(result) == 0


# =============================================================================
# Section 27: Ambiguity guards — compact token should NOT match in certain contexts
# =============================================================================

def test_1d_in_date_context_2024_1d():
    """The '1d' in '2024-1d' should not be extracted as a compact token."""
    result = parse_time_references('2024-1d')
    # Should either return empty or return something OTHER than a day compact token
    # For this test, we check that if there's a result, it's not a compact 'd' token
    if len(result) > 0:
        assert not (result[0].frame == 'day' and result[0].cardinality == 1)


# =============================================================================
# Section 28: Extract APIs — extract_relative_times
# =============================================================================

def test_extract_relative_times_1d_ago():
    result = extract_relative_times('1d ago')
    assert len(result) == 1
    assert result[0].frame == 'day'

def test_extract_relative_times_2w_ago():
    result = extract_relative_times('2w ago')
    assert len(result) == 1
    assert result[0].frame == 'week'


# =============================================================================
# Section 29: Extract APIs — extract_past_references
# =============================================================================

def test_extract_past_references_3d_ago():
    result = extract_past_references('3d ago')
    assert len(result) == 1
    assert result[0].cardinality == 3

def test_extract_past_references_5h():
    result = extract_past_references('5h')
    assert len(result) == 1
    assert result[0].cardinality == 5


# =============================================================================
# Section 30: Numeric range coverage — days 1-30
# =============================================================================

def test_11d_ago():
    result = parse_time_references('11d ago')
    assert result[0].cardinality == 11

def test_12d_ago():
    result = parse_time_references('12d ago')
    assert result[0].cardinality == 12

def test_13d_ago():
    result = parse_time_references('13d ago')
    assert result[0].cardinality == 13

def test_14d_ago():
    result = parse_time_references('14d ago')
    assert result[0].cardinality == 14

def test_16d_ago():
    result = parse_time_references('16d ago')
    assert result[0].cardinality == 16

def test_17d_ago():
    result = parse_time_references('17d ago')
    assert result[0].cardinality == 17

def test_18d_ago():
    result = parse_time_references('18d ago')
    assert result[0].cardinality == 18

def test_19d_ago():
    result = parse_time_references('19d ago')
    assert result[0].cardinality == 19

def test_21d_ago():
    result = parse_time_references('21d ago')
    assert result[0].cardinality == 21

def test_22d_ago():
    result = parse_time_references('22d ago')
    assert result[0].cardinality == 22

def test_23d_ago():
    result = parse_time_references('23d ago')
    assert result[0].cardinality == 23

def test_24d_ago():
    result = parse_time_references('24d ago')
    assert result[0].cardinality == 24

def test_26d_ago():
    result = parse_time_references('26d ago')
    assert result[0].cardinality == 26

def test_27d_ago():
    result = parse_time_references('27d ago')
    assert result[0].cardinality == 27

def test_28d_ago():
    result = parse_time_references('28d ago')
    assert result[0].cardinality == 28

def test_29d_ago():
    result = parse_time_references('29d ago')
    assert result[0].cardinality == 29


# =============================================================================
# Section 31: Numeric range coverage — weeks 1-20
# =============================================================================

def test_6w_ago():
    result = parse_time_references('6w ago')
    assert result[0].cardinality == 6

def test_7w_ago():
    result = parse_time_references('7w ago')
    assert result[0].cardinality == 7

def test_8w_ago():
    result = parse_time_references('8w ago')
    assert result[0].cardinality == 8

def test_9w_ago():
    result = parse_time_references('9w ago')
    assert result[0].cardinality == 9

def test_11w_ago():
    result = parse_time_references('11w ago')
    assert result[0].cardinality == 11

def test_12w_ago():
    result = parse_time_references('12w ago')
    assert result[0].cardinality == 12

def test_15w_ago():
    result = parse_time_references('15w ago')
    assert result[0].cardinality == 15


# =============================================================================
# Section 32: Numeric range coverage — months 1-18
# =============================================================================

def test_4mo_ago():
    result = parse_time_references('4mo ago')
    assert result[0].cardinality == 4

def test_5mo_ago():
    result = parse_time_references('5mo ago')
    assert result[0].cardinality == 5

def test_7mo_ago():
    result = parse_time_references('7mo ago')
    assert result[0].cardinality == 7

def test_8mo_ago():
    result = parse_time_references('8mo ago')
    assert result[0].cardinality == 8

def test_9mo_ago():
    result = parse_time_references('9mo ago')
    assert result[0].cardinality == 9

def test_10mo_ago():
    result = parse_time_references('10mo ago')
    assert result[0].cardinality == 10

def test_11mo_ago():
    result = parse_time_references('11mo ago')
    assert result[0].cardinality == 11

def test_13mo_ago():
    result = parse_time_references('13mo ago')
    assert result[0].cardinality == 13

def test_14mo_ago():
    result = parse_time_references('14mo ago')
    assert result[0].cardinality == 14

def test_15mo_ago():
    result = parse_time_references('15mo ago')
    assert result[0].cardinality == 15

def test_16mo_ago():
    result = parse_time_references('16mo ago')
    assert result[0].cardinality == 16

def test_17mo_ago():
    result = parse_time_references('17mo ago')
    assert result[0].cardinality == 17


# =============================================================================
# Section 33: Numeric range coverage — years 1-20
# =============================================================================

def test_4y_ago():
    result = parse_time_references('4y ago')
    assert result[0].cardinality == 4

def test_6y_ago():
    result = parse_time_references('6y ago')
    assert result[0].cardinality == 6

def test_7y_ago():
    result = parse_time_references('7y ago')
    assert result[0].cardinality == 7

def test_8y_ago():
    result = parse_time_references('8y ago')
    assert result[0].cardinality == 8

def test_9y_ago():
    result = parse_time_references('9y ago')
    assert result[0].cardinality == 9

def test_11y_ago():
    result = parse_time_references('11y ago')
    assert result[0].cardinality == 11

def test_12y_ago():
    result = parse_time_references('12y ago')
    assert result[0].cardinality == 12

def test_15y_ago():
    result = parse_time_references('15y ago')
    assert result[0].cardinality == 15


# =============================================================================
# Section 34: Numeric range coverage — hours 1-48
# =============================================================================

def test_4h_ago():
    result = parse_time_references('4h ago')
    assert result[0].cardinality == 4

def test_6h_ago():
    result = parse_time_references('6h ago')
    assert result[0].cardinality == 6

def test_7h_ago():
    result = parse_time_references('7h ago')
    assert result[0].cardinality == 7

def test_8h_ago():
    result = parse_time_references('8h ago')
    assert result[0].cardinality == 8

def test_9h_ago():
    result = parse_time_references('9h ago')
    assert result[0].cardinality == 9

def test_10h_ago():
    result = parse_time_references('10h ago')
    assert result[0].cardinality == 10

def test_11h_ago():
    result = parse_time_references('11h ago')
    assert result[0].cardinality == 11

def test_13h_ago():
    result = parse_time_references('13h ago')
    assert result[0].cardinality == 13

def test_14h_ago():
    result = parse_time_references('14h ago')
    assert result[0].cardinality == 14

def test_15h_ago():
    result = parse_time_references('15h ago')
    assert result[0].cardinality == 15

def test_16h_ago():
    result = parse_time_references('16h ago')
    assert result[0].cardinality == 16

def test_18h_ago():
    result = parse_time_references('18h ago')
    assert result[0].cardinality == 18

def test_20h_ago():
    result = parse_time_references('20h ago')
    assert result[0].cardinality == 20

def test_36h_ago():
    result = parse_time_references('36h ago')
    assert result[0].cardinality == 36


# =============================================================================
# Section 35: Numeric range coverage — minutes 1-60
# =============================================================================

def test_2min_ago():
    result = parse_time_references('2min ago')
    assert result[0].cardinality == 2

def test_3min_ago():
    result = parse_time_references('3min ago')
    assert result[0].cardinality == 3

def test_4min_ago():
    result = parse_time_references('4min ago')
    assert result[0].cardinality == 4

def test_6min_ago():
    result = parse_time_references('6min ago')
    assert result[0].cardinality == 6

def test_7min_ago():
    result = parse_time_references('7min ago')
    assert result[0].cardinality == 7

def test_8min_ago():
    result = parse_time_references('8min ago')
    assert result[0].cardinality == 8

def test_9min_ago():
    result = parse_time_references('9min ago')
    assert result[0].cardinality == 9

def test_20min_ago():
    result = parse_time_references('20min ago')
    assert result[0].cardinality == 20

def test_25min_ago():
    result = parse_time_references('25min ago')
    assert result[0].cardinality == 25


# =============================================================================
# Section 36: Numeric range coverage — seconds 1-60
# =============================================================================

def test_2s_ago():
    result = parse_time_references('2s ago')
    assert result[0].cardinality == 2

def test_3s_ago():
    result = parse_time_references('3s ago')
    assert result[0].cardinality == 3

def test_4s_ago():
    result = parse_time_references('4s ago')
    assert result[0].cardinality == 4

def test_6s_ago():
    result = parse_time_references('6s ago')
    assert result[0].cardinality == 6

def test_7s_ago():
    result = parse_time_references('7s ago')
    assert result[0].cardinality == 7

def test_8s_ago():
    result = parse_time_references('8s ago')
    assert result[0].cardinality == 8

def test_9s_ago():
    result = parse_time_references('9s ago')
    assert result[0].cardinality == 9

def test_15s_ago():
    result = parse_time_references('15s ago')
    assert result[0].cardinality == 15

def test_20s_ago():
    result = parse_time_references('20s ago')
    assert result[0].cardinality == 20

def test_45s_ago():
    result = parse_time_references('45s ago')
    assert result[0].cardinality == 45


# =============================================================================
# Section 37: Additional implicit past tests across all units
# =============================================================================

def test_3d_implicit():
    result = parse_time_references('3d')
    assert result[0].cardinality == 3
    assert result[0].tense == 'past'

def test_4w_implicit():
    result = parse_time_references('4w')
    assert result[0].cardinality == 4
    assert result[0].tense == 'past'

def test_3mo_implicit():
    result = parse_time_references('3mo')
    assert result[0].cardinality == 3
    assert result[0].tense == 'past'

def test_3y_implicit():
    result = parse_time_references('3y')
    assert result[0].cardinality == 3
    assert result[0].tense == 'past'

def test_6h_implicit():
    result = parse_time_references('6h')
    assert result[0].cardinality == 6
    assert result[0].tense == 'past'

def test_15min_implicit():
    result = parse_time_references('15min')
    assert result[0].cardinality == 15
    assert result[0].tense == 'past'

def test_45s_implicit():
    result = parse_time_references('45s')
    assert result[0].cardinality == 45
    assert result[0].tense == 'past'


# =============================================================================
# Section 38: Additional numeric coverage to reach 250+ tests
# =============================================================================

def test_31d_ago():
    result = parse_time_references('31d ago')
    assert result[0].cardinality == 31

def test_40d_ago():
    result = parse_time_references('40d ago')
    assert result[0].cardinality == 40

def test_60d_ago():
    result = parse_time_references('60d ago')
    assert result[0].cardinality == 60

def test_90d_ago():
    result = parse_time_references('90d ago')
    assert result[0].cardinality == 90

def test_13w_ago():
    result = parse_time_references('13w ago')
    assert result[0].cardinality == 13

def test_14w_ago():
    result = parse_time_references('14w ago')
    assert result[0].cardinality == 14

def test_16w_ago():
    result = parse_time_references('16w ago')
    assert result[0].cardinality == 16

def test_13y_ago():
    result = parse_time_references('13y ago')
    assert result[0].cardinality == 13

def test_14y_ago():
    result = parse_time_references('14y ago')
    assert result[0].cardinality == 14

def test_16y_ago():
    result = parse_time_references('16y ago')
    assert result[0].cardinality == 16

def test_17y_ago():
    result = parse_time_references('17y ago')
    assert result[0].cardinality == 17

def test_18y_ago():
    result = parse_time_references('18y ago')
    assert result[0].cardinality == 18

def test_19y_ago():
    result = parse_time_references('19y ago')
    assert result[0].cardinality == 19

def test_17h_ago():
    result = parse_time_references('17h ago')
    assert result[0].cardinality == 17

def test_19h_ago():
    result = parse_time_references('19h ago')
    assert result[0].cardinality == 19

def test_21h_ago():
    result = parse_time_references('21h ago')
    assert result[0].cardinality == 21

def test_22h_ago():
    result = parse_time_references('22h ago')
    assert result[0].cardinality == 22

def test_23h_ago():
    result = parse_time_references('23h ago')
    assert result[0].cardinality == 23

def test_11min_ago():
    result = parse_time_references('11min ago')
    assert result[0].cardinality == 11

def test_12min_ago():
    result = parse_time_references('12min ago')
    assert result[0].cardinality == 12

def test_13min_ago():
    result = parse_time_references('13min ago')
    assert result[0].cardinality == 13

def test_14min_ago():
    result = parse_time_references('14min ago')
    assert result[0].cardinality == 14

def test_16min_ago():
    result = parse_time_references('16min ago')
    assert result[0].cardinality == 16

def test_17min_ago():
    result = parse_time_references('17min ago')
    assert result[0].cardinality == 17

def test_18min_ago():
    result = parse_time_references('18min ago')
    assert result[0].cardinality == 18

def test_19min_ago():
    result = parse_time_references('19min ago')
    assert result[0].cardinality == 19

def test_11s_ago():
    result = parse_time_references('11s ago')
    assert result[0].cardinality == 11

def test_12s_ago():
    result = parse_time_references('12s ago')
    assert result[0].cardinality == 12

def test_13s_ago():
    result = parse_time_references('13s ago')
    assert result[0].cardinality == 13

def test_14s_ago():
    result = parse_time_references('14s ago')
    assert result[0].cardinality == 14

def test_16s_ago():
    result = parse_time_references('16s ago')
    assert result[0].cardinality == 16

def test_17s_ago():
    result = parse_time_references('17s ago')
    assert result[0].cardinality == 17

def test_18s_ago():
    result = parse_time_references('18s ago')
    assert result[0].cardinality == 18

def test_19s_ago():
    result = parse_time_references('19s ago')
    assert result[0].cardinality == 19
