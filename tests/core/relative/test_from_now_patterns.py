#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for extract_future_references function."""

import pytest
from fast_parse_time import extract_future_references, RelativeTime

class TestFromNowPatterns:
    """Tests for 'X from now' patterns."""

    def test_half_an_hour_from_now(self):
        """'half an hour from now' should resolve to 30 minutes in the future."""
        result = extract_future_references('half an hour from now')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'minute'
        assert result[0].tense == 'future'
