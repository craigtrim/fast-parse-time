#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for RelativeTime dataclass methods."""

import pytest
from datetime import datetime, timedelta
from fast_parse_time import RelativeTime

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
