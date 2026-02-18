#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Tests for Issue #20: Compound multi-unit expressions not supported.

Compound expressions combine multiple time units into a single temporal
reference. fast-parse-time must extract one RelativeTime per unit pair
(Option A / multi-result design), all sharing the same inferred tense.

Examples:
    '1 year 2 months ago'     → [RelativeTime(1,'year','past'), RelativeTime(2,'month','past')]
    'in 1 year 2 months'      → [RelativeTime(1,'year','future'), RelativeTime(2,'month','future')]
    '1 year, 2 months 3 days' → 3 results, all past

Connectors supported: whitespace, comma, "and", comma+and
Tense markers: 'ago'/'back' for past, 'from now'/'from today' for future,
               'in ...' prefix for future

Units: second, minute, hour, day, week, month, year, decade

Bug fix included: partial matching of '1 year ... 1 minute ago' previously
returned only the last unit; must return all units.

Related GitHub Issue:
    #20 - Gap: compound multi-unit expressions not supported
    https://github.com/craigtrim/fast-parse-time/issues/20
"""

import pytest
from datetime import timedelta
from fast_parse_time import (
    parse_time_references,
    extract_relative_times,
    extract_past_references,
    extract_future_references,
    has_temporal_info,
    resolve_to_timedelta,
    parse_dates,
    RelativeTime,
)


# =============================================================================
# Section 1: Two-unit past compounds — whitespace connector
# =============================================================================

def test_two_unit_year_month_ago():
    result = parse_time_references('1 year 2 months ago')
    assert len(result) == 2

def test_two_unit_year_month_ago_year_cardinality():
    result = parse_time_references('1 year 2 months ago')
    year_units = [r for r in result if r.frame == 'year']
    assert len(year_units) == 1
    assert year_units[0].cardinality == 1

def test_two_unit_year_month_ago_month_cardinality():
    result = parse_time_references('1 year 2 months ago')
    month_units = [r for r in result if r.frame == 'month']
    assert len(month_units) == 1
    assert month_units[0].cardinality == 2

def test_two_unit_year_month_ago_both_past():
    result = parse_time_references('1 year 2 months ago')
    assert all(r.tense == 'past' for r in result)

def test_two_unit_month_week_ago():
    result = parse_time_references('3 months 2 weeks ago')
    assert len(result) == 2

def test_two_unit_month_week_ago_month_cardinality():
    result = parse_time_references('3 months 2 weeks ago')
    month_units = [r for r in result if r.frame == 'month']
    assert month_units[0].cardinality == 3

def test_two_unit_month_week_ago_week_cardinality():
    result = parse_time_references('3 months 2 weeks ago')
    week_units = [r for r in result if r.frame == 'week']
    assert week_units[0].cardinality == 2

def test_two_unit_month_week_ago_both_past():
    result = parse_time_references('3 months 2 weeks ago')
    assert all(r.tense == 'past' for r in result)

def test_two_unit_week_day_ago():
    result = parse_time_references('2 weeks 3 days ago')
    assert len(result) == 2

def test_two_unit_week_day_ago_week_cardinality():
    result = parse_time_references('2 weeks 3 days ago')
    week_units = [r for r in result if r.frame == 'week']
    assert week_units[0].cardinality == 2

def test_two_unit_week_day_ago_day_cardinality():
    result = parse_time_references('2 weeks 3 days ago')
    day_units = [r for r in result if r.frame == 'day']
    assert day_units[0].cardinality == 3

def test_two_unit_day_hour_ago():
    result = parse_time_references('4 days 6 hours ago')
    assert len(result) == 2

def test_two_unit_day_hour_ago_day_cardinality():
    result = parse_time_references('4 days 6 hours ago')
    day_units = [r for r in result if r.frame == 'day']
    assert day_units[0].cardinality == 4

def test_two_unit_day_hour_ago_hour_cardinality():
    result = parse_time_references('4 days 6 hours ago')
    hour_units = [r for r in result if r.frame == 'hour']
    assert hour_units[0].cardinality == 6

def test_two_unit_hour_minute_ago():
    result = parse_time_references('2 hours 30 minutes ago')
    assert len(result) == 2

def test_two_unit_hour_minute_ago_hour_cardinality():
    result = parse_time_references('2 hours 30 minutes ago')
    hour_units = [r for r in result if r.frame == 'hour']
    assert hour_units[0].cardinality == 2

def test_two_unit_hour_minute_ago_minute_cardinality():
    result = parse_time_references('2 hours 30 minutes ago')
    minute_units = [r for r in result if r.frame == 'minute']
    assert minute_units[0].cardinality == 30

def test_two_unit_minute_second_ago():
    result = parse_time_references('5 minutes 45 seconds ago')
    assert len(result) == 2

def test_two_unit_minute_second_ago_minute_cardinality():
    result = parse_time_references('5 minutes 45 seconds ago')
    minute_units = [r for r in result if r.frame == 'minute']
    assert minute_units[0].cardinality == 5

def test_two_unit_minute_second_ago_second_cardinality():
    result = parse_time_references('5 minutes 45 seconds ago')
    second_units = [r for r in result if r.frame == 'second']
    assert second_units[0].cardinality == 45

def test_two_unit_year_week_ago():
    result = parse_time_references('1 year 3 weeks ago')
    assert len(result) == 2

def test_two_unit_year_day_ago():
    result = parse_time_references('2 years 15 days ago')
    assert len(result) == 2

def test_two_unit_year_hour_ago():
    result = parse_time_references('1 year 4 hours ago')
    assert len(result) == 2

def test_two_unit_decade_year_ago():
    result = parse_time_references('1 decade 2 years ago')
    assert len(result) == 2

def test_two_unit_decade_year_ago_decade_cardinality():
    """Decade is stored as Frame='year' with cardinality*10 in the KB.
    1 decade ago -> RelativeTime(10, 'year', 'past')."""
    result = parse_time_references('1 decade 2 years ago')
    # decade normalises to year(10); one of the year units must have cardinality 10
    assert any(r.frame == 'year' and r.cardinality == 10 for r in result)

def test_two_unit_decade_year_ago_year_cardinality():
    result = parse_time_references('1 decade 2 years ago')
    # decade(10) + year(2): both stored as frame='year'
    assert any(r.frame == 'year' and r.cardinality == 2 for r in result)

def test_two_unit_decade_year_ago_both_past():
    result = parse_time_references('1 decade 2 years ago')
    assert all(r.tense == 'past' for r in result)

def test_two_unit_decade_month_ago():
    result = parse_time_references('2 decades 6 months ago')
    assert len(result) == 2

def test_two_unit_year_second_ago():
    result = parse_time_references('1 year 30 seconds ago')
    assert len(result) == 2

def test_two_unit_month_hour_ago():
    result = parse_time_references('2 months 5 hours ago')
    assert len(result) == 2


# =============================================================================
# Section 2: Two-unit past compounds — comma connector
# =============================================================================

def test_two_unit_comma_year_month_ago():
    result = parse_time_references('1 year, 2 months ago')
    assert len(result) == 2

def test_two_unit_comma_year_month_ago_year_cardinality():
    result = parse_time_references('1 year, 2 months ago')
    year_units = [r for r in result if r.frame == 'year']
    assert year_units[0].cardinality == 1

def test_two_unit_comma_year_month_ago_month_cardinality():
    result = parse_time_references('1 year, 2 months ago')
    month_units = [r for r in result if r.frame == 'month']
    assert month_units[0].cardinality == 2

def test_two_unit_comma_year_month_ago_both_past():
    result = parse_time_references('1 year, 2 months ago')
    assert all(r.tense == 'past' for r in result)

def test_two_unit_comma_month_week_ago():
    result = parse_time_references('3 months, 2 weeks ago')
    assert len(result) == 2

def test_two_unit_comma_week_day_ago():
    result = parse_time_references('2 weeks, 3 days ago')
    assert len(result) == 2

def test_two_unit_comma_day_hour_ago():
    result = parse_time_references('4 days, 6 hours ago')
    assert len(result) == 2

def test_two_unit_comma_hour_minute_ago():
    result = parse_time_references('2 hours, 30 minutes ago')
    assert len(result) == 2

def test_two_unit_comma_minute_second_ago():
    result = parse_time_references('5 minutes, 45 seconds ago')
    assert len(result) == 2

def test_two_unit_comma_decade_year_ago():
    result = parse_time_references('1 decade, 5 years ago')
    assert len(result) == 2

def test_two_unit_comma_year_day_ago():
    result = parse_time_references('1 year, 10 days ago')
    assert len(result) == 2

def test_two_unit_comma_month_hour_ago():
    result = parse_time_references('6 months, 12 hours ago')
    assert len(result) == 2


# =============================================================================
# Section 3: Two-unit past compounds — "and" connector
# =============================================================================

def test_two_unit_and_year_month_ago():
    result = parse_time_references('1 year and 2 months ago')
    assert len(result) == 2

def test_two_unit_and_year_month_ago_year_cardinality():
    result = parse_time_references('1 year and 2 months ago')
    year_units = [r for r in result if r.frame == 'year']
    assert year_units[0].cardinality == 1

def test_two_unit_and_year_month_ago_month_cardinality():
    result = parse_time_references('1 year and 2 months ago')
    month_units = [r for r in result if r.frame == 'month']
    assert month_units[0].cardinality == 2

def test_two_unit_and_year_month_ago_both_past():
    result = parse_time_references('1 year and 2 months ago')
    assert all(r.tense == 'past' for r in result)

def test_two_unit_and_month_week_ago():
    result = parse_time_references('3 months and 2 weeks ago')
    assert len(result) == 2

def test_two_unit_and_week_day_ago():
    result = parse_time_references('2 weeks and 3 days ago')
    assert len(result) == 2

def test_two_unit_and_day_hour_ago():
    result = parse_time_references('4 days and 6 hours ago')
    assert len(result) == 2

def test_two_unit_and_hour_minute_ago():
    result = parse_time_references('2 hours and 30 minutes ago')
    assert len(result) == 2

def test_two_unit_and_minute_second_ago():
    result = parse_time_references('5 minutes and 45 seconds ago')
    assert len(result) == 2

def test_two_unit_and_decade_year_ago():
    result = parse_time_references('1 decade and 3 years ago')
    assert len(result) == 2

def test_two_unit_and_month_hour_ago():
    result = parse_time_references('2 months and 4 hours ago')
    assert len(result) == 2

def test_two_unit_and_year_week_ago():
    result = parse_time_references('1 year and 6 weeks ago')
    assert len(result) == 2


# =============================================================================
# Section 4: Two-unit past compounds — comma+and connector
# =============================================================================

def test_two_unit_comma_and_year_month_ago():
    result = parse_time_references('1 year, and 2 months ago')
    assert len(result) == 2

def test_two_unit_comma_and_month_week_ago():
    result = parse_time_references('3 months, and 2 weeks ago')
    assert len(result) == 2

def test_two_unit_comma_and_week_day_ago():
    result = parse_time_references('2 weeks, and 3 days ago')
    assert len(result) == 2

def test_two_unit_comma_and_hour_minute_ago():
    result = parse_time_references('2 hours, and 30 minutes ago')
    assert len(result) == 2

def test_two_unit_comma_and_decade_year_ago():
    result = parse_time_references('1 decade, and 5 years ago')
    assert len(result) == 2


# =============================================================================
# Section 5: Three-unit past compounds
# =============================================================================

def test_three_unit_year_month_week_ago():
    result = parse_time_references('1 year 2 months 3 weeks ago')
    assert len(result) == 3

def test_three_unit_year_month_week_ago_year():
    result = parse_time_references('1 year 2 months 3 weeks ago')
    year_units = [r for r in result if r.frame == 'year']
    assert year_units[0].cardinality == 1

def test_three_unit_year_month_week_ago_month():
    result = parse_time_references('1 year 2 months 3 weeks ago')
    month_units = [r for r in result if r.frame == 'month']
    assert month_units[0].cardinality == 2

def test_three_unit_year_month_week_ago_week():
    result = parse_time_references('1 year 2 months 3 weeks ago')
    week_units = [r for r in result if r.frame == 'week']
    assert week_units[0].cardinality == 3

def test_three_unit_year_month_week_ago_all_past():
    result = parse_time_references('1 year 2 months 3 weeks ago')
    assert all(r.tense == 'past' for r in result)

def test_three_unit_month_week_day_ago():
    result = parse_time_references('2 months 3 weeks 4 days ago')
    assert len(result) == 3

def test_three_unit_month_week_day_ago_month():
    result = parse_time_references('2 months 3 weeks 4 days ago')
    month_units = [r for r in result if r.frame == 'month']
    assert month_units[0].cardinality == 2

def test_three_unit_month_week_day_ago_week():
    result = parse_time_references('2 months 3 weeks 4 days ago')
    week_units = [r for r in result if r.frame == 'week']
    assert week_units[0].cardinality == 3

def test_three_unit_month_week_day_ago_day():
    result = parse_time_references('2 months 3 weeks 4 days ago')
    day_units = [r for r in result if r.frame == 'day']
    assert day_units[0].cardinality == 4

def test_three_unit_week_day_hour_ago():
    result = parse_time_references('1 week 2 days 6 hours ago')
    assert len(result) == 3

def test_three_unit_week_day_hour_ago_all_past():
    result = parse_time_references('1 week 2 days 6 hours ago')
    assert all(r.tense == 'past' for r in result)

def test_three_unit_day_hour_minute_ago():
    result = parse_time_references('3 days 2 hours 15 minutes ago')
    assert len(result) == 3

def test_three_unit_day_hour_minute_ago_day():
    result = parse_time_references('3 days 2 hours 15 minutes ago')
    day_units = [r for r in result if r.frame == 'day']
    assert day_units[0].cardinality == 3

def test_three_unit_day_hour_minute_ago_hour():
    result = parse_time_references('3 days 2 hours 15 minutes ago')
    hour_units = [r for r in result if r.frame == 'hour']
    assert hour_units[0].cardinality == 2

def test_three_unit_day_hour_minute_ago_minute():
    result = parse_time_references('3 days 2 hours 15 minutes ago')
    minute_units = [r for r in result if r.frame == 'minute']
    assert minute_units[0].cardinality == 15

def test_three_unit_hour_minute_second_ago():
    result = parse_time_references('1 hour 30 minutes 45 seconds ago')
    assert len(result) == 3

def test_three_unit_hour_minute_second_ago_hour():
    result = parse_time_references('1 hour 30 minutes 45 seconds ago')
    hour_units = [r for r in result if r.frame == 'hour']
    assert hour_units[0].cardinality == 1

def test_three_unit_hour_minute_second_ago_minute():
    result = parse_time_references('1 hour 30 minutes 45 seconds ago')
    minute_units = [r for r in result if r.frame == 'minute']
    assert minute_units[0].cardinality == 30

def test_three_unit_hour_minute_second_ago_second():
    result = parse_time_references('1 hour 30 minutes 45 seconds ago')
    second_units = [r for r in result if r.frame == 'second']
    assert second_units[0].cardinality == 45

def test_three_unit_comma_separated_ago():
    result = parse_time_references('1 year, 09 months, 01 weeks ago')
    assert len(result) == 3

def test_three_unit_comma_separated_ago_year():
    result = parse_time_references('1 year, 09 months, 01 weeks ago')
    year_units = [r for r in result if r.frame == 'year']
    assert year_units[0].cardinality == 1

def test_three_unit_comma_separated_ago_month():
    result = parse_time_references('1 year, 09 months, 01 weeks ago')
    month_units = [r for r in result if r.frame == 'month']
    assert month_units[0].cardinality == 9

def test_three_unit_comma_separated_ago_week():
    result = parse_time_references('1 year, 09 months, 01 weeks ago')
    week_units = [r for r in result if r.frame == 'week']
    assert week_units[0].cardinality == 1

def test_three_unit_decade_year_month_ago():
    result = parse_time_references('1 decade 2 years 3 months ago')
    assert len(result) == 3

def test_three_unit_decade_year_month_ago_decade():
    """1 decade → RelativeTime(10, 'year', 'past') in the KB."""
    result = parse_time_references('1 decade 2 years 3 months ago')
    assert any(r.frame == 'year' and r.cardinality == 10 for r in result)

def test_three_unit_decade_year_month_ago_year():
    result = parse_time_references('1 decade 2 years 3 months ago')
    assert any(r.frame == 'year' and r.cardinality == 2 for r in result)

def test_three_unit_decade_year_month_ago_month():
    result = parse_time_references('1 decade 2 years 3 months ago')
    month_units = [r for r in result if r.frame == 'month']
    assert month_units[0].cardinality == 3

def test_three_unit_year_month_day_ago():
    result = parse_time_references('2 years 6 months 15 days ago')
    assert len(result) == 3

def test_three_unit_year_month_day_all_past():
    result = parse_time_references('2 years 6 months 15 days ago')
    assert all(r.tense == 'past' for r in result)


# =============================================================================
# Section 6: Four-unit past compounds
# =============================================================================

def test_four_unit_year_month_week_day_ago():
    result = parse_time_references('1 year 2 months 3 weeks 4 days ago')
    assert len(result) == 4

def test_four_unit_year_month_week_day_ago_year():
    result = parse_time_references('1 year 2 months 3 weeks 4 days ago')
    year_units = [r for r in result if r.frame == 'year']
    assert year_units[0].cardinality == 1

def test_four_unit_year_month_week_day_ago_month():
    result = parse_time_references('1 year 2 months 3 weeks 4 days ago')
    month_units = [r for r in result if r.frame == 'month']
    assert month_units[0].cardinality == 2

def test_four_unit_year_month_week_day_ago_week():
    result = parse_time_references('1 year 2 months 3 weeks 4 days ago')
    week_units = [r for r in result if r.frame == 'week']
    assert week_units[0].cardinality == 3

def test_four_unit_year_month_week_day_ago_day():
    result = parse_time_references('1 year 2 months 3 weeks 4 days ago')
    day_units = [r for r in result if r.frame == 'day']
    assert day_units[0].cardinality == 4

def test_four_unit_year_month_week_day_all_past():
    result = parse_time_references('1 year 2 months 3 weeks 4 days ago')
    assert all(r.tense == 'past' for r in result)

def test_four_unit_month_week_day_hour_ago():
    result = parse_time_references('3 months 2 weeks 5 days 8 hours ago')
    assert len(result) == 4

def test_four_unit_week_day_hour_minute_ago():
    result = parse_time_references('1 week 2 days 3 hours 30 minutes ago')
    assert len(result) == 4

def test_four_unit_day_hour_minute_second_ago():
    result = parse_time_references('1 day 2 hours 15 minutes 30 seconds ago')
    assert len(result) == 4

def test_four_unit_day_hour_minute_second_day():
    result = parse_time_references('1 day 2 hours 15 minutes 30 seconds ago')
    day_units = [r for r in result if r.frame == 'day']
    assert day_units[0].cardinality == 1

def test_four_unit_comma_separated():
    result = parse_time_references('1 year, 2 months, 3 weeks, 4 days ago')
    assert len(result) == 4

def test_four_unit_comma_separated_all_past():
    result = parse_time_references('1 year, 2 months, 3 weeks, 4 days ago')
    assert all(r.tense == 'past' for r in result)


# =============================================================================
# Section 7: Five and six-unit past compounds
# =============================================================================

def test_five_unit_compound_ago():
    result = parse_time_references('1 year 2 months 3 weeks 4 days 5 hours ago')
    assert len(result) == 5

def test_five_unit_compound_ago_all_past():
    result = parse_time_references('1 year 2 months 3 weeks 4 days 5 hours ago')
    assert all(r.tense == 'past' for r in result)

def test_five_unit_compound_ago_year():
    result = parse_time_references('1 year 2 months 3 weeks 4 days 5 hours ago')
    year_units = [r for r in result if r.frame == 'year']
    assert year_units[0].cardinality == 1

def test_five_unit_compound_ago_hour():
    result = parse_time_references('1 year 2 months 3 weeks 4 days 5 hours ago')
    hour_units = [r for r in result if r.frame == 'hour']
    assert hour_units[0].cardinality == 5

def test_six_unit_compound_ago():
    result = parse_time_references('1 year 1 month 1 week 1 day 1 hour 1 minute ago')
    assert len(result) == 6

def test_six_unit_compound_ago_all_past():
    result = parse_time_references('1 year 1 month 1 week 1 day 1 hour 1 minute ago')
    assert all(r.tense == 'past' for r in result)

def test_six_unit_compound_ago_year():
    result = parse_time_references('1 year 1 month 1 week 1 day 1 hour 1 minute ago')
    year_units = [r for r in result if r.frame == 'year']
    assert year_units[0].cardinality == 1

def test_six_unit_compound_ago_minute():
    result = parse_time_references('1 year 1 month 1 week 1 day 1 hour 1 minute ago')
    minute_units = [r for r in result if r.frame == 'minute']
    assert minute_units[0].cardinality == 1

def test_six_unit_comma_separated_ago():
    result = parse_time_references('1 year, 1 month, 1 week, 1 day, 1 hour, 1 minute ago')
    assert len(result) == 6

def test_six_unit_full_dateparser_expression():
    """Bug fix: full expression previously returned only 1 result (the last unit)."""
    result = parse_time_references('1 year, 1 month, 1 week, 1 day, 1 hour and 1 minute ago')
    assert len(result) == 6

def test_six_unit_full_dateparser_all_past():
    result = parse_time_references('1 year, 1 month, 1 week, 1 day, 1 hour and 1 minute ago')
    assert all(r.tense == 'past' for r in result)

def test_six_unit_full_dateparser_year():
    result = parse_time_references('1 year, 1 month, 1 week, 1 day, 1 hour and 1 minute ago')
    year_units = [r for r in result if r.frame == 'year']
    assert year_units[0].cardinality == 1

def test_six_unit_full_dateparser_month():
    result = parse_time_references('1 year, 1 month, 1 week, 1 day, 1 hour and 1 minute ago')
    month_units = [r for r in result if r.frame == 'month']
    assert month_units[0].cardinality == 1

def test_six_unit_full_dateparser_week():
    result = parse_time_references('1 year, 1 month, 1 week, 1 day, 1 hour and 1 minute ago')
    week_units = [r for r in result if r.frame == 'week']
    assert week_units[0].cardinality == 1

def test_six_unit_full_dateparser_day():
    result = parse_time_references('1 year, 1 month, 1 week, 1 day, 1 hour and 1 minute ago')
    day_units = [r for r in result if r.frame == 'day']
    assert day_units[0].cardinality == 1

def test_six_unit_full_dateparser_hour():
    result = parse_time_references('1 year, 1 month, 1 week, 1 day, 1 hour and 1 minute ago')
    hour_units = [r for r in result if r.frame == 'hour']
    assert hour_units[0].cardinality == 1

def test_six_unit_full_dateparser_minute():
    result = parse_time_references('1 year, 1 month, 1 week, 1 day, 1 hour and 1 minute ago')
    minute_units = [r for r in result if r.frame == 'minute']
    assert minute_units[0].cardinality == 1


# =============================================================================
# Section 8: Two-unit future compounds — "from now"
# =============================================================================

def test_two_unit_future_year_month_from_now():
    result = parse_time_references('1 year 2 months from now')
    assert len(result) == 2

def test_two_unit_future_year_month_from_now_year():
    result = parse_time_references('1 year 2 months from now')
    year_units = [r for r in result if r.frame == 'year']
    assert year_units[0].cardinality == 1

def test_two_unit_future_year_month_from_now_month():
    result = parse_time_references('1 year 2 months from now')
    month_units = [r for r in result if r.frame == 'month']
    assert month_units[0].cardinality == 2

def test_two_unit_future_year_month_from_now_both_future():
    result = parse_time_references('1 year 2 months from now')
    assert all(r.tense == 'future' for r in result)

def test_two_unit_future_month_week_from_now():
    result = parse_time_references('3 months 2 weeks from now')
    assert len(result) == 2

def test_two_unit_future_month_week_from_now_both_future():
    result = parse_time_references('3 months 2 weeks from now')
    assert all(r.tense == 'future' for r in result)

def test_two_unit_future_week_day_from_now():
    result = parse_time_references('2 weeks 3 days from now')
    assert len(result) == 2

def test_two_unit_future_day_hour_from_now():
    result = parse_time_references('4 days 6 hours from now')
    assert len(result) == 2

def test_two_unit_future_hour_minute_from_now():
    result = parse_time_references('2 hours 30 minutes from now')
    assert len(result) == 2

def test_two_unit_future_hour_minute_from_now_both_future():
    result = parse_time_references('2 hours 30 minutes from now')
    assert all(r.tense == 'future' for r in result)

def test_two_unit_future_minute_second_from_now():
    result = parse_time_references('5 minutes 30 seconds from now')
    assert len(result) == 2

def test_two_unit_future_decade_year_from_now():
    result = parse_time_references('1 decade 2 years from now')
    assert len(result) == 2

def test_two_unit_future_decade_year_from_now_both_future():
    result = parse_time_references('1 decade 2 years from now')
    assert all(r.tense == 'future' for r in result)

def test_two_unit_future_year_week_from_now():
    result = parse_time_references('1 year 6 weeks from now')
    assert len(result) == 2

def test_two_unit_future_comma_year_month_from_now():
    result = parse_time_references('1 year, 2 months from now')
    assert len(result) == 2

def test_two_unit_future_comma_year_month_from_now_both_future():
    result = parse_time_references('1 year, 2 months from now')
    assert all(r.tense == 'future' for r in result)

def test_two_unit_future_and_year_month_from_now():
    result = parse_time_references('1 year and 2 months from now')
    assert len(result) == 2

def test_two_unit_future_and_year_month_from_now_both_future():
    result = parse_time_references('1 year and 2 months from now')
    assert all(r.tense == 'future' for r in result)

def test_two_unit_future_and_hour_minute_from_now():
    result = parse_time_references('2 hours and 30 minutes from now')
    assert len(result) == 2

def test_two_unit_future_comma_and_month_week_from_now():
    result = parse_time_references('3 months, and 2 weeks from now')
    assert len(result) == 2


# =============================================================================
# Section 9: Three-unit future compounds — "from now"
# =============================================================================

def test_three_unit_future_year_month_week_from_now():
    result = parse_time_references('1 year 2 months 3 weeks from now')
    assert len(result) == 3

def test_three_unit_future_year_month_week_from_now_all_future():
    result = parse_time_references('1 year 2 months 3 weeks from now')
    assert all(r.tense == 'future' for r in result)

def test_three_unit_future_year_month_week_from_now_week():
    result = parse_time_references('1 year 2 months 3 weeks from now')
    week_units = [r for r in result if r.frame == 'week']
    assert week_units[0].cardinality == 3

def test_three_unit_future_month_week_day_from_now():
    result = parse_time_references('2 months 3 weeks 4 days from now')
    assert len(result) == 3

def test_three_unit_future_week_day_hour_from_now():
    result = parse_time_references('1 week 2 days 6 hours from now')
    assert len(result) == 3

def test_three_unit_future_day_hour_minute_from_now():
    result = parse_time_references('3 days 2 hours 15 minutes from now')
    assert len(result) == 3

def test_three_unit_future_day_hour_minute_from_now_all_future():
    result = parse_time_references('3 days 2 hours 15 minutes from now')
    assert all(r.tense == 'future' for r in result)

def test_three_unit_future_comma_separated_from_now():
    result = parse_time_references('1 year, 2 months, 3 weeks from now')
    assert len(result) == 3

def test_three_unit_future_comma_separated_from_now_all_future():
    result = parse_time_references('1 year, 2 months, 3 weeks from now')
    assert all(r.tense == 'future' for r in result)

def test_three_unit_future_decade_year_month_from_now():
    result = parse_time_references('1 decade 2 years 3 months from now')
    assert len(result) == 3

def test_three_unit_future_hour_minute_second_from_now():
    result = parse_time_references('1 hour 30 minutes 45 seconds from now')
    assert len(result) == 3


# =============================================================================
# Section 10: "In N unit M unit" future prefix form
# =============================================================================

def test_in_prefix_two_unit_year_month():
    result = parse_time_references('in 1 year 2 months')
    assert len(result) == 2

def test_in_prefix_two_unit_year_month_year():
    result = parse_time_references('in 1 year 2 months')
    year_units = [r for r in result if r.frame == 'year']
    assert year_units[0].cardinality == 1

def test_in_prefix_two_unit_year_month_month():
    result = parse_time_references('in 1 year 2 months')
    month_units = [r for r in result if r.frame == 'month']
    assert month_units[0].cardinality == 2

def test_in_prefix_two_unit_year_month_both_future():
    result = parse_time_references('in 1 year 2 months')
    assert all(r.tense == 'future' for r in result)

def test_in_prefix_two_unit_month_week():
    result = parse_time_references('in 3 months 2 weeks')
    assert len(result) == 2

def test_in_prefix_two_unit_month_week_both_future():
    result = parse_time_references('in 3 months 2 weeks')
    assert all(r.tense == 'future' for r in result)

def test_in_prefix_two_unit_week_day():
    result = parse_time_references('in 2 weeks 3 days')
    assert len(result) == 2

def test_in_prefix_two_unit_day_hour():
    result = parse_time_references('in 4 days 6 hours')
    assert len(result) == 2

def test_in_prefix_two_unit_hour_minute():
    result = parse_time_references('in 2 hours 30 minutes')
    assert len(result) == 2

def test_in_prefix_two_unit_hour_minute_both_future():
    result = parse_time_references('in 2 hours 30 minutes')
    assert all(r.tense == 'future' for r in result)

def test_in_prefix_three_unit_year_month_week():
    result = parse_time_references('in 1 year 2 months 3 weeks')
    assert len(result) == 3

def test_in_prefix_three_unit_all_future():
    result = parse_time_references('in 1 year 2 months 3 weeks')
    assert all(r.tense == 'future' for r in result)

def test_in_prefix_three_unit_month_week_day():
    result = parse_time_references('in 2 months 3 weeks 4 days')
    assert len(result) == 3

def test_in_prefix_four_unit():
    result = parse_time_references('in 1 year 2 months 3 weeks 4 days')
    assert len(result) == 4

def test_in_prefix_four_unit_all_future():
    result = parse_time_references('in 1 year 2 months 3 weeks 4 days')
    assert all(r.tense == 'future' for r in result)

def test_in_prefix_comma_two_unit():
    result = parse_time_references('in 1 year, 2 months')
    assert len(result) == 2

def test_in_prefix_comma_two_unit_both_future():
    result = parse_time_references('in 1 year, 2 months')
    assert all(r.tense == 'future' for r in result)

def test_in_prefix_and_two_unit():
    result = parse_time_references('in 1 year and 2 months')
    assert len(result) == 2

def test_in_prefix_and_two_unit_both_future():
    result = parse_time_references('in 1 year and 2 months')
    assert all(r.tense == 'future' for r in result)

def test_in_prefix_decade_year():
    result = parse_time_references('in 1 decade 2 years')
    assert len(result) == 2

def test_in_prefix_decade_year_both_future():
    result = parse_time_references('in 1 decade 2 years')
    assert all(r.tense == 'future' for r in result)


# =============================================================================
# Section 11: "Back" tense marker (synonym for "ago")
# =============================================================================

def test_two_unit_back_year_month():
    result = parse_time_references('1 year 2 months back')
    assert len(result) == 2

def test_two_unit_back_year_month_both_past():
    result = parse_time_references('1 year 2 months back')
    assert all(r.tense == 'past' for r in result)

def test_two_unit_back_month_week():
    result = parse_time_references('3 months 2 weeks back')
    assert len(result) == 2

def test_two_unit_back_week_day():
    result = parse_time_references('2 weeks 3 days back')
    assert len(result) == 2

def test_three_unit_back_compound():
    result = parse_time_references('1 year 2 months 3 weeks back')
    assert len(result) == 3

def test_three_unit_back_compound_all_past():
    result = parse_time_references('1 year 2 months 3 weeks back')
    assert all(r.tense == 'past' for r in result)


# =============================================================================
# Section 12: Cardinality type assertions — must be int
# =============================================================================

def test_compound_cardinality_is_int_year():
    result = parse_time_references('1 year 2 months ago')
    year_units = [r for r in result if r.frame == 'year']
    assert isinstance(year_units[0].cardinality, int)

def test_compound_cardinality_is_int_month():
    result = parse_time_references('1 year 2 months ago')
    month_units = [r for r in result if r.frame == 'month']
    assert isinstance(month_units[0].cardinality, int)

def test_compound_cardinality_is_int_week():
    result = parse_time_references('2 weeks 3 days ago')
    week_units = [r for r in result if r.frame == 'week']
    assert isinstance(week_units[0].cardinality, int)

def test_compound_cardinality_is_int_day():
    result = parse_time_references('2 weeks 3 days ago')
    day_units = [r for r in result if r.frame == 'day']
    assert isinstance(day_units[0].cardinality, int)

def test_compound_cardinality_is_int_hour():
    result = parse_time_references('2 hours 30 minutes ago')
    hour_units = [r for r in result if r.frame == 'hour']
    assert isinstance(hour_units[0].cardinality, int)

def test_compound_cardinality_is_int_minute():
    result = parse_time_references('2 hours 30 minutes ago')
    minute_units = [r for r in result if r.frame == 'minute']
    assert isinstance(minute_units[0].cardinality, int)

def test_compound_cardinality_is_int_second():
    result = parse_time_references('5 minutes 45 seconds ago')
    second_units = [r for r in result if r.frame == 'second']
    assert isinstance(second_units[0].cardinality, int)

def test_compound_return_type_is_list():
    result = parse_time_references('1 year 2 months ago')
    assert isinstance(result, list)

def test_compound_elements_are_relativetime():
    result = parse_time_references('1 year 2 months ago')
    for r in result:
        assert isinstance(r, RelativeTime)

def test_compound_frame_is_string():
    result = parse_time_references('1 year 2 months ago')
    for r in result:
        assert isinstance(r.frame, str)

def test_compound_tense_is_string():
    result = parse_time_references('1 year 2 months ago')
    for r in result:
        assert isinstance(r.tense, str)


# =============================================================================
# Section 13: Float cardinalities in compound expressions
# =============================================================================

def test_float_in_compound_year_rounded():
    result = parse_time_references('1.5 years 2 months ago')
    year_units = [r for r in result if r.frame == 'year']
    assert year_units[0].cardinality == 2

def test_float_in_compound_month_rounded():
    result = parse_time_references('1 year 2.7 months ago')
    month_units = [r for r in result if r.frame == 'month']
    assert month_units[0].cardinality == 3

def test_float_in_compound_both_float():
    result = parse_time_references('1.2 years 2.8 months ago')
    assert len(result) == 2

def test_float_in_compound_both_float_year():
    result = parse_time_references('1.2 years 2.8 months ago')
    year_units = [r for r in result if r.frame == 'year']
    assert year_units[0].cardinality == 1

def test_float_in_compound_both_float_month():
    result = parse_time_references('1.2 years 2.8 months ago')
    month_units = [r for r in result if r.frame == 'month']
    assert month_units[0].cardinality == 3

def test_float_in_compound_week_day():
    result = parse_time_references('2.3 weeks 4.1 days ago')
    assert len(result) == 2

def test_float_in_compound_week_rounded():
    result = parse_time_references('2.3 weeks 4.1 days ago')
    week_units = [r for r in result if r.frame == 'week']
    assert week_units[0].cardinality == 2

def test_float_in_compound_day_rounded():
    result = parse_time_references('2.3 weeks 4.1 days ago')
    day_units = [r for r in result if r.frame == 'day']
    assert day_units[0].cardinality == 4

def test_float_in_compound_future():
    result = parse_time_references('1.5 years 3 months from now')
    year_units = [r for r in result if r.frame == 'year']
    assert year_units[0].cardinality == 2
    assert year_units[0].tense == 'future'

def test_float_in_compound_three_units():
    result = parse_time_references('1.5 years 2.3 months 10.7 days ago')
    assert len(result) == 3

def test_float_in_compound_hour_minute():
    result = parse_time_references('2.9 hours 45.4 minutes ago')
    hour_units = [r for r in result if r.frame == 'hour']
    assert hour_units[0].cardinality == 3


# =============================================================================
# Section 14: Abbreviated units in compound expressions
# =============================================================================

def test_abbreviated_hr_min_ago():
    result = parse_time_references('2 hrs 30 mins ago')
    assert len(result) == 2

def test_abbreviated_hr_min_ago_hour():
    result = parse_time_references('2 hrs 30 mins ago')
    hour_units = [r for r in result if r.frame == 'hour']
    assert hour_units[0].cardinality == 2

def test_abbreviated_hr_min_ago_minute():
    result = parse_time_references('2 hrs 30 mins ago')
    minute_units = [r for r in result if r.frame == 'minute']
    assert minute_units[0].cardinality == 30

def test_abbreviated_hr_min_ago_both_past():
    result = parse_time_references('2 hrs 30 mins ago')
    assert all(r.tense == 'past' for r in result)

def test_abbreviated_yr_mo_ago():
    result = parse_time_references('2 yrs 6 mos ago')
    assert len(result) == 2

def test_abbreviated_yr_mo_ago_year():
    result = parse_time_references('2 yrs 6 mos ago')
    year_units = [r for r in result if r.frame == 'year']
    assert year_units[0].cardinality == 2

def test_abbreviated_yr_mo_ago_month():
    result = parse_time_references('2 yrs 6 mos ago')
    month_units = [r for r in result if r.frame == 'month']
    assert month_units[0].cardinality == 6

def test_abbreviated_wks_days_ago():
    result = parse_time_references('3 wks 4 days ago')
    assert len(result) == 2

def test_abbreviated_wks_days_ago_week():
    result = parse_time_references('3 wks 4 days ago')
    week_units = [r for r in result if r.frame == 'week']
    assert week_units[0].cardinality == 3

def test_abbreviated_secs_mins_ago():
    result = parse_time_references('10 secs 5 mins ago')
    assert len(result) == 2

def test_abbreviated_hr_min_from_now():
    result = parse_time_references('2 hrs 30 mins from now')
    assert len(result) == 2

def test_abbreviated_hr_min_from_now_both_future():
    result = parse_time_references('2 hrs 30 mins from now')
    assert all(r.tense == 'future' for r in result)

def test_abbreviated_yr_mo_from_now():
    result = parse_time_references('1 yr 6 mos from now')
    assert len(result) == 2

def test_abbreviated_three_unit_compound():
    result = parse_time_references('2 yrs 6 mos 15 days ago')
    assert len(result) == 3


# =============================================================================
# Section 15: Sentence context — compound embedded in prose
# =============================================================================

def test_compound_in_sentence_basic():
    result = parse_time_references('I posted this 1 year 2 months ago on the forum')
    year_units = [r for r in result if r.frame == 'year']
    month_units = [r for r in result if r.frame == 'month']
    assert len(year_units) == 1
    assert len(month_units) == 1

def test_compound_in_sentence_cardinalities():
    result = parse_time_references('I posted this 1 year 2 months ago on the forum')
    year_units = [r for r in result if r.frame == 'year']
    assert year_units[0].cardinality == 1

def test_compound_in_sentence_future():
    result = parse_time_references('the contract expires in 2 years 6 months')
    year_units = [r for r in result if r.frame == 'year']
    month_units = [r for r in result if r.frame == 'month']
    assert len(year_units) == 1
    assert len(month_units) == 1

def test_compound_in_sentence_future_tense():
    result = parse_time_references('the contract expires in 2 years 6 months')
    assert all(r.tense == 'future' for r in result)

def test_compound_in_sentence_at_start():
    result = parse_time_references('3 months 2 weeks ago the project started')
    month_units = [r for r in result if r.frame == 'month']
    assert month_units[0].cardinality == 3

def test_compound_in_sentence_three_unit():
    result = parse_time_references('she left the company 2 years 3 months 1 week ago')
    assert len([r for r in result if r.frame in ('year', 'month', 'week')]) == 3

def test_compound_in_sentence_three_unit_tense():
    result = parse_time_references('she left the company 2 years 3 months 1 week ago')
    assert all(r.tense == 'past' for r in result)

def test_compound_in_sentence_date_and_compound():
    """Compound relative time alongside other text extracts correctly."""
    result = parse_time_references('data from 2 years 6 months ago is now archived')
    year_units = [r for r in result if r.frame == 'year']
    assert year_units[0].cardinality == 2

def test_compound_in_sentence_with_comma():
    result = parse_time_references('we met 1 year, 3 months ago at the conference')
    year_units = [r for r in result if r.frame == 'year']
    month_units = [r for r in result if r.frame == 'month']
    assert year_units[0].cardinality == 1
    assert month_units[0].cardinality == 3

def test_compound_in_sentence_future_from_now():
    result = parse_time_references('the deadline is 6 months 2 weeks from now')
    month_units = [r for r in result if r.frame == 'month']
    week_units = [r for r in result if r.frame == 'week']
    assert month_units[0].cardinality == 6
    assert week_units[0].cardinality == 2


# =============================================================================
# Section 16: has_temporal_info with compound expressions
# =============================================================================

def test_has_temporal_info_two_unit_compound():
    assert has_temporal_info('1 year 2 months ago') is True

def test_has_temporal_info_three_unit_compound():
    assert has_temporal_info('2 months 3 weeks 4 days ago') is True

def test_has_temporal_info_future_compound():
    assert has_temporal_info('1 year 2 months from now') is True

def test_has_temporal_info_in_prefix_compound():
    assert has_temporal_info('in 1 year 2 months') is True

def test_has_temporal_info_six_unit_compound():
    assert has_temporal_info('1 year, 1 month, 1 week, 1 day, 1 hour and 1 minute ago') is True

def test_has_temporal_info_compound_in_sentence():
    assert has_temporal_info('I posted this 1 year 2 months ago') is True


# =============================================================================
# Section 17: extract_past_references with compound
# =============================================================================

def test_extract_past_two_unit():
    result = extract_past_references('1 year 2 months ago')
    assert len(result) == 2

def test_extract_past_two_unit_all_past():
    result = extract_past_references('1 year 2 months ago')
    assert all(r.tense == 'past' for r in result)

def test_extract_past_three_unit():
    result = extract_past_references('2 months 3 weeks 4 days ago')
    assert len(result) == 3

def test_extract_past_six_unit():
    result = extract_past_references('1 year, 1 month, 1 week, 1 day, 1 hour and 1 minute ago')
    assert len(result) == 6

def test_extract_past_excludes_future():
    result = extract_past_references('1 year 2 months from now')
    assert len(result) == 0

def test_extract_past_mixed_text():
    """Past compound doesn't bleed into future references."""
    result = extract_past_references('posted 1 year 2 months ago, due in 3 weeks')
    year_units = [r for r in result if r.frame == 'year']
    assert year_units[0].cardinality == 1


