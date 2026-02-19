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


class TestDecadeTense:
    """Tense detection for past vs future decade expressions"""

    def test_tense_ago_is_past(self):
        result = parse_time_references('2 decades ago')
        assert result[0].tense == 'past'

    def test_tense_back_is_past(self):
        result = parse_time_references('2 decades back')
        assert result[0].tense == 'past'

    def test_tense_before_now_is_past(self):
        result = parse_time_references('2 decades before now')
        assert result[0].tense == 'past'

    def test_tense_prior_is_past(self):
        result = parse_time_references('2 decades prior')
        assert result[0].tense == 'past'

    def test_tense_last_decade_is_past(self):
        result = parse_time_references('last decade')
        assert result[0].tense == 'past'

    def test_tense_past_decade_is_past(self):
        result = parse_time_references('past decade')
        assert result[0].tense == 'past'

    def test_tense_a_decade_ago_is_past(self):
        result = parse_time_references('a decade ago')
        assert result[0].tense == 'past'

    def test_tense_from_now_is_future(self):
        result = parse_time_references('2 decades from now')
        assert result[0].tense == 'future'

    def test_tense_in_decades_is_future(self):
        result = parse_time_references('in 2 decades')
        assert result[0].tense == 'future'

    def test_tense_next_decade_is_future(self):
        result = parse_time_references('next decade')
        assert result[0].tense == 'future'
