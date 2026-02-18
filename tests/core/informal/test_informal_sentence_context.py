#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for informal time expressions."""

import pytest
from fast_parse_time import parse_time_references

class TestInformalSentenceContext:
    """Tests for informal expressions within sentence context."""

    def test_few_hours_in_sentence(self):
        """'a few hours ago' within a sentence should be extracted."""
        result = parse_time_references('the outage started a few hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_couple_of_days_in_sentence(self):
        """'couple of days ago' within a sentence should be extracted."""
        result = parse_time_references('we updated that a couple of days ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_several_hours_in_sentence(self):
        """'several hours ago' within a sentence should be extracted."""
        result = parse_time_references('the backup completed several hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
