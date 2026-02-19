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


class TestDecadeSentenceContext:
    """Decade extraction works when embedded in surrounding prose"""

    def test_sentence_2_decades_ago(self):
        result = parse_time_references('the policy was introduced 2 decades ago')
        assert len(result) == 1
        assert result[0].cardinality == 20
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_sentence_last_decade(self):
        result = parse_time_references('revenues have doubled in the last decade')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_sentence_next_decade(self):
        result = parse_time_references('the project will be completed in the next decade')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'year'
        assert result[0].tense == 'future'

    def test_sentence_a_decade_ago(self):
        result = parse_time_references('this technology was invented a decade ago')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_sentence_3_decades_ago(self):
        result = parse_time_references('the building was constructed 3 decades ago')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_sentence_in_2_decades(self):
        result = parse_time_references('we expect to be done in 2 decades')
        assert len(result) == 1
        assert result[0].cardinality == 20
        assert result[0].frame == 'year'
        assert result[0].tense == 'future'

    def test_sentence_5_decades_from_now(self):
        result = parse_time_references('the fund matures 5 decades from now')
        assert len(result) == 1
        assert result[0].cardinality == 50
        assert result[0].frame == 'year'
        assert result[0].tense == 'future'

    def test_sentence_over_the_last_decade(self):
        result = parse_time_references('growth has accelerated over the last decade')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_sentence_past_decade(self):
        result = parse_time_references('we have seen rapid change in the past decade')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_sentence_4_decades_back(self):
        result = parse_time_references('the original site was established 4 decades back')
        assert len(result) == 1
        assert result[0].cardinality == 40
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'
