#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for 'last X' and 'past X' without explicit cardinality."""

import pytest
from fast_parse_time import parse_time_references

class TestLastHourMinuteSecond:
    """Tests for 'last hour', 'last minute', 'last second' patterns."""

    def test_last_hour(self):
        """'last hour' should imply cardinality of 1 and frame of hour."""
        result = parse_time_references('last hour')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_last_minute(self):
        """'last minute' should imply cardinality of 1 and frame of minute."""
        result = parse_time_references('last minute')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_last_second(self):
        """'last second' should imply cardinality of 1 and frame of second."""
        result = parse_time_references('last second')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'
