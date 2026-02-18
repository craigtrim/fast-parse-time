#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for RelativeTime dataclass methods."""

import pytest
from datetime import datetime, timedelta
from fast_parse_time import RelativeTime

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