# =============================================================================
# Section 18: extract_future_references with compound
# =============================================================================

def test_extract_future_two_unit():
    result = extract_future_references('1 year 2 months from now')
    assert len(result) == 2

def test_extract_future_two_unit_all_future():
    result = extract_future_references('1 year 2 months from now')
    assert all(r.tense == 'future' for r in result)

def test_extract_future_three_unit():
    result = extract_future_references('2 months 3 weeks 4 days from now')
    assert len(result) == 3

def test_extract_future_in_prefix():
    result = extract_future_references('in 1 year 2 months')
    assert len(result) == 2

def test_extract_future_excludes_past():
    result = extract_future_references('1 year 2 months ago')
    assert len(result) == 0

def test_extract_future_in_prefix_four_unit():
    result = extract_future_references('in 1 year 2 months 3 weeks 4 days')
    assert len(result) == 4


# =============================================================================
# Section 19: resolve_to_timedelta with compound expressions
# =============================================================================

def test_resolve_timedelta_two_unit_past_returns_list():
    result = resolve_to_timedelta('1 year 2 months ago')
    assert isinstance(result, list)

def test_resolve_timedelta_two_unit_past_length():
    result = resolve_to_timedelta('1 year 2 months ago')
    assert len(result) == 2

def test_resolve_timedelta_year_negative():
    """Year unit in past compound resolves to negative timedelta."""
    result = resolve_to_timedelta('1 year 2 months ago')
    year_deltas = [d for d in result if d.days <= -365]
    assert len(year_deltas) >= 1

