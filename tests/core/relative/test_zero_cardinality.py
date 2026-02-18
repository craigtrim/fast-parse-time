#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for RelativeTime dataclass methods."""

import pytest
from datetime import datetime, timedelta
from fast_parse_time import RelativeTime

class TestZeroCardinality:
    """Tests for zero cardinality behavior."""

    def test_zero_cardinality_present(self):
        """Cardinality of 0 with present tense should produce zero timedelta."""
        rt = RelativeTime(cardinality=0, frame='day', tense='present')
        delta = rt.to_timedelta()
        assert delta.total_seconds() == 0
