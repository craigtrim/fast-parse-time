#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for 'last X' and 'past X' without explicit cardinality."""

import pytest
from fast_parse_time import parse_time_references

class TestMoreCapitalizationVariants:
    """Additional capitalization variant tests."""

    def test_last_year_uppercase(self):
        """'LAST YEAR' should work (case-insensitive)."""
        result = parse_time_references('LAST YEAR')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_last_day_mixed_case(self):
        """'Last Day' should work (case-insensitive)."""
        result = parse_time_references('Last Day')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_past_year_title_case(self):
        """'Past Year' should work (case-insensitive)."""
        result = parse_time_references('Past Year')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
