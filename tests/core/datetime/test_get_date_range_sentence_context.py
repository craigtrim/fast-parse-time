#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for get_date_range function."""

import pytest
from datetime import datetime
from fast_parse_time import get_date_range

class TestGetDateRangeSentenceContext:
    """Tests for get_date_range within sentence context."""

    def test_in_sentence_with_from_to(self):
        """'from X to Y' pattern in a sentence should work."""
        result = get_date_range('show me activity from 30 days ago to 7 days ago')
        assert result is not None
        start, end = result
        assert start < end

    def test_earlier_reference_is_start(self):
        """The earlier date should always be the start of the range."""
        result = get_date_range('show me activity from 30 days ago to 7 days ago')
        assert result is not None
        start, end = result
        now = datetime.now()
        # Start should be approximately 30 days before now
        # End should be approximately 7 days before now
        assert start < end
        assert start < now
        assert end < now