def test_resolve_timedelta_future_positive():
    """Units in future compound resolve to positive timedeltas."""
    result = resolve_to_timedelta('1 year 2 months from now')
    assert all(d.days > 0 for d in result)

def test_resolve_timedelta_week_day_past():
    result = resolve_to_timedelta('2 weeks 3 days ago')
    assert len(result) == 2

def test_resolve_timedelta_week_negative():
    result = resolve_to_timedelta('2 weeks 3 days ago')
    week_deltas = [d for d in result if d == timedelta(days=-14)]
    assert len(week_deltas) == 1

def test_resolve_timedelta_day_negative():
    result = resolve_to_timedelta('2 weeks 3 days ago')
    day_deltas = [d for d in result if d == timedelta(days=-3)]
    assert len(day_deltas) == 1

def test_resolve_timedelta_hour_minute_past():
    result = resolve_to_timedelta('2 hours 30 minutes ago')
    hour_deltas = [d for d in result if d == timedelta(hours=-2)]
    assert len(hour_deltas) == 1

def test_resolve_timedelta_minute_delta():
    result = resolve_to_timedelta('2 hours 30 minutes ago')
    minute_deltas = [d for d in result if d == timedelta(minutes=-30)]
    assert len(minute_deltas) == 1

def test_resolve_timedelta_six_unit():
    result = resolve_to_timedelta('1 year, 1 month, 1 week, 1 day, 1 hour and 1 minute ago')
    assert len(result) == 6


