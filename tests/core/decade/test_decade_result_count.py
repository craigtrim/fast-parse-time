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


class TestDecadeResultCount:
    """Exactly one result returned for each decade expression"""

    def test_count_1_decade_ago(self):
        result = parse_time_references('1 decade ago')
        assert len(result) == 1

    def test_count_2_decades_ago(self):
        result = parse_time_references('2 decades ago')
        assert len(result) == 1

    def test_count_last_decade(self):
        result = parse_time_references('last decade')
        assert len(result) == 1

    def test_count_next_decade(self):
        result = parse_time_references('next decade')
        assert len(result) == 1

    def test_count_a_decade_ago(self):
        result = parse_time_references('a decade ago')
        assert len(result) == 1

    def test_count_3_decades_from_now(self):
        result = parse_time_references('3 decades from now')
        assert len(result) == 1

    def test_count_in_5_decades(self):
        result = parse_time_references('in 5 decades')
        assert len(result) == 1

    def test_count_a_decade_back(self):
        result = parse_time_references('a decade back')
        assert len(result) == 1

    def test_count_past_decade(self):
        result = parse_time_references('past decade')
        assert len(result) == 1

    def test_count_in_a_decade(self):
        result = parse_time_references('in a decade')
        assert len(result) == 1
