#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for informal time expressions."""

import pytest
from fast_parse_time import parse_time_references

class TestHalfAnHour:
    """Tests for 'half an hour' patterns."""

    def test_half_an_hour_ago(self):
        """'half an hour ago' should resolve to 30 minutes."""
        result = parse_time_references('half an hour ago')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_half_an_hour_from_now(self):
        """'half an hour from now' should resolve to 30 minutes."""
        result = parse_time_references('half an hour from now')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'minute'
        assert result[0].tense == 'future'

    def test_half_a_day_ago(self):
        """'half a day ago' should resolve to 12 hours."""
        result = parse_time_references('half a day ago')
        assert len(result) == 1
        assert result[0].cardinality == 12
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'