# =============================================================================
# Section 20: parse_dates integration with compound
# =============================================================================

def test_parse_dates_two_unit_has_relative():
    result = parse_dates('1 year 2 months ago')
    assert len(result.relative_times) == 2

def test_parse_dates_two_unit_year_cardinality():
    result = parse_dates('1 year 2 months ago')
    year_units = [r for r in result.relative_times if r.frame == 'year']
    assert year_units[0].cardinality == 1

def test_parse_dates_two_unit_month_cardinality():
    result = parse_dates('1 year 2 months ago')
    month_units = [r for r in result.relative_times if r.frame == 'month']
    assert month_units[0].cardinality == 2

def test_parse_dates_six_unit_count():
    result = parse_dates('1 year, 1 month, 1 week, 1 day, 1 hour and 1 minute ago')
    assert len(result.relative_times) == 6

def test_parse_dates_compound_has_dates():
    result = parse_dates('1 year 2 months ago')
    assert result.has_dates is True

def test_parse_dates_future_compound():
    result = parse_dates('in 1 year 2 months')
    assert len(result.relative_times) == 2

def test_parse_dates_future_compound_tense():
    result = parse_dates('in 1 year 2 months')
    assert all(r.tense == 'future' for r in result.relative_times)

def test_parse_dates_compound_in_sentence():
    result = parse_dates('she left 2 years 6 months ago to travel')
    year_units = [r for r in result.relative_times if r.frame == 'year']
    assert year_units[0].cardinality == 2


