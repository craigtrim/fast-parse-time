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


class TestDecadeCapitalization:
    """Capitalization variants are handled correctly"""

    def test_upper_a_decade_ago(self):
        result = parse_time_references('A Decade Ago')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_upper_last_decade(self):
        result = parse_time_references('Last Decade')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'year'

    def test_upper_next_decade(self):
        result = parse_time_references('Next Decade')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'year'

    def test_upper_2_decades_ago(self):
        result = parse_time_references('2 Decades Ago')
        assert len(result) == 1
        assert result[0].cardinality == 20
        assert result[0].frame == 'year'

    def test_upper_3_decades_from_now(self):
        result = parse_time_references('3 Decades From Now')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'year'
