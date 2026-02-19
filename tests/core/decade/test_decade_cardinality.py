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


class TestDecadeCardinality:
    """Verify N*10 cardinality mapping is accurate"""

    def test_cardinality_1_decade(self):
        result = parse_time_references('1 decade ago')
        assert result[0].cardinality == 10

    def test_cardinality_2_decades(self):
        result = parse_time_references('2 decades ago')
        assert result[0].cardinality == 20

    def test_cardinality_3_decades(self):
        result = parse_time_references('3 decades ago')
        assert result[0].cardinality == 30

    def test_cardinality_4_decades(self):
        result = parse_time_references('4 decades ago')
        assert result[0].cardinality == 40

    def test_cardinality_5_decades(self):
        result = parse_time_references('5 decades ago')
        assert result[0].cardinality == 50

    def test_cardinality_6_decades(self):
        result = parse_time_references('6 decades ago')
        assert result[0].cardinality == 60

    def test_cardinality_7_decades(self):
        result = parse_time_references('7 decades ago')
        assert result[0].cardinality == 70

    def test_cardinality_8_decades(self):
        result = parse_time_references('8 decades ago')
        assert result[0].cardinality == 80

    def test_cardinality_9_decades(self):
        result = parse_time_references('9 decades ago')
        assert result[0].cardinality == 90

    def test_cardinality_10_decades(self):
        result = parse_time_references('10 decades ago')
        assert result[0].cardinality == 100
