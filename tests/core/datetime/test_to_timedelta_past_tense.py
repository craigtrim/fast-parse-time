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