# =============================================================================
# Section 21: Capitalization handling
# =============================================================================

def test_compound_capitalized_year():
    result = parse_time_references('1 Year 2 Months ago')
    assert len(result) == 2

def test_compound_capitalized_ago():
    result = parse_time_references('1 year 2 months Ago')
    assert len(result) == 2

def test_compound_all_caps():
    result = parse_time_references('1 YEAR 2 MONTHS AGO')
    assert len(result) == 2

def test_compound_mixed_caps_cardinality():
    result = parse_time_references('1 Year 2 Months ago')
    year_units = [r for r in result if r.frame == 'year']
    assert year_units[0].cardinality == 1

def test_compound_mixed_caps_tense():
    result = parse_time_references('1 Year 2 Months ago')
    assert all(r.tense == 'past' for r in result)

def test_compound_future_capitalized():
    result = parse_time_references('1 Year 2 Months From Now')
    assert all(r.tense == 'future' for r in result)


# =============================================================================
# Section 22: Large cardinalities in compound expressions
# =============================================================================

def test_large_cardinality_year_compound():
    result = parse_time_references('100 years 6 months ago')
    year_units = [r for r in result if r.frame == 'year']
    assert year_units[0].cardinality == 100

def test_large_cardinality_month_compound():
    result = parse_time_references('1 year 36 months ago')
    month_units = [r for r in result if r.frame == 'month']
    assert month_units[0].cardinality == 36

