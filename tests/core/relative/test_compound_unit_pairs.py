#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Exhaustive unit-pair tests for Issue #20: Compound multi-unit expressions.

Systematically covers all meaningful 2-unit combinations across the 8 supported
units (second, minute, hour, day, week, month, year, decade) in both past and
future tenses. Also covers connector variations per pair.

Related GitHub Issue:
    #20 - Gap: compound multi-unit expressions not supported
    https://github.com/craigtrim/fast-parse-time/issues/20
"""

import pytest
from fast_parse_time import (
    parse_time_references,
    extract_past_references,
    extract_future_references,
    has_temporal_info,
)


# =============================================================================
# Section A: Exhaustive 2-unit past pairs — high-to-low unit order
#   Units: decade > year > month > week > day > hour > minute > second
#   All 28 unique descending pairs × count + tense assertions
# =============================================================================

# --- decade + year ---

def test_pair_decade_year_ago_count():
    result = parse_time_references('1 decade 2 years ago')
    assert len(result) == 2

def test_pair_decade_year_ago_decade():
    """KB stores 1 decade as RelativeTime(10, 'year', ...)."""
    result = parse_time_references('1 decade 2 years ago')
    assert any(r.frame == 'year' and r.cardinality == 10 for r in result)

def test_pair_decade_year_ago_year():
    result = parse_time_references('1 decade 2 years ago')
    assert any(r.frame == 'year' and r.cardinality == 2 for r in result)

def test_pair_decade_year_ago_tense():
    result = parse_time_references('1 decade 2 years ago')
    assert all(r.tense == 'past' for r in result)

# --- decade + month ---

def test_pair_decade_month_ago_count():
    result = parse_time_references('1 decade 6 months ago')
    assert len(result) == 2

def test_pair_decade_month_ago_decade():
    """KB stores 1 decade as RelativeTime(10, 'year', ...)."""
    result = parse_time_references('1 decade 6 months ago')
    assert any(r.frame == 'year' and r.cardinality == 10 for r in result)

def test_pair_decade_month_ago_month():
    result = parse_time_references('1 decade 6 months ago')
    assert any(r.frame == 'month' and r.cardinality == 6 for r in result)

def test_pair_decade_month_ago_tense():
    result = parse_time_references('1 decade 6 months ago')
    assert all(r.tense == 'past' for r in result)

# --- decade + week ---

def test_pair_decade_week_ago_count():
    result = parse_time_references('2 decades 3 weeks ago')
    assert len(result) == 2

def test_pair_decade_week_ago_decade():
    """KB stores 2 decades as RelativeTime(20, 'year', ...)."""
    result = parse_time_references('2 decades 3 weeks ago')
    assert any(r.frame == 'year' and r.cardinality == 20 for r in result)

def test_pair_decade_week_ago_week():
    result = parse_time_references('2 decades 3 weeks ago')
    assert any(r.frame == 'week' and r.cardinality == 3 for r in result)

# --- decade + day ---

def test_pair_decade_day_ago_count():
    result = parse_time_references('1 decade 10 days ago')
    assert len(result) == 2

def test_pair_decade_day_ago_decade():
    """KB stores 1 decade as RelativeTime(10, 'year', ...)."""
    result = parse_time_references('1 decade 10 days ago')
    assert any(r.frame == 'year' and r.cardinality == 10 for r in result)

def test_pair_decade_day_ago_day():
    result = parse_time_references('1 decade 10 days ago')
    assert any(r.frame == 'day' and r.cardinality == 10 for r in result)

# --- decade + hour ---

def test_pair_decade_hour_ago_count():
    result = parse_time_references('1 decade 5 hours ago')
    assert len(result) == 2

def test_pair_decade_hour_ago_tense():
    result = parse_time_references('1 decade 5 hours ago')
    assert all(r.tense == 'past' for r in result)

# --- decade + minute ---

def test_pair_decade_minute_ago_count():
    result = parse_time_references('1 decade 30 minutes ago')
    assert len(result) == 2

def test_pair_decade_minute_ago_tense():
    result = parse_time_references('1 decade 30 minutes ago')
    assert all(r.tense == 'past' for r in result)

# --- decade + second ---

def test_pair_decade_second_ago_count():
    result = parse_time_references('1 decade 45 seconds ago')
    assert len(result) == 2

def test_pair_decade_second_ago_tense():
    result = parse_time_references('1 decade 45 seconds ago')
    assert all(r.tense == 'past' for r in result)

# --- year + month ---

def test_pair_year_month_ago_count():
    result = parse_time_references('3 years 4 months ago')
    assert len(result) == 2

def test_pair_year_month_ago_year():
    result = parse_time_references('3 years 4 months ago')
    assert any(r.frame == 'year' and r.cardinality == 3 for r in result)

def test_pair_year_month_ago_month():
    result = parse_time_references('3 years 4 months ago')
    assert any(r.frame == 'month' and r.cardinality == 4 for r in result)

def test_pair_year_month_ago_tense():
    result = parse_time_references('3 years 4 months ago')
    assert all(r.tense == 'past' for r in result)

# --- year + week ---

def test_pair_year_week_ago_count():
    result = parse_time_references('2 years 6 weeks ago')
    assert len(result) == 2

def test_pair_year_week_ago_year():
    result = parse_time_references('2 years 6 weeks ago')
    assert any(r.frame == 'year' and r.cardinality == 2 for r in result)

def test_pair_year_week_ago_week():
    result = parse_time_references('2 years 6 weeks ago')
    assert any(r.frame == 'week' and r.cardinality == 6 for r in result)

# --- year + day ---

def test_pair_year_day_ago_count():
    result = parse_time_references('1 year 90 days ago')
    assert len(result) == 2

def test_pair_year_day_ago_day():
    result = parse_time_references('1 year 90 days ago')
    assert any(r.frame == 'day' and r.cardinality == 90 for r in result)

def test_pair_year_day_ago_tense():
    result = parse_time_references('1 year 90 days ago')
    assert all(r.tense == 'past' for r in result)

# --- year + hour ---

def test_pair_year_hour_ago_count():
    result = parse_time_references('1 year 12 hours ago')
    assert len(result) == 2

def test_pair_year_hour_ago_hour():
    result = parse_time_references('1 year 12 hours ago')
    assert any(r.frame == 'hour' and r.cardinality == 12 for r in result)

# --- year + minute ---

def test_pair_year_minute_ago_count():
    result = parse_time_references('2 years 45 minutes ago')
    assert len(result) == 2

def test_pair_year_minute_ago_tense():
    result = parse_time_references('2 years 45 minutes ago')
    assert all(r.tense == 'past' for r in result)

# --- year + second ---

def test_pair_year_second_ago_count():
    result = parse_time_references('1 year 120 seconds ago')
    assert len(result) == 2

def test_pair_year_second_ago_second():
    result = parse_time_references('1 year 120 seconds ago')
    assert any(r.frame == 'second' and r.cardinality == 120 for r in result)

# --- month + week ---

def test_pair_month_week_ago_count():
    result = parse_time_references('5 months 2 weeks ago')
    assert len(result) == 2

def test_pair_month_week_ago_month():
    result = parse_time_references('5 months 2 weeks ago')
    assert any(r.frame == 'month' and r.cardinality == 5 for r in result)

def test_pair_month_week_ago_week():
    result = parse_time_references('5 months 2 weeks ago')
    assert any(r.frame == 'week' and r.cardinality == 2 for r in result)

def test_pair_month_week_ago_tense():
    result = parse_time_references('5 months 2 weeks ago')
    assert all(r.tense == 'past' for r in result)

# --- month + day ---

def test_pair_month_day_ago_count():
    result = parse_time_references('2 months 20 days ago')
    assert len(result) == 2

def test_pair_month_day_ago_day():
    result = parse_time_references('2 months 20 days ago')
    assert any(r.frame == 'day' and r.cardinality == 20 for r in result)

# --- month + hour ---

def test_pair_month_hour_ago_count():
    result = parse_time_references('4 months 8 hours ago')
    assert len(result) == 2

def test_pair_month_hour_ago_tense():
    result = parse_time_references('4 months 8 hours ago')
    assert all(r.tense == 'past' for r in result)

# --- month + minute ---

def test_pair_month_minute_ago_count():
    result = parse_time_references('3 months 15 minutes ago')
    assert len(result) == 2

def test_pair_month_minute_ago_minute():
    result = parse_time_references('3 months 15 minutes ago')
    assert any(r.frame == 'minute' and r.cardinality == 15 for r in result)

# --- month + second ---

def test_pair_month_second_ago_count():
    result = parse_time_references('1 month 90 seconds ago')
    assert len(result) == 2

def test_pair_month_second_ago_tense():
    result = parse_time_references('1 month 90 seconds ago')
    assert all(r.tense == 'past' for r in result)

# --- week + day ---

def test_pair_week_day_ago_count():
    result = parse_time_references('3 weeks 5 days ago')
    assert len(result) == 2

def test_pair_week_day_ago_week():
    result = parse_time_references('3 weeks 5 days ago')
    assert any(r.frame == 'week' and r.cardinality == 3 for r in result)

def test_pair_week_day_ago_day():
    result = parse_time_references('3 weeks 5 days ago')
    assert any(r.frame == 'day' and r.cardinality == 5 for r in result)

def test_pair_week_day_ago_tense():
    result = parse_time_references('3 weeks 5 days ago')
    assert all(r.tense == 'past' for r in result)

# --- week + hour ---

def test_pair_week_hour_ago_count():
    result = parse_time_references('1 week 4 hours ago')
    assert len(result) == 2

def test_pair_week_hour_ago_hour():
    result = parse_time_references('1 week 4 hours ago')
    assert any(r.frame == 'hour' and r.cardinality == 4 for r in result)

# --- week + minute ---

def test_pair_week_minute_ago_count():
    result = parse_time_references('2 weeks 45 minutes ago')
    assert len(result) == 2

def test_pair_week_minute_ago_tense():
    result = parse_time_references('2 weeks 45 minutes ago')
    assert all(r.tense == 'past' for r in result)

# --- week + second ---

def test_pair_week_second_ago_count():
    result = parse_time_references('1 week 30 seconds ago')
    assert len(result) == 2

def test_pair_week_second_ago_tense():
    result = parse_time_references('1 week 30 seconds ago')
    assert all(r.tense == 'past' for r in result)

# --- day + hour ---

def test_pair_day_hour_ago_count():
    result = parse_time_references('5 days 12 hours ago')
    assert len(result) == 2

def test_pair_day_hour_ago_day():
    result = parse_time_references('5 days 12 hours ago')
    assert any(r.frame == 'day' and r.cardinality == 5 for r in result)

def test_pair_day_hour_ago_hour():
    result = parse_time_references('5 days 12 hours ago')
    assert any(r.frame == 'hour' and r.cardinality == 12 for r in result)

def test_pair_day_hour_ago_tense():
    result = parse_time_references('5 days 12 hours ago')
    assert all(r.tense == 'past' for r in result)

# --- day + minute ---

def test_pair_day_minute_ago_count():
    result = parse_time_references('3 days 20 minutes ago')
    assert len(result) == 2

def test_pair_day_minute_ago_minute():
    result = parse_time_references('3 days 20 minutes ago')
    assert any(r.frame == 'minute' and r.cardinality == 20 for r in result)

# --- day + second ---

def test_pair_day_second_ago_count():
    result = parse_time_references('2 days 45 seconds ago')
    assert len(result) == 2

def test_pair_day_second_ago_tense():
    result = parse_time_references('2 days 45 seconds ago')
    assert all(r.tense == 'past' for r in result)

# --- hour + minute ---

def test_pair_hour_minute_ago_count():
    result = parse_time_references('3 hours 45 minutes ago')
    assert len(result) == 2

def test_pair_hour_minute_ago_hour():
    result = parse_time_references('3 hours 45 minutes ago')
    assert any(r.frame == 'hour' and r.cardinality == 3 for r in result)

def test_pair_hour_minute_ago_minute():
    result = parse_time_references('3 hours 45 minutes ago')
    assert any(r.frame == 'minute' and r.cardinality == 45 for r in result)

def test_pair_hour_minute_ago_tense():
    result = parse_time_references('3 hours 45 minutes ago')
    assert all(r.tense == 'past' for r in result)

# --- hour + second ---

def test_pair_hour_second_ago_count():
    result = parse_time_references('1 hour 30 seconds ago')
    assert len(result) == 2

def test_pair_hour_second_ago_second():
    result = parse_time_references('1 hour 30 seconds ago')
    assert any(r.frame == 'second' and r.cardinality == 30 for r in result)

# --- minute + second ---

def test_pair_minute_second_ago_count():
    result = parse_time_references('10 minutes 20 seconds ago')
    assert len(result) == 2

def test_pair_minute_second_ago_minute():
    result = parse_time_references('10 minutes 20 seconds ago')
    assert any(r.frame == 'minute' and r.cardinality == 10 for r in result)

def test_pair_minute_second_ago_second():
    result = parse_time_references('10 minutes 20 seconds ago')
    assert any(r.frame == 'second' and r.cardinality == 20 for r in result)

def test_pair_minute_second_ago_tense():
    result = parse_time_references('10 minutes 20 seconds ago')
    assert all(r.tense == 'past' for r in result)


# =============================================================================
# Section B: Exhaustive 2-unit future pairs — "from now"
#   All 28 descending pairs × count + tense assertions
# =============================================================================

def test_pair_future_decade_year_count():
    result = parse_time_references('1 decade 2 years from now')
    assert len(result) == 2

def test_pair_future_decade_year_tense():
    result = parse_time_references('1 decade 2 years from now')
    assert all(r.tense == 'future' for r in result)

def test_pair_future_decade_month_count():
    result = parse_time_references('1 decade 6 months from now')
    assert len(result) == 2

def test_pair_future_decade_month_tense():
    result = parse_time_references('1 decade 6 months from now')
    assert all(r.tense == 'future' for r in result)

def test_pair_future_decade_week_count():
    result = parse_time_references('2 decades 3 weeks from now')
    assert len(result) == 2

def test_pair_future_decade_week_tense():
    result = parse_time_references('2 decades 3 weeks from now')
    assert all(r.tense == 'future' for r in result)

def test_pair_future_decade_day_count():
    result = parse_time_references('1 decade 10 days from now')
    assert len(result) == 2

def test_pair_future_decade_day_tense():
    result = parse_time_references('1 decade 10 days from now')
    assert all(r.tense == 'future' for r in result)

def test_pair_future_decade_hour_count():
    result = parse_time_references('1 decade 5 hours from now')
    assert len(result) == 2

def test_pair_future_decade_minute_count():
    result = parse_time_references('1 decade 30 minutes from now')
    assert len(result) == 2

def test_pair_future_decade_second_count():
    result = parse_time_references('1 decade 45 seconds from now')
    assert len(result) == 2

def test_pair_future_year_month_count():
    result = parse_time_references('3 years 4 months from now')
    assert len(result) == 2

def test_pair_future_year_month_tense():
    result = parse_time_references('3 years 4 months from now')
    assert all(r.tense == 'future' for r in result)

def test_pair_future_year_month_year():
    result = parse_time_references('3 years 4 months from now')
    assert any(r.frame == 'year' and r.cardinality == 3 for r in result)

def test_pair_future_year_month_month():
    result = parse_time_references('3 years 4 months from now')
    assert any(r.frame == 'month' and r.cardinality == 4 for r in result)

def test_pair_future_year_week_count():
    result = parse_time_references('2 years 6 weeks from now')
    assert len(result) == 2

def test_pair_future_year_week_tense():
    result = parse_time_references('2 years 6 weeks from now')
    assert all(r.tense == 'future' for r in result)

def test_pair_future_year_day_count():
    result = parse_time_references('1 year 90 days from now')
    assert len(result) == 2

def test_pair_future_year_hour_count():
    result = parse_time_references('1 year 12 hours from now')
    assert len(result) == 2

def test_pair_future_year_minute_count():
    result = parse_time_references('2 years 45 minutes from now')
    assert len(result) == 2

def test_pair_future_year_second_count():
    result = parse_time_references('1 year 120 seconds from now')
    assert len(result) == 2

def test_pair_future_month_week_count():
    result = parse_time_references('5 months 2 weeks from now')
    assert len(result) == 2

def test_pair_future_month_week_tense():
    result = parse_time_references('5 months 2 weeks from now')
    assert all(r.tense == 'future' for r in result)

def test_pair_future_month_day_count():
    result = parse_time_references('2 months 20 days from now')
    assert len(result) == 2

def test_pair_future_month_hour_count():
    result = parse_time_references('4 months 8 hours from now')
    assert len(result) == 2

def test_pair_future_month_minute_count():
    result = parse_time_references('3 months 15 minutes from now')
    assert len(result) == 2

def test_pair_future_month_second_count():
    result = parse_time_references('1 month 90 seconds from now')
    assert len(result) == 2

def test_pair_future_week_day_count():
    result = parse_time_references('3 weeks 5 days from now')
    assert len(result) == 2

def test_pair_future_week_day_tense():
    result = parse_time_references('3 weeks 5 days from now')
    assert all(r.tense == 'future' for r in result)

def test_pair_future_week_hour_count():
    result = parse_time_references('1 week 4 hours from now')
    assert len(result) == 2

def test_pair_future_week_minute_count():
    result = parse_time_references('2 weeks 45 minutes from now')
    assert len(result) == 2

def test_pair_future_week_second_count():
    result = parse_time_references('1 week 30 seconds from now')
    assert len(result) == 2

def test_pair_future_day_hour_count():
    result = parse_time_references('5 days 12 hours from now')
    assert len(result) == 2

def test_pair_future_day_hour_tense():
    result = parse_time_references('5 days 12 hours from now')
    assert all(r.tense == 'future' for r in result)

def test_pair_future_day_minute_count():
    result = parse_time_references('3 days 20 minutes from now')
    assert len(result) == 2

def test_pair_future_day_second_count():
    result = parse_time_references('2 days 45 seconds from now')
    assert len(result) == 2

def test_pair_future_hour_minute_count():
    result = parse_time_references('3 hours 45 minutes from now')
    assert len(result) == 2

def test_pair_future_hour_minute_tense():
    result = parse_time_references('3 hours 45 minutes from now')
    assert all(r.tense == 'future' for r in result)

def test_pair_future_hour_second_count():
    result = parse_time_references('1 hour 30 seconds from now')
    assert len(result) == 2

def test_pair_future_minute_second_count():
    result = parse_time_references('10 minutes 20 seconds from now')
    assert len(result) == 2

def test_pair_future_minute_second_tense():
    result = parse_time_references('10 minutes 20 seconds from now')
    assert all(r.tense == 'future' for r in result)


# =============================================================================
# Section C: Connector variations for key pairs — past
# =============================================================================

# year + month across all 4 connectors

def test_connector_space_year_month_ago():
    result = parse_time_references('1 year 2 months ago')
    assert len(result) == 2 and all(r.tense == 'past' for r in result)

def test_connector_comma_year_month_ago():
    result = parse_time_references('1 year, 2 months ago')
    assert len(result) == 2 and all(r.tense == 'past' for r in result)

def test_connector_and_year_month_ago():
    result = parse_time_references('1 year and 2 months ago')
    assert len(result) == 2 and all(r.tense == 'past' for r in result)

def test_connector_comma_and_year_month_ago():
    result = parse_time_references('1 year, and 2 months ago')
    assert len(result) == 2 and all(r.tense == 'past' for r in result)

# week + day across all 4 connectors

def test_connector_space_week_day_ago():
    result = parse_time_references('2 weeks 3 days ago')
    assert len(result) == 2

def test_connector_comma_week_day_ago():
    result = parse_time_references('2 weeks, 3 days ago')
    assert len(result) == 2

def test_connector_and_week_day_ago():
    result = parse_time_references('2 weeks and 3 days ago')
    assert len(result) == 2

def test_connector_comma_and_week_day_ago():
    result = parse_time_references('2 weeks, and 3 days ago')
    assert len(result) == 2

# hour + minute across all 4 connectors

def test_connector_space_hour_minute_ago():
    result = parse_time_references('2 hours 30 minutes ago')
    assert len(result) == 2

def test_connector_comma_hour_minute_ago():
    result = parse_time_references('2 hours, 30 minutes ago')
    assert len(result) == 2

def test_connector_and_hour_minute_ago():
    result = parse_time_references('2 hours and 30 minutes ago')
    assert len(result) == 2

def test_connector_comma_and_hour_minute_ago():
    result = parse_time_references('2 hours, and 30 minutes ago')
    assert len(result) == 2


# =============================================================================
# Section D: Connector variations for key pairs — future
# =============================================================================

def test_connector_space_year_month_from_now():
    result = parse_time_references('1 year 2 months from now')
    assert len(result) == 2 and all(r.tense == 'future' for r in result)

def test_connector_comma_year_month_from_now():
    result = parse_time_references('1 year, 2 months from now')
    assert len(result) == 2 and all(r.tense == 'future' for r in result)

def test_connector_and_year_month_from_now():
    result = parse_time_references('1 year and 2 months from now')
    assert len(result) == 2 and all(r.tense == 'future' for r in result)

def test_connector_comma_and_year_month_from_now():
    result = parse_time_references('1 year, and 2 months from now')
    assert len(result) == 2 and all(r.tense == 'future' for r in result)

def test_connector_space_week_day_from_now():
    result = parse_time_references('2 weeks 3 days from now')
    assert len(result) == 2 and all(r.tense == 'future' for r in result)

def test_connector_comma_week_day_from_now():
    result = parse_time_references('2 weeks, 3 days from now')
    assert len(result) == 2

def test_connector_and_week_day_from_now():
    result = parse_time_references('2 weeks and 3 days from now')
    assert len(result) == 2

def test_connector_space_hour_minute_from_now():
    result = parse_time_references('2 hours 30 minutes from now')
    assert len(result) == 2 and all(r.tense == 'future' for r in result)

def test_connector_and_hour_minute_from_now():
    result = parse_time_references('2 hours and 30 minutes from now')
    assert len(result) == 2


# =============================================================================
# Section E: "In" prefix for all major pairs
# =============================================================================

def test_in_prefix_decade_year():
    result = parse_time_references('in 1 decade 2 years')
    assert len(result) == 2 and all(r.tense == 'future' for r in result)

def test_in_prefix_year_month():
    result = parse_time_references('in 3 years 4 months')
    assert len(result) == 2 and all(r.tense == 'future' for r in result)

def test_in_prefix_year_week():
    result = parse_time_references('in 2 years 6 weeks')
    assert len(result) == 2 and all(r.tense == 'future' for r in result)

def test_in_prefix_year_day():
    result = parse_time_references('in 1 year 90 days')
    assert len(result) == 2 and all(r.tense == 'future' for r in result)

def test_in_prefix_month_week():
    result = parse_time_references('in 5 months 2 weeks')
    assert len(result) == 2 and all(r.tense == 'future' for r in result)

def test_in_prefix_month_day():
    result = parse_time_references('in 2 months 20 days')
    assert len(result) == 2 and all(r.tense == 'future' for r in result)

def test_in_prefix_week_day():
    result = parse_time_references('in 3 weeks 5 days')
    assert len(result) == 2 and all(r.tense == 'future' for r in result)

def test_in_prefix_day_hour():
    result = parse_time_references('in 5 days 12 hours')
    assert len(result) == 2 and all(r.tense == 'future' for r in result)

def test_in_prefix_hour_minute():
    result = parse_time_references('in 3 hours 45 minutes')
    assert len(result) == 2 and all(r.tense == 'future' for r in result)

def test_in_prefix_minute_second():
    result = parse_time_references('in 10 minutes 20 seconds')
    assert len(result) == 2 and all(r.tense == 'future' for r in result)

def test_in_prefix_week_hour():
    result = parse_time_references('in 1 week 4 hours')
    assert len(result) == 2 and all(r.tense == 'future' for r in result)

def test_in_prefix_month_hour():
    result = parse_time_references('in 4 months 8 hours')
    assert len(result) == 2 and all(r.tense == 'future' for r in result)

def test_in_prefix_year_hour():
    result = parse_time_references('in 1 year 12 hours')
    assert len(result) == 2 and all(r.tense == 'future' for r in result)


# =============================================================================
# Section F: "Back" tense marker for all major pairs
# =============================================================================

def test_back_decade_year():
    result = parse_time_references('1 decade 2 years back')
    assert len(result) == 2 and all(r.tense == 'past' for r in result)

def test_back_year_month():
    result = parse_time_references('3 years 4 months back')
    assert len(result) == 2 and all(r.tense == 'past' for r in result)

def test_back_year_week():
    result = parse_time_references('2 years 6 weeks back')
    assert len(result) == 2 and all(r.tense == 'past' for r in result)

def test_back_year_day():
    result = parse_time_references('1 year 90 days back')
    assert len(result) == 2 and all(r.tense == 'past' for r in result)

def test_back_month_week():
    result = parse_time_references('5 months 2 weeks back')
    assert len(result) == 2 and all(r.tense == 'past' for r in result)

def test_back_week_day():
    result = parse_time_references('3 weeks 5 days back')
    assert len(result) == 2 and all(r.tense == 'past' for r in result)

def test_back_day_hour():
    result = parse_time_references('5 days 12 hours back')
    assert len(result) == 2 and all(r.tense == 'past' for r in result)

def test_back_hour_minute():
    result = parse_time_references('3 hours 45 minutes back')
    assert len(result) == 2 and all(r.tense == 'past' for r in result)

def test_back_minute_second():
    result = parse_time_references('10 minutes 20 seconds back')
    assert len(result) == 2 and all(r.tense == 'past' for r in result)

def test_back_month_day():
    result = parse_time_references('2 months 20 days back')
    assert len(result) == 2 and all(r.tense == 'past' for r in result)

def test_back_month_hour():
    result = parse_time_references('4 months 8 hours back')
    assert len(result) == 2 and all(r.tense == 'past' for r in result)

def test_back_year_hour():
    result = parse_time_references('1 year 12 hours back')
    assert len(result) == 2 and all(r.tense == 'past' for r in result)


# =============================================================================
# Section G: has_temporal_info for key pairs
# =============================================================================

def test_has_info_decade_year_ago():
    assert has_temporal_info('1 decade 2 years ago') is True

def test_has_info_year_month_ago():
    assert has_temporal_info('3 years 4 months ago') is True

def test_has_info_month_week_ago():
    assert has_temporal_info('5 months 2 weeks ago') is True

def test_has_info_week_day_ago():
    assert has_temporal_info('3 weeks 5 days ago') is True

def test_has_info_day_hour_ago():
    assert has_temporal_info('5 days 12 hours ago') is True

def test_has_info_hour_minute_ago():
    assert has_temporal_info('3 hours 45 minutes ago') is True

def test_has_info_minute_second_ago():
    assert has_temporal_info('10 minutes 20 seconds ago') is True

def test_has_info_year_month_from_now():
    assert has_temporal_info('3 years 4 months from now') is True

def test_has_info_hour_minute_from_now():
    assert has_temporal_info('3 hours 45 minutes from now') is True

def test_has_info_in_year_month():
    assert has_temporal_info('in 3 years 4 months') is True

def test_has_info_three_unit():
    assert has_temporal_info('1 year 2 months 3 weeks ago') is True

def test_has_info_six_unit():
    assert has_temporal_info('1 year, 1 month, 1 week, 1 day, 1 hour and 1 minute ago') is True


# =============================================================================
# Section H: extract_past_references for key pairs
# =============================================================================

def test_extract_past_decade_year():
    result = extract_past_references('1 decade 2 years ago')
    assert len(result) == 2

def test_extract_past_year_month():
    result = extract_past_references('3 years 4 months ago')
    assert len(result) == 2

def test_extract_past_month_week():
    result = extract_past_references('5 months 2 weeks ago')
    assert len(result) == 2

def test_extract_past_week_day():
    result = extract_past_references('3 weeks 5 days ago')
    assert len(result) == 2

def test_extract_past_day_hour():
    result = extract_past_references('5 days 12 hours ago')
    assert len(result) == 2

def test_extract_past_hour_minute():
    result = extract_past_references('3 hours 45 minutes ago')
    assert len(result) == 2

def test_extract_past_minute_second():
    result = extract_past_references('10 minutes 20 seconds ago')
    assert len(result) == 2

def test_extract_past_three_unit():
    result = extract_past_references('1 year 2 months 3 weeks ago')
    assert len(result) == 3

def test_extract_past_four_unit():
    result = extract_past_references('1 year 2 months 3 weeks 4 days ago')
    assert len(result) == 4


# =============================================================================
# Section I: extract_future_references for key pairs
# =============================================================================

def test_extract_future_decade_year():
    result = extract_future_references('1 decade 2 years from now')
    assert len(result) == 2

def test_extract_future_year_month():
    result = extract_future_references('3 years 4 months from now')
    assert len(result) == 2

def test_extract_future_month_week():
    result = extract_future_references('5 months 2 weeks from now')
    assert len(result) == 2

def test_extract_future_week_day():
    result = extract_future_references('3 weeks 5 days from now')
    assert len(result) == 2

def test_extract_future_day_hour():
    result = extract_future_references('5 days 12 hours from now')
    assert len(result) == 2

def test_extract_future_hour_minute():
    result = extract_future_references('3 hours 45 minutes from now')
    assert len(result) == 2

def test_extract_future_minute_second():
    result = extract_future_references('10 minutes 20 seconds from now')
    assert len(result) == 2

def test_extract_future_in_prefix_year_month():
    result = extract_future_references('in 3 years 4 months')
    assert len(result) == 2

def test_extract_future_three_unit():
    result = extract_future_references('1 year 2 months 3 weeks from now')
    assert len(result) == 3
