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


class TestDecadeRegressions:
    """Ensure decade support does not break existing year tests"""

    def test_existing_1_year_ago(self):
        result = parse_time_references('1 year ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_existing_10_years_ago(self):
        result = parse_time_references('10 years ago')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_existing_last_year(self):
        result = parse_time_references('last year')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_existing_next_year(self):
        result = parse_time_references('next year')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'year'
        assert result[0].tense == 'future'

    def test_existing_100_years_ago(self):
        result = parse_time_references('100 years ago')
        assert len(result) == 1
        assert result[0].cardinality == 100
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'
