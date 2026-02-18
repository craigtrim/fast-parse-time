#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for named day references like yesterday, tomorrow, today."""

import pytest
from fast_parse_time import parse_time_references

class TestTomorrowPositionVariations:
    """Tests for 'tomorrow' at different positions and combinations."""

    def test_tomorrow_at_start_of_sentence(self):
        """'tomorrow' at the start of a sentence should be extracted."""
        result = parse_time_references('tomorrow we deploy the fix')
        assert len(result) == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'future'

    def test_tomorrow_morning_frame_and_tense(self):
        """'tomorrow morning' should still return frame=day and tense=future."""
        result = parse_time_references('the call is tomorrow morning')
        assert len(result) >= 1
        tomorrow_refs = [r for r in result if r.frame == 'day' and r.tense == 'future']
        assert len(tomorrow_refs) >= 1

    def test_tomorrow_at_end_of_sentence(self):
        """'tomorrow' at the end of a sentence should be extracted."""
        result = parse_time_references('can we reschedule for tomorrow')
        assert len(result) == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'future'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
