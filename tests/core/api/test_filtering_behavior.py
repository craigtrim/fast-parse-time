#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for extract_future_references function."""

import pytest
from fast_parse_time import extract_future_references, RelativeTime

class TestFilteringBehavior:
    """Tests that only future references are returned (past excluded)."""

    def test_excludes_past_references(self):
        """Past references should not appear in future results."""
        result = extract_future_references('5 days ago')
        assert result == []

    def test_excludes_yesterday(self):
        """'yesterday' (past) should be excluded."""
        result = extract_future_references('yesterday')
        assert result == []

    def test_mixed_only_returns_future(self):
        """Mixed past/future text should only return future references."""
        result = extract_future_references('show data from last week and next week')
        assert len(result) == 1
        assert result[0].tense == 'future'
        assert result[0].frame == 'week'
