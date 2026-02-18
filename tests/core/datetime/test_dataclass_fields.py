#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for RelativeTime dataclass methods."""

import pytest
from datetime import datetime, timedelta
from fast_parse_time import RelativeTime

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
