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


class TestDecadeFromNow:
    """N decades from now -> future, year, N*10"""

    def test_1_decade_from_now(self):
        result = parse_time_references('1 decade from now')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'year'
        assert result[0].tense == 'future'

    def test_2_decades_from_now(self):
        result = parse_time_references('2 decades from now')
        assert len(result) == 1
        assert result[0].cardinality == 20
        assert result[0].frame == 'year'
        assert result[0].tense == 'future'

    def test_3_decades_from_now(self):
        result = parse_time_references('3 decades from now')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'year'
        assert result[0].tense == 'future'

    def test_4_decades_from_now(self):
        result = parse_time_references('4 decades from now')
        assert len(result) == 1
        assert result[0].cardinality == 40
        assert result[0].frame == 'year'
        assert result[0].tense == 'future'

    def test_5_decades_from_now(self):
        result = parse_time_references('5 decades from now')
        assert len(result) == 1
        assert result[0].cardinality == 50
        assert result[0].frame == 'year'
        assert result[0].tense == 'future'

    def test_6_decades_from_now(self):
        result = parse_time_references('6 decades from now')
        assert len(result) == 1
        assert result[0].cardinality == 60
        assert result[0].frame == 'year'
        assert result[0].tense == 'future'

    def test_7_decades_from_now(self):
        result = parse_time_references('7 decades from now')
        assert len(result) == 1
        assert result[0].cardinality == 70
        assert result[0].frame == 'year'
        assert result[0].tense == 'future'

    def test_8_decades_from_now(self):
        result = parse_time_references('8 decades from now')
        assert len(result) == 1
        assert result[0].cardinality == 80
        assert result[0].frame == 'year'
        assert result[0].tense == 'future'

    def test_9_decades_from_now(self):
        result = parse_time_references('9 decades from now')
        assert len(result) == 1
        assert result[0].cardinality == 90
        assert result[0].frame == 'year'
        assert result[0].tense == 'future'

    def test_10_decades_from_now(self):
        result = parse_time_references('10 decades from now')
        assert len(result) == 1
        assert result[0].cardinality == 100
        assert result[0].frame == 'year'
        assert result[0].tense == 'future'
