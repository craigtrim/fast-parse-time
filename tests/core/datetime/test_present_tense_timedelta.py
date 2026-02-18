#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for RelativeTime dataclass methods."""

import pytest
from datetime import datetime, timedelta
from fast_parse_time import RelativeTime

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
