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


class TestDecadeLastN:
    """last N decades -> past, year, N*10"""

    def test_last_2_decades(self):
        result = parse_time_references('last 2 decades')
        assert len(result) == 1
        assert result[0].cardinality == 20
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_last_3_decades(self):
        result = parse_time_references('last 3 decades')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_last_4_decades(self):
        result = parse_time_references('last 4 decades')
        assert len(result) == 1
        assert result[0].cardinality == 40
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_last_5_decades(self):
        result = parse_time_references('last 5 decades')
        assert len(result) == 1
        assert result[0].cardinality == 50
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_last_10_decades(self):
        result = parse_time_references('last 10 decades')
        assert len(result) == 1
        assert result[0].cardinality == 100
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'