def test_large_cardinality_day_compound():
    result = parse_time_references('2 months 365 days ago')
    day_units = [r for r in result if r.frame == 'day']
    assert day_units[0].cardinality == 365

def test_large_cardinality_hour_compound():
    result = parse_time_references('1 week 48 hours ago')
    hour_units = [r for r in result if r.frame == 'hour']
    assert hour_units[0].cardinality == 48

def test_large_cardinality_minute_compound():
    result = parse_time_references('2 hours 120 minutes ago')
    minute_units = [r for r in result if r.frame == 'minute']
    assert minute_units[0].cardinality == 120

def test_large_cardinality_second_compound():
    result = parse_time_references('1 minute 300 seconds ago')
    second_units = [r for r in result if r.frame == 'second']
    assert second_units[0].cardinality == 300

def test_large_cardinality_decade_compound():
    """5 decades → RelativeTime(50, 'year', 'past') in the KB."""
    result = parse_time_references('5 decades 3 years ago')
    assert any(r.frame == 'year' and r.cardinality == 50 for r in result)


# =============================================================================
# Section 23: Regression — partial match bug
# =============================================================================

def test_regression_partial_match_six_unit():
    """Previously returned only [RelativeTime(1,'minute','past')] — must return 6."""
    result = parse_time_references('1 year, 1 month, 1 week, 1 day, 1 hour and 1 minute ago')
    assert len(result) == 6

