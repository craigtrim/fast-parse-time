#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for extract_future_references function."""

import pytest
from fast_parse_time import extract_future_references, RelativeTime

class TestReturnType:
    """Tests for correct return types."""

    def test_returns_list(self):
        """Function should always return a list."""
        result = extract_future_references('next week')
        assert isinstance(result, list)

    def test_returns_relative_time_objects(self):
        """Items in list should be RelativeTime instances."""
        result = extract_future_references('next week')
        assert len(result) == 1
        assert isinstance(result[0], RelativeTime)

    def test_empty_on_no_temporal(self):
        """Text with no temporal info should return empty list."""
        result = extract_future_references('Hello world')
        assert result == []

    def test_empty_on_empty_string(self):
        """Empty string should return empty list."""
        result = extract_future_references('')
        assert result == []
