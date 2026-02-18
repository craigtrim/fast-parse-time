#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for RelativeTime dataclass methods."""

import pytest
from datetime import datetime, timedelta
from fast_parse_time import RelativeTime


class TestToTimedeltaPastTense:
    """Tests for to_timedelta() with past tense (negative offsets)."""

    def test_past_days(self):
        """5 days past should be timedelta of -5 days."""
        rt = RelativeTime(cardinality=5, frame='day', tense='past')
        delta = rt.to_timedelta()
        assert delta == timedelta(days=-5)

    def test_past_weeks(self):
        """2 weeks past should be timedelta of -14 days."""
        rt = RelativeTime(cardinality=2, frame='week', tense='past')
        delta = rt.to_timedelta()
        assert delta == timedelta(days=-14)

    def test_past_months(self):
        """3 months past should be timedelta of -90 days (30 days/month avg)."""
        rt = RelativeTime(cardinality=3, frame='month', tense='past')
        delta = rt.to_timedelta()
        assert delta == timedelta(days=-90)

    def test_past_years(self):
        """1 year past should be timedelta of -365 days."""
        rt = RelativeTime(cardinality=1, frame='year', tense='past')
        delta = rt.to_timedelta()
        assert delta == timedelta(days=-365)

    def test_past_hours(self):
        """1 hour past should be timedelta of -1 hour."""
        rt = RelativeTime(cardinality=1, frame='hour', tense='past')
        delta = rt.to_timedelta()
        assert delta == timedelta(hours=-1)

    def test_past_minutes(self):
        """30 minutes past should be timedelta of -30 minutes."""
        rt = RelativeTime(cardinality=30, frame='minute', tense='past')
        delta = rt.to_timedelta()
        assert delta == timedelta(minutes=-30)

    def test_past_seconds(self):
        """10 seconds past should be timedelta of -10 seconds."""
        rt = RelativeTime(cardinality=10, frame='second', tense='past')
        delta = rt.to_timedelta()
        assert delta == timedelta(seconds=-10)


class TestToTimedeltaFutureTense:
    """Tests for to_timedelta() with future tense (positive offsets)."""

    def test_future_days(self):
        """3 days future should be timedelta of +3 days."""
        rt = RelativeTime(cardinality=3, frame='day', tense='future')
        delta = rt.to_timedelta()
        assert delta == timedelta(days=3)

    def test_future_weeks(self):
        """1 week future should be timedelta of +7 days."""
        rt = RelativeTime(cardinality=1, frame='week', tense='future')
        delta = rt.to_timedelta()
        assert delta == timedelta(days=7)

    def test_future_months(self):
        """2 months future should be timedelta of +60 days."""
        rt = RelativeTime(cardinality=2, frame='month', tense='future')
        delta = rt.to_timedelta()
        assert delta == timedelta(days=60)

    def test_future_years(self):
        """1 year future should be timedelta of +365 days."""
        rt = RelativeTime(cardinality=1, frame='year', tense='future')
        delta = rt.to_timedelta()
        assert delta == timedelta(days=365)

    def test_future_hours(self):
        """2 hours future should be timedelta of +2 hours."""
        rt = RelativeTime(cardinality=2, frame='hour', tense='future')
        delta = rt.to_timedelta()
        assert delta == timedelta(hours=2)

    def test_future_minutes(self):
        """30 minutes future should be timedelta of +30 minutes."""
        rt = RelativeTime(cardinality=30, frame='minute', tense='future')
        delta = rt.to_timedelta()
        assert delta == timedelta(minutes=30)

    def test_future_seconds(self):
        """45 seconds future should be timedelta of +45 seconds."""
        rt = RelativeTime(cardinality=45, frame='second', tense='future')
        delta = rt.to_timedelta()
        assert delta == timedelta(seconds=45)


class TestToTimedeltaReturnType:
    """Tests for to_timedelta() return type."""

    def test_returns_timedelta(self):
        """to_timedelta() should return a timedelta object."""
        rt = RelativeTime(cardinality=5, frame='day', tense='past')
        assert isinstance(rt.to_timedelta(), timedelta)

    def test_returns_negative_for_past(self):
        """to_timedelta() for past tense should return negative timedelta."""
        rt = RelativeTime(cardinality=5, frame='day', tense='past')
        delta = rt.to_timedelta()
        assert delta.total_seconds() < 0

    def test_returns_positive_for_future(self):
        """to_timedelta() for future tense should return positive timedelta."""
        rt = RelativeTime(cardinality=5, frame='day', tense='future')
        delta = rt.to_timedelta()
        assert delta.total_seconds() > 0


class TestToDatetimeWithReference:
    """Tests for to_datetime() with a custom reference datetime."""

    def test_past_is_before_reference(self):
        """Past tense datetime should be before the reference."""
        ref = datetime(2025, 6, 15, 12, 0, 0)
        rt = RelativeTime(cardinality=5, frame='day', tense='past')
        result = rt.to_datetime(reference=ref)
        assert result < ref

    def test_future_is_after_reference(self):
        """Future tense datetime should be after the reference."""
        ref = datetime(2025, 6, 15, 12, 0, 0)
        rt = RelativeTime(cardinality=5, frame='day', tense='future')
        result = rt.to_datetime(reference=ref)
        assert result > ref

    def test_exact_past_calculation(self):
        """5 days past from a known reference should give exact result."""
        ref = datetime(2025, 6, 20, 0, 0, 0)
        rt = RelativeTime(cardinality=5, frame='day', tense='past')
        result = rt.to_datetime(reference=ref)
        assert result == datetime(2025, 6, 15, 0, 0, 0)

    def test_exact_future_calculation(self):
        """3 days future from a known reference should give exact result."""
        ref = datetime(2025, 6, 15, 0, 0, 0)
        rt = RelativeTime(cardinality=3, frame='day', tense='future')
        result = rt.to_datetime(reference=ref)
        assert result == datetime(2025, 6, 18, 0, 0, 0)

    def test_exact_week_calculation(self):
        """1 week past from a known reference should be 7 days earlier."""
        ref = datetime(2025, 6, 22, 0, 0, 0)
        rt = RelativeTime(cardinality=1, frame='week', tense='past')
        result = rt.to_datetime(reference=ref)
        assert result == datetime(2025, 6, 15, 0, 0, 0)

    def test_exact_hour_calculation(self):
        """2 hours past from a known reference should give exact result."""
        ref = datetime(2025, 6, 15, 10, 0, 0)
        rt = RelativeTime(cardinality=2, frame='hour', tense='past')
        result = rt.to_datetime(reference=ref)
        assert result == datetime(2025, 6, 15, 8, 0, 0)


