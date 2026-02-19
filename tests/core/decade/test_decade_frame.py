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


class TestDecadeFrame:
    """Decade always resolves to frame='year'"""

    def test_frame_ago(self):
        result = parse_time_references('3 decades ago')
        assert result[0].frame == 'year'

    def test_frame_back(self):
        result = parse_time_references('3 decades back')
        assert result[0].frame == 'year'

    def test_frame_before_now(self):
        result = parse_time_references('3 decades before now')
        assert result[0].frame == 'year'

    def test_frame_prior(self):
        result = parse_time_references('3 decades prior')
        assert result[0].frame == 'year'

    def test_frame_from_now(self):
        result = parse_time_references('3 decades from now')
        assert result[0].frame == 'year'

    def test_frame_in(self):
        result = parse_time_references('in 3 decades')
        assert result[0].frame == 'year'

    def test_frame_last_decade(self):
        result = parse_time_references('last decade')
        assert result[0].frame == 'year'

    def test_frame_next_decade(self):
        result = parse_time_references('next decade')
        assert result[0].frame == 'year'

    def test_frame_a_decade_ago(self):
        result = parse_time_references('a decade ago')
        assert result[0].frame == 'year'

    def test_frame_past_decade(self):
        result = parse_time_references('past decade')
        assert result[0].frame == 'year'
