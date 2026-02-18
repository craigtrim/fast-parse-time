#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for informal time expressions."""

import pytest
from fast_parse_time import parse_time_references

class TestSeveralWithHourFrame:
    """Tests for 'several hours ago' pattern."""

    def test_several_hours_ago(self):
        """'several hours ago' should resolve to 3 hours."""
        result = parse_time_references('several hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'
