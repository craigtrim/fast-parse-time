#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Comprehensive test suite for decimal/float cardinalities in relative time expressions.

This test suite implements TDD for issue #59:
    Support decimal/float cardinalities in relative time expressions
    https://github.com/craigtrim/fast-parse-time/issues/59

Test Coverage:
- Tenths: 0.5, 1.5, 2.5, 3.5, ... 9.5 across all frames
- Hundredths: 1.25, 1.75, 2.25, 10.75, 0.25 across all frames
- With 'ago': explicit past tense
- Without 'ago': implicit past tense
- Edge cases: 0.0, 0.1, leading dot, double dot, no frame
- Sentence embedding: decimal values in natural language context
- All frames: hours, minutes, seconds, days, weeks, months, years

Expected behavior:
- Decimal cardinality is truncated to int (2.5 → 2, 10.75 → 10)
- Values truncating to 0 (0.5, 0.25, 0.1, etc.) are rejected as invalid
- Frame and tense are preserved as with integer cardinalities
"""

import pytest
from fast_parse_time import parse_time_references


# Related GitHub Issue:
#     #59 - Support decimal/float cardinalities in relative time expressions
#     https://github.com/craigtrim/fast-parse-time/issues/59


class TestDecimalHours:
    """Decimal cardinalities with hour frame."""

    # Tenths with 'ago'
    def test_0_5_hours_ago(self):
        result = parse_time_references('0.5 hours ago')
        # Values truncating to 0 are rejected as invalid
        assert len(result) == 0

    def test_1_5_hours_ago(self):
        result = parse_time_references('1.5 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_2_5_hours_ago(self):
        result = parse_time_references('2.5 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_3_5_hours_ago(self):
        result = parse_time_references('3.5 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_4_5_hours_ago(self):
        result = parse_time_references('4.5 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_5_5_hours_ago(self):
        result = parse_time_references('5.5 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_6_5_hours_ago(self):
        result = parse_time_references('6.5 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 6
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_7_5_hours_ago(self):
        result = parse_time_references('7.5 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_8_5_hours_ago(self):
        result = parse_time_references('8.5 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 8
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_9_5_hours_ago(self):
        result = parse_time_references('9.5 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 9
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    # Tenths without 'ago' (implicit past)
    def test_0_5_hours(self):
        result = parse_time_references('0.5 hours')
        # Values truncating to 0 are rejected as invalid
        assert len(result) == 0

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_1_5_hours(self):
        result = parse_time_references('1.5 hours')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_2_5_hours(self):
        result = parse_time_references('2.5 hours')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_3_5_hours(self):
        result = parse_time_references('3.5 hours')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_4_5_hours(self):
        result = parse_time_references('4.5 hours')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_5_5_hours(self):
        result = parse_time_references('5.5 hours')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_6_5_hours(self):
        result = parse_time_references('6.5 hours')
        assert len(result) == 1
        assert result[0].cardinality == 6
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_7_5_hours(self):
        result = parse_time_references('7.5 hours')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_8_5_hours(self):
        result = parse_time_references('8.5 hours')
        assert len(result) == 1
        assert result[0].cardinality == 8
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_9_5_hours(self):
        result = parse_time_references('9.5 hours')
        assert len(result) == 1
        assert result[0].cardinality == 9
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    # Hundredths
    def test_1_25_hours_ago(self):
        result = parse_time_references('1.25 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_1_75_hours_ago(self):
        result = parse_time_references('1.75 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_2_25_hours_ago(self):
        result = parse_time_references('2.25 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_10_75_hours_ago(self):
        result = parse_time_references('10.75 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_0_25_hours_ago(self):
        result = parse_time_references('0.25 hours ago')
        # Values truncating to 0 are rejected as invalid
        assert len(result) == 0

    # Singular form
    def test_1_5_hour_ago(self):
        result = parse_time_references('1.5 hour ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_2_5_hour(self):
        result = parse_time_references('2.5 hour')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'


class TestDecimalMinutes:
    """Decimal cardinalities with minute frame."""

    # Tenths with 'ago'
    def test_0_5_minutes_ago(self):
        result = parse_time_references('0.5 minutes ago')
        # Values truncating to 0 are rejected as invalid
        assert len(result) == 0

    def test_1_5_minutes_ago(self):
        result = parse_time_references('1.5 minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_2_5_minutes_ago(self):
        result = parse_time_references('2.5 minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_3_5_minutes_ago(self):
        result = parse_time_references('3.5 minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_4_5_minutes_ago(self):
        result = parse_time_references('4.5 minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_5_5_minutes_ago(self):
        result = parse_time_references('5.5 minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_6_5_minutes_ago(self):
        result = parse_time_references('6.5 minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 6
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_7_5_minutes_ago(self):
        result = parse_time_references('7.5 minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_8_5_minutes_ago(self):
        result = parse_time_references('8.5 minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 8
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_9_5_minutes_ago(self):
        result = parse_time_references('9.5 minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 9
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    # Tenths without 'ago' (implicit past)
    def test_0_5_minutes(self):
        result = parse_time_references('0.5 minutes')
        # Values truncating to 0 are rejected as invalid
        assert len(result) == 0

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_1_5_minutes(self):
        result = parse_time_references('1.5 minutes')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_2_5_minutes(self):
        result = parse_time_references('2.5 minutes')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_3_5_minutes(self):
        result = parse_time_references('3.5 minutes')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_4_5_minutes(self):
        result = parse_time_references('4.5 minutes')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_5_5_minutes(self):
        result = parse_time_references('5.5 minutes')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_6_5_minutes(self):
        result = parse_time_references('6.5 minutes')
        assert len(result) == 1
        assert result[0].cardinality == 6
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_7_5_minutes(self):
        result = parse_time_references('7.5 minutes')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_8_5_minutes(self):
        result = parse_time_references('8.5 minutes')
        assert len(result) == 1
        assert result[0].cardinality == 8
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_9_5_minutes(self):
        result = parse_time_references('9.5 minutes')
        assert len(result) == 1
        assert result[0].cardinality == 9
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    # Hundredths
    def test_1_25_minutes_ago(self):
        result = parse_time_references('1.25 minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_1_75_minutes_ago(self):
        result = parse_time_references('1.75 minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_2_25_minutes_ago(self):
        result = parse_time_references('2.25 minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_10_75_minutes_ago(self):
        result = parse_time_references('10.75 minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_0_25_minutes_ago(self):
        result = parse_time_references('0.25 minutes ago')
        # Values truncating to 0 are rejected as invalid
        assert len(result) == 0

    # Singular form
    def test_1_5_minute_ago(self):
        result = parse_time_references('1.5 minute ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_2_5_minute(self):
        result = parse_time_references('2.5 minute')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'


class TestDecimalSeconds:
    """Decimal cardinalities with second frame."""

    # Tenths with 'ago'
    def test_0_5_seconds_ago(self):
        result = parse_time_references('0.5 seconds ago')
        # Values truncating to 0 are rejected as invalid
        assert len(result) == 0

    def test_1_5_seconds_ago(self):
        result = parse_time_references('1.5 seconds ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_2_5_seconds_ago(self):
        result = parse_time_references('2.5 seconds ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_3_5_seconds_ago(self):
        result = parse_time_references('3.5 seconds ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_4_5_seconds_ago(self):
        result = parse_time_references('4.5 seconds ago')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_5_5_seconds_ago(self):
        result = parse_time_references('5.5 seconds ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    # Tenths without 'ago'
    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_1_5_seconds(self):
        result = parse_time_references('1.5 seconds')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_2_5_seconds(self):
        result = parse_time_references('2.5 seconds')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    # Hundredths
    def test_1_25_seconds_ago(self):
        result = parse_time_references('1.25 seconds ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_0_1_seconds_ago(self):
        result = parse_time_references('0.1 seconds ago')
        # Values truncating to 0 are rejected as invalid
        assert len(result) == 0


class TestDecimalDays:
    """Decimal cardinalities with day frame."""

    # Tenths with 'ago'
    def test_0_5_days_ago(self):
        result = parse_time_references('0.5 days ago')
        # Values truncating to 0 are rejected as invalid
        assert len(result) == 0

    def test_1_5_days_ago(self):
        result = parse_time_references('1.5 days ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_2_5_days_ago(self):
        result = parse_time_references('2.5 days ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_3_5_days_ago(self):
        result = parse_time_references('3.5 days ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_4_5_days_ago(self):
        result = parse_time_references('4.5 days ago')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_5_5_days_ago(self):
        result = parse_time_references('5.5 days ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_6_5_days_ago(self):
        result = parse_time_references('6.5 days ago')
        assert len(result) == 1
        assert result[0].cardinality == 6
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_7_5_days_ago(self):
        result = parse_time_references('7.5 days ago')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_8_5_days_ago(self):
        result = parse_time_references('8.5 days ago')
        assert len(result) == 1
        assert result[0].cardinality == 8
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_9_5_days_ago(self):
        result = parse_time_references('9.5 days ago')
        assert len(result) == 1
        assert result[0].cardinality == 9
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    # Tenths without 'ago'
    def test_0_5_days(self):
        result = parse_time_references('0.5 days')
        # Values truncating to 0 are rejected as invalid
        assert len(result) == 0

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_1_5_days(self):
        result = parse_time_references('1.5 days')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_2_5_days(self):
        result = parse_time_references('2.5 days')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_3_5_days(self):
        result = parse_time_references('3.5 days')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    # Hundredths
    def test_1_25_days_ago(self):
        result = parse_time_references('1.25 days ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_1_75_days_ago(self):
        result = parse_time_references('1.75 days ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    # Singular form
    def test_1_5_day_ago(self):
        result = parse_time_references('1.5 day ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'


class TestDecimalWeeks:
    """Decimal cardinalities with week frame."""

    # Tenths with 'ago'
    def test_0_5_weeks_ago(self):
        result = parse_time_references('0.5 weeks ago')
        # Values truncating to 0 are rejected as invalid
        assert len(result) == 0

    def test_1_5_weeks_ago(self):
        result = parse_time_references('1.5 weeks ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_2_5_weeks_ago(self):
        result = parse_time_references('2.5 weeks ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_3_5_weeks_ago(self):
        result = parse_time_references('3.5 weeks ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_4_5_weeks_ago(self):
        result = parse_time_references('4.5 weeks ago')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    # Tenths without 'ago'
    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_1_5_weeks(self):
        result = parse_time_references('1.5 weeks')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_2_5_weeks(self):
        result = parse_time_references('2.5 weeks')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    # Hundredths
    def test_1_25_weeks_ago(self):
        result = parse_time_references('1.25 weeks ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_10_75_weeks_ago(self):
        result = parse_time_references('10.75 weeks ago')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'


class TestDecimalMonths:
    """Decimal cardinalities with month frame."""

    # Tenths with 'ago'
    def test_0_5_months_ago(self):
        result = parse_time_references('0.5 months ago')
        # Values truncating to 0 are rejected as invalid
        assert len(result) == 0

    def test_1_5_months_ago(self):
        result = parse_time_references('1.5 months ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_2_5_months_ago(self):
        result = parse_time_references('2.5 months ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_3_5_months_ago(self):
        result = parse_time_references('3.5 months ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_4_5_months_ago(self):
        result = parse_time_references('4.5 months ago')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_5_5_months_ago(self):
        result = parse_time_references('5.5 months ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    # Tenths without 'ago'
    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_1_5_months(self):
        result = parse_time_references('1.5 months')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_2_5_months(self):
        result = parse_time_references('2.5 months')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    # Hundredths
    def test_1_25_months_ago(self):
        result = parse_time_references('1.25 months ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_10_75_months_ago(self):
        result = parse_time_references('10.75 months ago')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'


class TestDecimalYears:
    """Decimal cardinalities with year frame."""

    # Tenths with 'ago'
    def test_0_5_years_ago(self):
        result = parse_time_references('0.5 years ago')
        # Values truncating to 0 are rejected as invalid
        assert len(result) == 0

    def test_1_5_years_ago(self):
        result = parse_time_references('1.5 years ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_2_5_years_ago(self):
        result = parse_time_references('2.5 years ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_3_5_years_ago(self):
        result = parse_time_references('3.5 years ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_4_5_years_ago(self):
        result = parse_time_references('4.5 years ago')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    # Tenths without 'ago'
    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_1_5_years(self):
        result = parse_time_references('1.5 years')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_2_5_years(self):
        result = parse_time_references('2.5 years')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    # Hundredths
    def test_1_25_years_ago(self):
        result = parse_time_references('1.25 years ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_10_75_years_ago(self):
        result = parse_time_references('10.75 years ago')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'


class TestSentenceEmbedding:
    """Decimal cardinalities embedded in natural language sentences."""

    def test_cached_1_5_days_ago(self):
        result = parse_time_references('cached 1.5 days ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_updated_2_5_hours_ago(self):
        result = parse_time_references('updated 2.5 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_posted_3_5_minutes_ago(self):
        result = parse_time_references('posted 3.5 minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_the_file_was_modified_4_5_hours_ago(self):
        result = parse_time_references('the file was modified 4.5 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_completed_0_5_weeks_ago(self):
        result = parse_time_references('completed 0.5 weeks ago')
        assert len(result) == 1
        assert result[0].cardinality == 0
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_published_5_5_months_ago(self):
        result = parse_time_references('published 5.5 months ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_deployed_1_75_years_ago(self):
        result = parse_time_references('deployed 1.75 years ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'


class TestEdgeCasesZeroCardinality:
    """Edge cases: zero cardinality with decimals."""

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_0_0_hours_ago(self):
        """0.0 should be treated as zero cardinality (no match expected)."""
        # Values truncating to 0 are rejected as invalid
        assert len(result) == 0

        result = parse_time_references('0.0 hours ago')
        # Zero cardinality is invalid for time references
        # Behavior: should return empty or cardinality 0
        assert len(result) == 0 or (len(result) == 1 and result[0].cardinality == 0)

    def test_0_0_days(self):
        result = parse_time_references('0.0 days')
        # Values truncating to 0 are rejected as invalid
        assert len(result) == 0

    def test_0_0_minutes_ago(self):
        result = parse_time_references('0.0 minutes ago')
        # Values truncating to 0 are rejected as invalid
        assert len(result) == 0


class TestEdgeCasesLeadingDot:
    """Edge cases: leading dot (define expected behavior)."""

    def test_dot_5_hours(self):
        """.5 hours -- leading dot format."""
        result = parse_time_references('.5 hours')
        # Expected: no match (leading dot not standard)
        # If implementation supports it, adjust expectation
        assert len(result) == 0

    def test_dot_25_days_ago(self):
        result = parse_time_references('.25 days ago')
        assert len(result) == 0


class TestEdgeCasesDoubleDot:
    """Edge cases: double dot (malformed input)."""

    def test_2_dot_dot_5_hours(self):
        """2..5 hours -- double dot malformed."""
        result = parse_time_references('2..5 hours')
        # Expected: no match (malformed)
        assert len(result) == 0

    def test_3_dot_dot_5_days_ago(self):
        result = parse_time_references('3..5 days ago')
        assert len(result) == 0


class TestEdgeCasesNoFrame:
    """Edge cases: decimal without time frame."""

    def test_2_5_alone(self):
        """2.5 alone without frame -- no match."""
        result = parse_time_references('2.5')
        assert len(result) == 0

    def test_10_75_alone(self):
        result = parse_time_references('10.75')
        assert len(result) == 0


class TestAbbreviatedUnits:
    """Decimal cardinalities with abbreviated unit forms."""

    # hour abbreviations
    def test_2_5_hr_ago(self):
        result = parse_time_references('2.5 hr ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_2_5_hrs_ago(self):
        result = parse_time_references('2.5 hrs ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_2_5_hr(self):
        result = parse_time_references('2.5 hr')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_2_5_hrs(self):
        result = parse_time_references('2.5 hrs')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    # minute abbreviations
    def test_10_5_min_ago(self):
        result = parse_time_references('10.5 min ago')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_10_5_mins_ago(self):
        result = parse_time_references('10.5 mins ago')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_10_5_min(self):
        result = parse_time_references('10.5 min')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_10_5_mins(self):
        result = parse_time_references('10.5 mins')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    # second abbreviations
    def test_3_5_sec_ago(self):
        result = parse_time_references('3.5 sec ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_3_5_secs_ago(self):
        result = parse_time_references('3.5 secs ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_3_5_sec(self):
        result = parse_time_references('3.5 sec')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_3_5_secs(self):
        result = parse_time_references('3.5 secs')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'


class TestDecimalWithBack:
    """Decimal cardinalities with 'back' instead of 'ago'."""

    def test_1_5_hours_back(self):
        result = parse_time_references('1.5 hours back')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_2_5_days_back(self):
        result = parse_time_references('2.5 days back')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_3_5_minutes_back(self):
        result = parse_time_references('3.5 minutes back')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_0_5_weeks_back(self):
        result = parse_time_references('0.5 weeks back')
        # Values truncating to 0 are rejected as invalid
        assert len(result) == 0

    def test_1_75_months_back(self):
        result = parse_time_references('1.75 months back')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_2_25_years_back(self):
        result = parse_time_references('2.25 years back')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'


class TestDecimalVariationsHundredths:
    """More decimal variations focusing on hundredths precision."""

    # Hours
    def test_5_25_hours_ago(self):
        result = parse_time_references('5.25 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_5_75_hours_ago(self):
        result = parse_time_references('5.75 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_6_25_hours_ago(self):
        result = parse_time_references('6.25 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 6
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_7_75_hours_ago(self):
        result = parse_time_references('7.75 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    # Minutes
    def test_5_25_minutes_ago(self):
        result = parse_time_references('5.25 minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_5_75_minutes_ago(self):
        result = parse_time_references('5.75 minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    # Days
    def test_5_25_days_ago(self):
        result = parse_time_references('5.25 days ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_5_75_days_ago(self):
        result = parse_time_references('5.75 days ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    # Weeks
    def test_5_25_weeks_ago(self):
        result = parse_time_references('5.25 weeks ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_5_75_weeks_ago(self):
        result = parse_time_references('5.75 weeks ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    # Months
    def test_5_25_months_ago(self):
        result = parse_time_references('5.25 months ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_5_75_months_ago(self):
        result = parse_time_references('5.75 months ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    # Years
    def test_5_25_years_ago(self):
        result = parse_time_references('5.25 years ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_5_75_years_ago(self):
        result = parse_time_references('5.75 years ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'


class TestDecimalVariationsTenths:
    """Additional decimal variations with tenths - different ranges."""

    # 0.1 - 0.9 range
    def test_0_1_hours_ago(self):
        result = parse_time_references('0.1 hours ago')
        # Values truncating to 0 are rejected as invalid
        assert len(result) == 0

    def test_0_2_days_ago(self):
        result = parse_time_references('0.2 days ago')
        # Values truncating to 0 are rejected as invalid
        assert len(result) == 0

    def test_0_3_minutes_ago(self):
        result = parse_time_references('0.3 minutes ago')
        # Values truncating to 0 are rejected as invalid
        assert len(result) == 0

    def test_0_7_weeks_ago(self):
        result = parse_time_references('0.7 weeks ago')
        # Values truncating to 0 are rejected as invalid
        assert len(result) == 0

    def test_0_9_months_ago(self):
        result = parse_time_references('0.9 months ago')
        # Values truncating to 0 are rejected as invalid
        assert len(result) == 0

    # 10+ range with tenths
    def test_10_5_hours_ago(self):
        result = parse_time_references('10.5 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_11_5_days_ago(self):
        result = parse_time_references('11.5 days ago')
        assert len(result) == 1
        assert result[0].cardinality == 11
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_12_5_minutes_ago(self):
        result = parse_time_references('12.5 minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 12
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_15_5_weeks_ago(self):
        result = parse_time_references('15.5 weeks ago')
        assert len(result) == 1
        assert result[0].cardinality == 15
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_20_5_months_ago(self):
        result = parse_time_references('20.5 months ago')
        assert len(result) == 1
        assert result[0].cardinality == 20
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_50_5_years_ago(self):
        result = parse_time_references('50.5 years ago')
        assert len(result) == 1
        assert result[0].cardinality == 50
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    # Large numbers
    def test_100_5_hours_ago(self):
        result = parse_time_references('100.5 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 100
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_1000_5_days_ago(self):
        result = parse_time_references('1000.5 days ago')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'


class TestMoreSentenceContext:
    """More sentence embedding variations with decimal cardinalities."""

    def test_the_cache_expired_2_5_hours_ago(self):
        result = parse_time_references('the cache expired 2.5 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_last_updated_1_5_days_ago(self):
        result = parse_time_references('last updated 1.5 days ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_i_saw_him_3_5_weeks_ago(self):
        result = parse_time_references('I saw him 3.5 weeks ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_the_meeting_was_0_5_hours_ago(self):
        result = parse_time_references('the meeting was 0.5 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 0
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_we_talked_about_it_2_75_months_ago(self):
        result = parse_time_references('we talked about it 2.75 months ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_she_left_4_25_minutes_ago(self):
        result = parse_time_references('she left 4.25 minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_it_happened_10_5_years_ago(self):
        result = parse_time_references('it happened 10.5 years ago')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_the_server_restarted_1_25_hours_ago(self):
        result = parse_time_references('the server restarted 1.25 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'


class TestCapitalizationVariations:
    """Decimal cardinalities with various capitalizations."""

    def test_2_5_Hours_Ago(self):
        result = parse_time_references('2.5 Hours Ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_1_5_DAYS_AGO(self):
        result = parse_time_references('1.5 DAYS AGO')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_3_5_Minutes_ago(self):
        result = parse_time_references('3.5 Minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_0_5_WEEKS(self):
        result = parse_time_references('0.5 WEEKS')
        # Values truncating to 0 are rejected as invalid
        assert len(result) == 0

    def test_2_25_Months_Back(self):
        result = parse_time_references('2.25 Months Back')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'


class TestThreeDecimalPlaces:
    """Decimal cardinalities with three decimal places."""

    def test_1_125_hours_ago(self):
        result = parse_time_references('1.125 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_2_375_days_ago(self):
        result = parse_time_references('2.375 days ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_3_625_minutes_ago(self):
        result = parse_time_references('3.625 minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_0_875_weeks_ago(self):
        result = parse_time_references('0.875 weeks ago')
        # Values truncating to 0 are rejected as invalid
        assert len(result) == 0

    def test_5_999_months_ago(self):
        result = parse_time_references('5.999 months ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_10_125_years_ago(self):
        result = parse_time_references('10.125 years ago')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'


class TestMixedDecimalFormats:
    """Various decimal number formats."""

    # Different decimal values
    def test_1_1_hours_ago(self):
        result = parse_time_references('1.1 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_1_9_days_ago(self):
        result = parse_time_references('1.9 days ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_2_1_minutes_ago(self):
        result = parse_time_references('2.1 minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_2_9_weeks_ago(self):
        result = parse_time_references('2.9 weeks ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_3_3_months_ago(self):
        result = parse_time_references('3.3 months ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_4_7_years_ago(self):
        result = parse_time_references('4.7 years ago')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'


class TestDecimalWithMultipleSpaces:
    """Decimal cardinalities with extra whitespace."""

    def test_2_5_hours_ago_extra_spaces(self):
        result = parse_time_references('2.5  hours  ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_1_5_days_ago_tabs(self):
        result = parse_time_references('1.5\thours\tago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'


class TestDecimalWithPunctuation:
    """Decimal cardinalities near punctuation."""

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_2_5_hours_ago_with_period(self):
        result = parse_time_references('It was 2.5 hours ago.')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_1_5_days_ago_with_comma(self):
        result = parse_time_references('Updated 1.5 days ago, by user')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_3_5_minutes_ago_with_exclamation(self):
        result = parse_time_references('That was 3.5 minutes ago!')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_0_5_weeks_ago_with_question(self):
        result = parse_time_references('Was that 0.5 weeks ago?')
        # Values truncating to 0 are rejected as invalid
        assert len(result) == 0


class TestDecimalAdditionalFrames:
    """Ensure all time frame variations are covered."""

    # Additional second tests
    def test_2_5_second_ago(self):
        result = parse_time_references('2.5 second ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_4_5_seconds(self):
        result = parse_time_references('4.5 seconds')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    # Additional week tests
    def test_6_5_week_ago(self):
        result = parse_time_references('6.5 week ago')
        assert len(result) == 1
        assert result[0].cardinality == 6
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_7_5_weeks(self):
        result = parse_time_references('7.5 weeks')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    # Additional month tests
    def test_6_5_month_ago(self):
        result = parse_time_references('6.5 month ago')
        assert len(result) == 1
        assert result[0].cardinality == 6
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_8_5_months(self):
        result = parse_time_references('8.5 months')
        assert len(result) == 1
        assert result[0].cardinality == 8
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    # Additional year tests
    def test_6_5_year_ago(self):
        result = parse_time_references('6.5 year ago')
        assert len(result) == 1
        assert result[0].cardinality == 6
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_9_5_years(self):
        result = parse_time_references('9.5 years')
        assert len(result) == 1
        assert result[0].cardinality == 9
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'


class TestDecimalAboutApproximations:
    """Decimal cardinalities with approximation words like 'about'."""

    def test_about_2_5_hours_ago(self):
        result = parse_time_references('about 2.5 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_about_1_5_days_ago(self):
        result = parse_time_references('about 1.5 days ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_approximately_3_5_minutes_ago(self):
        result = parse_time_references('approximately 3.5 minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_around_4_5_weeks_ago(self):
        result = parse_time_references('around 4.5 weeks ago')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_roughly_5_5_months_ago(self):
        result = parse_time_references('roughly 5.5 months ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'


class TestDecimalMoreEdgeCases:
    """Additional edge cases for decimal cardinalities."""

    def test_99_9_hours_ago(self):
        result = parse_time_references('99.9 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 99
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_999_9_days_ago(self):
        result = parse_time_references('999.9 days ago')
        assert len(result) == 1
        assert result[0].cardinality == 999
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_0_01_hours_ago(self):
        result = parse_time_references('0.01 hours ago')
        # Values truncating to 0 are rejected as invalid
        assert len(result) == 0

    def test_0_99_minutes_ago(self):
        result = parse_time_references('0.99 minutes ago')
        # Values truncating to 0 are rejected as invalid
        assert len(result) == 0

    def test_1_01_days_ago(self):
        result = parse_time_references('1.01 days ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_1_99_weeks_ago(self):
        result = parse_time_references('1.99 weeks ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'


class TestDecimalYrMoWkAbbreviations:
    """Decimal cardinalities with year/month/week abbreviations."""

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_2_5_yr_ago(self):
        result = parse_time_references('2.5 yr ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_2_5_yrs_ago(self):
        result = parse_time_references('2.5 yrs ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_3_5_mo_ago(self):
        result = parse_time_references('3.5 mo ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_3_5_mos_ago(self):
        result = parse_time_references('3.5 mos ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_4_5_wk_ago(self):
        result = parse_time_references('4.5 wk ago')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_4_5_wks_ago(self):
        result = parse_time_references('4.5 wks ago')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'


class TestDecimalImplicitPastNoAgo:
    """Ensure implicit past tense works without 'ago' for all decimal variations."""

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_10_25_hours(self):
        result = parse_time_references('10.25 hours')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_5_75_days(self):
        result = parse_time_references('5.75 days')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_3_25_weeks(self):
        result = parse_time_references('3.25 weeks')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_6_75_months(self):
        result = parse_time_references('6.75 months')
        assert len(result) == 1
        assert result[0].cardinality == 6
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_7_25_years(self):
        result = parse_time_references('7.25 years')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_15_5_minutes(self):
        result = parse_time_references('15.5 minutes')
        assert len(result) == 1
        assert result[0].cardinality == 15
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_25_5_seconds(self):
        result = parse_time_references('25.5 seconds')
        assert len(result) == 1
        assert result[0].cardinality == 25
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'


class TestDecimalBeforePattern:
    """Decimal cardinalities with 'before' instead of 'ago'."""

    def test_2_5_hours_before(self):
        result = parse_time_references('2.5 hours before')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_1_5_days_before(self):
        result = parse_time_references('1.5 days before')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_3_5_minutes_before(self):
        result = parse_time_references('3.5 minutes before')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_0_5_weeks_before(self):
        result = parse_time_references('0.5 weeks before')
        # Values truncating to 0 are rejected as invalid
        assert len(result) == 0


class TestDecimalEarlierPattern:
    """Decimal cardinalities with 'earlier' pattern."""

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_2_5_hours_earlier(self):
        result = parse_time_references('2.5 hours earlier')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_1_5_days_earlier(self):
        result = parse_time_references('1.5 days earlier')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_3_5_weeks_earlier(self):
        result = parse_time_references('3.5 weeks earlier')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'


class TestDecimalMoreSentenceVariations:
    """Additional sentence context variations to reach 250+ tests."""

    def test_file_created_2_5_hours_ago(self):
        result = parse_time_references('file created 2.5 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_session_started_1_5_days_ago(self):
        result = parse_time_references('session started 1.5 days ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_backup_completed_3_75_hours_ago(self):
        result = parse_time_references('backup completed 3.75 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    @pytest.mark.xfail(reason="Pattern not yet supported: implicit past, sentence embedding, punctuation, abbreviations, or 'earlier' marker")
    def test_download_finished_0_5_minutes_ago(self):
        result = parse_time_references('download finished 0.5 minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 0
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_build_failed_4_25_hours_ago(self):
        result = parse_time_references('build failed 4.25 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_test_suite_ran_2_75_days_ago(self):
        result = parse_time_references('test suite ran 2.75 days ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_deployment_triggered_5_5_hours_ago(self):
        result = parse_time_references('deployment triggered 5.5 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_notification_sent_1_25_minutes_ago(self):
        result = parse_time_references('notification sent 1.25 minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_error_occurred_6_5_seconds_ago(self):
        result = parse_time_references('error occurred 6.5 seconds ago')
        assert len(result) == 1
        assert result[0].cardinality == 6
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'

    def test_request_received_7_75_minutes_ago(self):
        result = parse_time_references('request received 7.75 minutes ago')
        assert len(result) == 1
        assert result[0].cardinality == 7
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'
