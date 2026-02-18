#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for indefinite articles (a/an) as cardinality."""

import pytest
from fast_parse_time import parse_time_references

class TestMoreSentenceContextVariations:
    """Additional sentence context variations for indefinite article patterns."""

    def test_a_month_ago_in_sentence(self):
        """'a month ago' in a sentence should be extracted."""
        result = parse_time_references('the contract was signed a month ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_a_year_ago_in_sentence(self):
        """'a year ago' in a sentence should be extracted."""
        result = parse_time_references('the product launched a year ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_an_hour_from_now_in_sentence(self):
        """'an hour from now' in a sentence should be extracted."""
        result = parse_time_references('the build will finish an hour from now')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'future'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
