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


class TestDecadeHasTemporalInfo:
    """has_temporal_info returns True for all decade expressions"""

    def test_has_temporal_1_decade_ago(self):
        assert has_temporal_info('1 decade ago') is True

    def test_has_temporal_2_decades_ago(self):
        assert has_temporal_info('2 decades ago') is True

    def test_has_temporal_last_decade(self):
        assert has_temporal_info('last decade') is True

    def test_has_temporal_next_decade(self):
        assert has_temporal_info('next decade') is True

    def test_has_temporal_a_decade_ago(self):
        assert has_temporal_info('a decade ago') is True

    def test_has_temporal_past_decade(self):
        assert has_temporal_info('past decade') is True

    def test_has_temporal_3_decades_from_now(self):
        assert has_temporal_info('3 decades from now') is True

    def test_has_temporal_in_2_decades(self):
        assert has_temporal_info('in 2 decades') is True

    def test_has_temporal_a_decade_back(self):
        assert has_temporal_info('a decade back') is True

    def test_has_temporal_in_a_decade(self):
        assert has_temporal_info('in a decade') is True
