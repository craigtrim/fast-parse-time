# -*- coding: utf-8 -*-
"""
Test decade as a time unit.

Related GitHub Issue:
    #19 - Gap: decade as a time unit not recognized
    https://github.com/craigtrim/fast-parse-time/issues/19

Decade normalizes to years with a multiplier of 10:
    1 decade  = 10 years
    2 decades = 20 years
    3 decades = 30 years
    N decades = N * 10 years

Frame is always 'year'. Cardinality is N * 10.
"""

from fast_parse_time import parse_time_references, has_temporal_info


class TestDecadeNextN:
    """next N decades -> future, year, N*10"""

    def test_next_2_decades(self):
        result = parse_time_references('next 2 decades')
        assert len(result) == 1
        assert result[0].cardinality == 20
        assert result[0].frame == 'year'
        assert result[0].tense == 'future'

    def test_next_3_decades(self):
        result = parse_time_references('next 3 decades')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'year'
        assert result[0].tense == 'future'

    def test_next_4_decades(self):
        result = parse_time_references('next 4 decades')
        assert len(result) == 1
        assert result[0].cardinality == 40
        assert result[0].frame == 'year'
        assert result[0].tense == 'future'

    def test_next_5_decades(self):
        result = parse_time_references('next 5 decades')
        assert len(result) == 1
        assert result[0].cardinality == 50
        assert result[0].frame == 'year'
        assert result[0].tense == 'future'

    def test_next_10_decades(self):
        result = parse_time_references('next 10 decades')
        assert len(result) == 1
        assert result[0].cardinality == 100
        assert result[0].frame == 'year'
        assert result[0].tense == 'future'