class TestToDatetimeWithoutReference:
    """Tests for to_datetime() without a reference (uses current time)."""

    def test_returns_datetime(self):
        """to_datetime() should return a datetime object."""
        rt = RelativeTime(cardinality=5, frame='day', tense='past')
        result = rt.to_datetime()
        assert isinstance(result, datetime)

    def test_past_is_before_now(self):
        """Past tense without reference should be before current time."""
        rt = RelativeTime(cardinality=5, frame='day', tense='past')
        result = rt.to_datetime()
        assert result < datetime.now()

    def test_future_is_after_now(self):
        """Future tense without reference should be after current time."""
        rt = RelativeTime(cardinality=5, frame='day', tense='future')
        result = rt.to_datetime()
        assert result > datetime.now()


class TestDataclassFields:
    """Tests for RelativeTime dataclass field access."""

    def test_cardinality_field(self):
        """Cardinality field should be accessible and correct."""
        rt = RelativeTime(cardinality=7, frame='day', tense='past')
        assert rt.cardinality == 7

    def test_frame_field(self):
        """Frame field should be accessible and correct."""
        rt = RelativeTime(cardinality=7, frame='week', tense='future')
        assert rt.frame == 'week'

    def test_tense_field(self):
        """Tense field should be accessible and correct."""
        rt = RelativeTime(cardinality=7, frame='day', tense='past')
        assert rt.tense == 'past'


class TestPresentTenseTimedelta:
    """Tests for to_timedelta() with present tense (zero offset)."""

    def test_present_tense_returns_zero_timedelta(self):
        """Present tense should return a zero timedelta."""
        rt = RelativeTime(cardinality=0, frame='day', tense='present')
        delta = rt.to_timedelta()
        assert delta == timedelta(0)

    def test_present_tense_total_seconds_is_zero(self):
        """Present tense timedelta total_seconds should be 0."""
        rt = RelativeTime(cardinality=0, frame='day', tense='present')
        delta = rt.to_timedelta()
        assert delta.total_seconds() == 0


class TestZeroCardinality:
    """Tests for zero cardinality behavior."""

    def test_zero_cardinality_present(self):
        """Cardinality of 0 with present tense should produce zero timedelta."""
        rt = RelativeTime(cardinality=0, frame='day', tense='present')
        delta = rt.to_timedelta()
        assert delta.total_seconds() == 0


class TestExactCalculationsAdditional:
    """Additional exact calculation tests for various frames."""

    def test_exact_month_calculation(self):
        """3 months past from a known reference should be 90 days earlier."""
        ref = datetime(2025, 9, 1, 0, 0, 0)
        rt = RelativeTime(cardinality=3, frame='month', tense='past')
        result = rt.to_datetime(reference=ref)
        assert result == datetime(2025, 6, 3, 0, 0, 0)

    def test_exact_year_calculation(self):
        """1 year past from a known reference should be 365 days earlier."""
        ref = datetime(2025, 6, 15, 0, 0, 0)
        rt = RelativeTime(cardinality=1, frame='year', tense='past')
        result = rt.to_datetime(reference=ref)
        assert result == datetime(2024, 6, 15, 0, 0, 0)

    def test_exact_minute_calculation(self):
        """30 minutes past from a known reference should give exact result."""
        ref = datetime(2025, 6, 15, 10, 30, 0)
        rt = RelativeTime(cardinality=30, frame='minute', tense='past')
        result = rt.to_datetime(reference=ref)
        assert result == datetime(2025, 6, 15, 10, 0, 0)


class TestTotalSecondsForFrames:
    """Tests for total_seconds() values across different frames."""

    def test_total_seconds_for_1_day_past(self):
        """1 day past should be -86400 total seconds."""
        rt = RelativeTime(cardinality=1, frame='day', tense='past')
        delta = rt.to_timedelta()
        assert delta.total_seconds() == -86400

    def test_total_seconds_for_1_hour_past(self):
        """1 hour past should be -3600 total seconds."""
        rt = RelativeTime(cardinality=1, frame='hour', tense='past')
        delta = rt.to_timedelta()
        assert delta.total_seconds() == -3600

    def test_total_seconds_for_1_minute_past(self):
        """1 minute past should be -60 total seconds."""
        rt = RelativeTime(cardinality=1, frame='minute', tense='past')
        delta = rt.to_timedelta()
        assert delta.total_seconds() == -60

    def test_total_seconds_for_1_second_past(self):
        """1 second past should be -1 total seconds."""
        rt = RelativeTime(cardinality=1, frame='second', tense='past')
        delta = rt.to_timedelta()
        assert delta.total_seconds() == -1

    def test_total_seconds_for_1_week_future(self):
        """1 week future should be +604800 total seconds."""
        rt = RelativeTime(cardinality=1, frame='week', tense='future')
        delta = rt.to_timedelta()
        assert delta.total_seconds() == 604800


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
