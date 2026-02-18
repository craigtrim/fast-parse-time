#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for informal time expressions."""

import pytest
from fast_parse_time import parse_time_references

class TestCapitalizationVariations:
    """Tests for capitalization variations."""

    def test_half_an_hour_uppercase(self):
        """'HALF AN HOUR AGO' should work (case-insensitive)."""
        result = parse_time_references('HALF AN HOUR AGO')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_several_weeks_mixed_case(self):
        """'Several Weeks Ago' should work (case-insensitive)."""
        result = parse_time_references('Several Weeks Ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'