def test_regression_partial_match_not_just_last():
    """The last unit is not the only result."""
    result = parse_time_references('1 year, 1 month, 1 week, 1 day, 1 hour and 1 minute ago')
    minute_only = [r for r in result if r.frame == 'minute']
    assert len(minute_only) == 1
    assert len(result) > 1  # not just minute

def test_regression_partial_match_year_included():
    result = parse_time_references('1 year, 1 month, 1 week, 1 day, 1 hour and 1 minute ago')
    year_units = [r for r in result if r.frame == 'year']
    assert len(year_units) == 1

def test_regression_partial_match_four_unit():
    """Four-unit expression must return 4, not just the tail."""
    result = parse_time_references('1 year 2 months 3 weeks 4 days ago')
    assert len(result) == 4

def test_regression_dateparser_exact_expression():
    """Exact expression from dateparser test suite."""
    result = parse_time_references('1 year, 09 months, 01 weeks ago')
    assert len(result) == 3


# =============================================================================
# Section 24: Implicit past (no tense marker)
# =============================================================================

def test_implicit_past_year_month():
    """'1 year 2 months' with no tense marker defaults to past."""
    result = parse_time_references('1 year 2 months')
    assert len(result) >= 1  # implementation may vary on implicit past

def test_implicit_past_has_temporal_info():
    assert has_temporal_info('1 year 2 months') is True


# =============================================================================
# Section 25: Non-interference with single-unit expressions
# =============================================================================

def test_single_unit_not_affected_days_ago():
    """Single unit expressions must still work correctly."""
    result = parse_time_references('5 days ago')
    assert len(result) == 1
    assert result[0].cardinality == 5
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'

def test_single_unit_not_affected_years_ago():
    result = parse_time_references('3 years ago')
    assert len(result) == 1
    assert result[0].cardinality == 3

def test_single_unit_not_affected_minutes_from_now():
    result = parse_time_references('30 minutes from now')
    assert len(result) == 1
    assert result[0].tense == 'future'

def test_single_unit_not_affected_hours_back():
    result = parse_time_references('2 hours back')
    assert len(result) == 1
    assert result[0].tense == 'past'

def test_yesterday_not_affected():
    result = parse_time_references('yesterday')
    assert len(result) == 1
    assert result[0].frame == 'day'
    assert result[0].tense == 'past'

def test_tomorrow_not_affected():
    result = parse_time_references('tomorrow')
    assert len(result) == 1
    assert result[0].tense == 'future'

def test_today_not_affected():
    result = parse_time_references('today')
    assert len(result) == 1
    assert result[0].tense == 'present'

def test_float_single_unit_not_affected():
    result = parse_time_references('7.2 days ago')
    assert len(result) == 1
    assert result[0].cardinality == 7


# =============================================================================
# Section 26: Decade unit in compound expressions
# =============================================================================

def test_decade_two_unit_past():
    result = parse_time_references('1 decade 2 years ago')
    assert len(result) == 2

def test_decade_two_unit_past_decade_frame():
    """KB stores decade as Frame='year' with cardinality*10; verify decade contribution."""
    result = parse_time_references('1 decade 2 years ago')
    # 1 decade → cardinality 10, frame year
    assert any(r.frame == 'year' and r.cardinality == 10 for r in result)

def test_decade_two_unit_past_both_past():
    result = parse_time_references('1 decade 2 years ago')
    assert all(r.tense == 'past' for r in result)

def test_decade_two_unit_future():
    result = parse_time_references('2 decades 5 years from now')
    assert len(result) == 2

def test_decade_two_unit_future_both_future():
    result = parse_time_references('2 decades 5 years from now')
    assert all(r.tense == 'future' for r in result)

def test_decade_three_unit_compound():
    result = parse_time_references('1 decade 2 years 6 months ago')
    assert len(result) == 3

def test_decade_three_unit_compound_all_past():
    result = parse_time_references('1 decade 2 years 6 months ago')
    assert all(r.tense == 'past' for r in result)

def test_decades_plural_compound():
    """2 decades → RelativeTime(20, 'year', 'past') in the KB."""
    result = parse_time_references('2 decades 3 years ago')
    assert any(r.frame == 'year' and r.cardinality == 20 for r in result)

def test_decade_in_prefix_compound():
    result = parse_time_references('in 1 decade 2 years')
    assert len(result) == 2
    assert all(r.tense == 'future' for r in result)

def test_decade_comma_compound():
    result = parse_time_references('1 decade, 3 years ago')
    assert len(result) == 2


# =============================================================================
# Section 27: Multiple compounds in one sentence (independent references)
# =============================================================================

def test_two_separate_compounds_total_count():
    """Two separate compound references in one sentence."""
    result = parse_time_references('started 1 year 2 months ago, ends in 3 months 2 weeks')
    # Should have at least 4 relative times
    assert len(result) >= 4

def test_two_separate_compounds_has_past():
    result = parse_time_references('started 1 year 2 months ago, ends in 3 months 2 weeks')
    past_units = [r for r in result if r.tense == 'past']
    assert len(past_units) >= 2

def test_two_separate_compounds_has_future():
    result = parse_time_references('started 1 year 2 months ago, ends in 3 months 2 weeks')
    future_units = [r for r in result if r.tense == 'future']
    assert len(future_units) >= 2


# =============================================================================
# Section 28: Specific cardinality values — varied magnitudes
# =============================================================================

def test_cardinality_1_year_11_months():
    result = parse_time_references('1 year 11 months ago')
    assert len(result) == 2

def test_cardinality_1_year_11_months_year():
    result = parse_time_references('1 year 11 months ago')
    year_units = [r for r in result if r.frame == 'year']
    assert year_units[0].cardinality == 1

def test_cardinality_1_year_11_months_month():
    result = parse_time_references('1 year 11 months ago')
    month_units = [r for r in result if r.frame == 'month']
    assert month_units[0].cardinality == 11

def test_cardinality_1_year_12_months():
    result = parse_time_references('1 year 12 months ago')
    assert len(result) == 2

def test_cardinality_1_year_12_months_month():
    result = parse_time_references('1 year 12 months ago')
    month_units = [r for r in result if r.frame == 'month']
    assert month_units[0].cardinality == 12

def test_cardinality_10_years_6_months():
    result = parse_time_references('10 years 6 months ago')
    year_units = [r for r in result if r.frame == 'year']
    assert year_units[0].cardinality == 10

def test_cardinality_zero_pad_09_months():
    """Leading zeros like '09 months' must parse correctly."""
    result = parse_time_references('1 year, 09 months ago')
    month_units = [r for r in result if r.frame == 'month']
    assert month_units[0].cardinality == 9

def test_cardinality_zero_pad_01_weeks():
    result = parse_time_references('1 year, 09 months, 01 weeks ago')
    week_units = [r for r in result if r.frame == 'week']
    assert week_units[0].cardinality == 1

def test_cardinality_50_years_compound():
    result = parse_time_references('50 years 6 months ago')
    year_units = [r for r in result if r.frame == 'year']
    assert year_units[0].cardinality == 50

def test_cardinality_5_minutes_30_seconds():
    result = parse_time_references('5 minutes 30 seconds ago')
    minute_units = [r for r in result if r.frame == 'minute']
    second_units = [r for r in result if r.frame == 'second']
    assert minute_units[0].cardinality == 5
    assert second_units[0].cardinality == 30


# =============================================================================
# Section 29: Frame values are correct strings
# =============================================================================

def test_frame_value_year():
    result = parse_time_references('1 year 2 months ago')
    year_units = [r for r in result if r.frame == 'year']
    assert year_units[0].frame == 'year'

def test_frame_value_month():
    result = parse_time_references('1 year 2 months ago')
    month_units = [r for r in result if r.frame == 'month']
    assert month_units[0].frame == 'month'

