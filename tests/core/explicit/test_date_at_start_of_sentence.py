#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for written month name formats in explicit dates."""

import pytest
from fast_parse_time import extract_explicit_dates

class TestDateAtStartOfSentence:
    """Tests for dates appearing at the very start of a sentence."""

    def test_date_at_start(self):
        """Date at the start of a sentence should be extracted."""
        result = extract_explicit_dates('March 15, 2024 is the deadline')
        assert len(result) == 1

    def test_abbreviated_month_at_start(self):
        """Abbreviated month at the start of a sentence should be extracted."""
        result = extract_explicit_dates('Apr 10, 2024 kicks off the project')
        assert len(result) == 1
