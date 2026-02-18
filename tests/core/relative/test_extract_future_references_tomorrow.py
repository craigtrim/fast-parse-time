#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for extract_future_references function."""

import pytest
from fast_parse_time import extract_future_references, RelativeTime

class TestTomorrow:
    """Tests for 'tomorrow' as a future reference."""

    def test_tomorrow(self):
        """'tomorrow' should be returned as a future reference."""
        result = extract_future_references('tomorrow')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'future'

    def test_tomorrow_in_sentence(self):
        """'tomorrow' in a sentence should be extracted."""
        result = extract_future_references("let's meet tomorrow")
        assert len(result) == 1
        assert result[0].tense == 'future'
