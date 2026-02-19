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


class TestDecadeSingularForms:
    """Singular natural-language forms: last decade, next decade, a decade ago, etc."""

    def test_a_decade_ago(self):
        result = parse_time_references('a decade ago')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_last_decade(self):
        result = parse_time_references('last decade')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_past_decade(self):
        result = parse_time_references('past decade')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_next_decade(self):
        result = parse_time_references('next decade')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'year'
        assert result[0].tense == 'future'

    def test_in_a_decade(self):
        result = parse_time_references('in a decade')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'year'
        assert result[0].tense == 'future'

    def test_a_decade_back(self):
        result = parse_time_references('a decade back')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_a_decade_prior(self):
        result = parse_time_references('a decade prior')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_a_decade_before_now(self):
        result = parse_time_references('a decade before now')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_1_decade(self):
        """Bare '1 decade' without direction - defaults to past"""
        result = parse_time_references('1 decade')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_a_decade_from_now(self):
        result = parse_time_references('a decade from now')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'year'
        assert result[0].tense == 'future'
