#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for RelativeTime dataclass methods."""

import pytest
from datetime import datetime, timedelta
from fast_parse_time import RelativeTime

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
