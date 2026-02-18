#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for informal time expressions."""

import pytest
from fast_parse_time import parse_time_references

class TestHalfAYear:
    """Tests for 'half a year ago' pattern."""

    def test_half_a_year_ago(self):
        """'half a year ago' - documents current behavior (resolves as 1 year past)."""
        # NOTE: 'half a year' is currently interpreted as 1 year (not 6 months)
        # because 'a year' is matched as a unit and 'half' modifies the cardinality
        # to a non-standard value that is rounded to 1.
        result = parse_time_references('half a year ago')
        assert len(result) == 1
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'
