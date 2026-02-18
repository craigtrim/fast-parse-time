#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for written month name formats in explicit dates."""

import pytest
from fast_parse_time import extract_explicit_dates

class TestSentenceContext:
    """Tests for written dates within sentences."""

    def test_date_in_sentence(self):
        """Date in a sentence should be extracted."""
        result = extract_explicit_dates('The meeting is on March 15, 2024')
        assert len(result) == 1

    def test_date_at_end(self):
        """Date at end of sentence should be extracted."""
        result = extract_explicit_dates('Event scheduled for December 25, 2024')
        assert len(result) == 1
