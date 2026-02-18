#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for informal time expressions."""

import pytest
from fast_parse_time import parse_time_references

class TestCoupleAdditionalFrames:
    """Tests for 'couple of X ago' with additional frames."""

    def test_couple_of_days_ago(self):
        """'couple of days ago' should resolve to 2 days."""
        result = parse_time_references('couple of days ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_couple_of_months_ago(self):
        """'couple of months ago' should resolve to 2 months."""
        result = parse_time_references('couple of months ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'
