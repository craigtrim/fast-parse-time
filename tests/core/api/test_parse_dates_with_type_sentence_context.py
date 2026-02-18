#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for parse_dates_with_type function."""

import pytest
from fast_parse_time import parse_dates_with_type

class TestSentenceContext:
    """Tests for parse_dates_with_type within sentence context."""

    def test_filter_in_sentence(self):
        """Filter should work on dates embedded in sentences."""
        result = parse_dates_with_type(
            'The meeting is scheduled for 04/08/2024 and followed up on 3/24',
            'FULL_EXPLICIT_DATE'
        )
        assert len(result) == 1
        assert '04/08/2024' in result