def test_frame_value_week():
    result = parse_time_references('2 weeks 3 days ago')
    week_units = [r for r in result if r.frame == 'week']
    assert week_units[0].frame == 'week'

def test_frame_value_day():
    result = parse_time_references('2 weeks 3 days ago')
    day_units = [r for r in result if r.frame == 'day']
    assert day_units[0].frame == 'day'

def test_frame_value_hour():
    result = parse_time_references('2 hours 30 minutes ago')
    hour_units = [r for r in result if r.frame == 'hour']
    assert hour_units[0].frame == 'hour'

def test_frame_value_minute():
    result = parse_time_references('2 hours 30 minutes ago')
    minute_units = [r for r in result if r.frame == 'minute']
    assert minute_units[0].frame == 'minute'

def test_frame_value_second():
    result = parse_time_references('5 minutes 45 seconds ago')
    second_units = [r for r in result if r.frame == 'second']
    assert second_units[0].frame == 'second'

def test_frame_value_decade():
    """KB stores decade as Frame='year'; verify both units are year-framed."""
    result = parse_time_references('1 decade 2 years ago')
    # both units stored as year (decade * 10, explicit year)
    assert all(r.frame == 'year' for r in result)


# =============================================================================
# Section 30: Tense values are correct strings
# =============================================================================

def test_tense_past_value():
    result = parse_time_references('1 year 2 months ago')
    for r in result:
        assert r.tense == 'past'

def test_tense_future_value():
    result = parse_time_references('1 year 2 months from now')
    for r in result:
        assert r.tense == 'future'

def test_tense_future_in_prefix():
    result = parse_time_references('in 1 year 2 months')
    for r in result:
        assert r.tense == 'future'

def test_tense_consistency_three_unit():
    result = parse_time_references('1 year 2 months 3 weeks ago')
    tenses = {r.tense for r in result}
    assert len(tenses) == 1  # all same tense

def test_tense_consistency_future_three_unit():
    result = parse_time_references('1 year 2 months 3 weeks from now')
    tenses = {r.tense for r in result}
    assert len(tenses) == 1

def test_tense_consistency_six_unit():
    result = parse_time_references('1 year, 1 month, 1 week, 1 day, 1 hour and 1 minute ago')
    tenses = {r.tense for r in result}
    assert len(tenses) == 1  # all past


# =============================================================================
# Section 31: extract_relative_times API with compound
# =============================================================================

def test_extract_relative_times_two_unit():
    result = extract_relative_times('1 year 2 months ago')
    assert len(result) == 2

def test_extract_relative_times_six_unit():
    result = extract_relative_times('1 year, 1 month, 1 week, 1 day, 1 hour and 1 minute ago')
    assert len(result) == 6

def test_extract_relative_times_future_compound():
    result = extract_relative_times('1 year 2 months from now')
    assert len(result) == 2

def test_extract_relative_times_in_prefix():
    result = extract_relative_times('in 1 year 2 months')
    assert len(result) == 2

def test_extract_relative_times_compound_in_sentence():
    result = extract_relative_times('I started here 1 year 2 months ago')
    year_units = [r for r in result if r.frame == 'year']
    assert len(year_units) == 1


# =============================================================================
# Section 32: Boundary and edge cases
# =============================================================================

def test_same_unit_repeated_not_compound():
    """'2 years 3 years ago' — ambiguous, at minimum doesn't crash."""
    result = parse_time_references('2 years 3 years ago')
    assert isinstance(result, list)

def test_compound_with_zero_cardinality():
    """'0 years 2 months ago' — edge case, 0 cardinality in compound."""
    result = parse_time_references('0 years 2 months ago')
    assert isinstance(result, list)

def test_compound_single_word_units():
    """Singular unit forms in compound: '1 year 1 month ago'."""
    result = parse_time_references('1 year 1 month ago')
    assert len(result) == 2

def test_compound_single_word_units_year():
    result = parse_time_references('1 year 1 month ago')
    year_units = [r for r in result if r.frame == 'year']
    assert year_units[0].cardinality == 1

def test_compound_single_word_units_month():
    result = parse_time_references('1 year 1 month ago')
    month_units = [r for r in result if r.frame == 'month']
    assert month_units[0].cardinality == 1

def test_compound_extra_whitespace():
    """Extra spaces between tokens should not break parsing."""
    result = parse_time_references('1 year  2 months ago')
    assert len(result) == 2

def test_empty_string_returns_empty():
    result = parse_time_references('')
    assert result == []

def test_compound_no_false_positive_on_plain_text():
    """Plain text without numbers shouldn't produce compound results."""
    result = parse_time_references('the quick brown fox')
    assert len(result) == 0


# =============================================================================
# Section 33: "from today" tense marker (synonym for "from now")
# =============================================================================

def test_from_today_two_unit_future():
    result = parse_time_references('1 year 2 months from today')
    assert len(result) == 2

def test_from_today_two_unit_both_future():
    result = parse_time_references('1 year 2 months from today')
    assert all(r.tense == 'future' for r in result)

def test_from_today_month_week():
    result = parse_time_references('3 months 2 weeks from today')
    assert len(result) == 2

def test_from_today_three_unit():
    result = parse_time_references('1 year 2 months 3 weeks from today')
    assert len(result) == 3


# =============================================================================
# Section 34: Varied cardinality magnitudes across units
# =============================================================================

def test_cardinality_magnitude_1_1():
    result = parse_time_references('1 year 1 month ago')
    assert len(result) == 2

def test_cardinality_magnitude_5_3():
    result = parse_time_references('5 years 3 months ago')
    year_units = [r for r in result if r.frame == 'year']
    assert year_units[0].cardinality == 5

def test_cardinality_magnitude_10_6():
    result = parse_time_references('10 years 6 months ago')
    year_units = [r for r in result if r.frame == 'year']
    assert year_units[0].cardinality == 10

def test_cardinality_magnitude_20_12():
    result = parse_time_references('20 years 12 months ago')
    year_units = [r for r in result if r.frame == 'year']
    assert year_units[0].cardinality == 20

def test_cardinality_magnitude_3_14():
    result = parse_time_references('3 months 14 days ago')
    day_units = [r for r in result if r.frame == 'day']
    assert day_units[0].cardinality == 14

def test_cardinality_magnitude_1_30():
    result = parse_time_references('1 month 30 days ago')
    day_units = [r for r in result if r.frame == 'day']
    assert day_units[0].cardinality == 30

def test_cardinality_magnitude_4_8():
    result = parse_time_references('4 weeks 8 hours ago')
    hour_units = [r for r in result if r.frame == 'hour']
    assert hour_units[0].cardinality == 8

def test_cardinality_magnitude_2_90():
    result = parse_time_references('2 hours 90 minutes ago')
    minute_units = [r for r in result if r.frame == 'minute']
    assert minute_units[0].cardinality == 90

def test_cardinality_magnitude_1_59():
    result = parse_time_references('1 minute 59 seconds ago')
    second_units = [r for r in result if r.frame == 'second']
    assert second_units[0].cardinality == 59


# =============================================================================
# Section 35: Consistency across APIs for same input
# =============================================================================

def test_api_consistency_parse_time_references():
    result = parse_time_references('1 year 2 months ago')
    assert len(result) == 2

def test_api_consistency_extract_relative_times():
    result = extract_relative_times('1 year 2 months ago')
    assert len(result) == 2

def test_api_consistency_extract_past_references():
    result = extract_past_references('1 year 2 months ago')
    assert len(result) == 2

def test_api_consistency_parse_dates():
    result = parse_dates('1 year 2 months ago')
    assert len(result.relative_times) == 2

def test_api_consistency_has_temporal_info():
    assert has_temporal_info('1 year 2 months ago') is True

def test_api_consistency_resolve_timedelta():
    result = resolve_to_timedelta('1 year 2 months ago')
    assert len(result) == 2

def test_api_consistency_future_parse_time_references():
    result = parse_time_references('1 year 2 months from now')
    assert len(result) == 2

def test_api_consistency_future_extract_relative_times():
    result = extract_relative_times('1 year 2 months from now')
    assert len(result) == 2

def test_api_consistency_future_extract_future_references():
    result = extract_future_references('1 year 2 months from now')
    assert len(result) == 2

def test_api_consistency_future_parse_dates():
    result = parse_dates('1 year 2 months from now')
    assert len(result.relative_times) == 2
