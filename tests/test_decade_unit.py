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


class TestDecadeAgo:
    """N decades ago -> past, year, N*10"""

    def test_1_decade_ago(self):
        result = parse_time_references('1 decade ago')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_2_decades_ago(self):
        result = parse_time_references('2 decades ago')
        assert len(result) == 1
        assert result[0].cardinality == 20
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_3_decades_ago(self):
        result = parse_time_references('3 decades ago')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_4_decades_ago(self):
        result = parse_time_references('4 decades ago')
        assert len(result) == 1
        assert result[0].cardinality == 40
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_5_decades_ago(self):
        result = parse_time_references('5 decades ago')
        assert len(result) == 1
        assert result[0].cardinality == 50
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_6_decades_ago(self):
        result = parse_time_references('6 decades ago')
        assert len(result) == 1
        assert result[0].cardinality == 60
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_7_decades_ago(self):
        result = parse_time_references('7 decades ago')
        assert len(result) == 1
        assert result[0].cardinality == 70
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_8_decades_ago(self):
        result = parse_time_references('8 decades ago')
        assert len(result) == 1
        assert result[0].cardinality == 80
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_9_decades_ago(self):
        result = parse_time_references('9 decades ago')
        assert len(result) == 1
        assert result[0].cardinality == 90
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_10_decades_ago(self):
        result = parse_time_references('10 decades ago')
        assert len(result) == 1
        assert result[0].cardinality == 100
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'


class TestDecadeBack:
    """N decades back -> past, year, N*10"""

    def test_1_decade_back(self):
        result = parse_time_references('1 decade back')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_2_decades_back(self):
        result = parse_time_references('2 decades back')
        assert len(result) == 1
        assert result[0].cardinality == 20
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_3_decades_back(self):
        result = parse_time_references('3 decades back')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_4_decades_back(self):
        result = parse_time_references('4 decades back')
        assert len(result) == 1
        assert result[0].cardinality == 40
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_5_decades_back(self):
        result = parse_time_references('5 decades back')
        assert len(result) == 1
        assert result[0].cardinality == 50
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_6_decades_back(self):
        result = parse_time_references('6 decades back')
        assert len(result) == 1
        assert result[0].cardinality == 60
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_7_decades_back(self):
        result = parse_time_references('7 decades back')
        assert len(result) == 1
        assert result[0].cardinality == 70
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_8_decades_back(self):
        result = parse_time_references('8 decades back')
        assert len(result) == 1
        assert result[0].cardinality == 80
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_9_decades_back(self):
        result = parse_time_references('9 decades back')
        assert len(result) == 1
        assert result[0].cardinality == 90
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_10_decades_back(self):
        result = parse_time_references('10 decades back')
        assert len(result) == 1
        assert result[0].cardinality == 100
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'


class TestDecadeBeforeNow:
    """N decades before now -> past, year, N*10"""

    def test_1_decade_before_now(self):
        result = parse_time_references('1 decade before now')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_2_decades_before_now(self):
        result = parse_time_references('2 decades before now')
        assert len(result) == 1
        assert result[0].cardinality == 20
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_3_decades_before_now(self):
        result = parse_time_references('3 decades before now')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_4_decades_before_now(self):
        result = parse_time_references('4 decades before now')
        assert len(result) == 1
        assert result[0].cardinality == 40
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_5_decades_before_now(self):
        result = parse_time_references('5 decades before now')
        assert len(result) == 1
        assert result[0].cardinality == 50
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_6_decades_before_now(self):
        result = parse_time_references('6 decades before now')
        assert len(result) == 1
        assert result[0].cardinality == 60
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_7_decades_before_now(self):
        result = parse_time_references('7 decades before now')
        assert len(result) == 1
        assert result[0].cardinality == 70
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_8_decades_before_now(self):
        result = parse_time_references('8 decades before now')
        assert len(result) == 1
        assert result[0].cardinality == 80
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_9_decades_before_now(self):
        result = parse_time_references('9 decades before now')
        assert len(result) == 1
        assert result[0].cardinality == 90
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_10_decades_before_now(self):
        result = parse_time_references('10 decades before now')
        assert len(result) == 1
        assert result[0].cardinality == 100
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'


class TestDecadePrior:
    """N decades prior -> past, year, N*10"""

    def test_1_decade_prior(self):
        result = parse_time_references('1 decade prior')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_2_decades_prior(self):
        result = parse_time_references('2 decades prior')
        assert len(result) == 1
        assert result[0].cardinality == 20
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_3_decades_prior(self):
        result = parse_time_references('3 decades prior')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_4_decades_prior(self):
        result = parse_time_references('4 decades prior')
        assert len(result) == 1
        assert result[0].cardinality == 40
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_5_decades_prior(self):
        result = parse_time_references('5 decades prior')
        assert len(result) == 1
        assert result[0].cardinality == 50
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_6_decades_prior(self):
        result = parse_time_references('6 decades prior')
        assert len(result) == 1
        assert result[0].cardinality == 60
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_7_decades_prior(self):
        result = parse_time_references('7 decades prior')
        assert len(result) == 1
        assert result[0].cardinality == 70
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_8_decades_prior(self):
        result = parse_time_references('8 decades prior')
        assert len(result) == 1
        assert result[0].cardinality == 80
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_9_decades_prior(self):
        result = parse_time_references('9 decades prior')
        assert len(result) == 1
        assert result[0].cardinality == 90
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_10_decades_prior(self):
        result = parse_time_references('10 decades prior')
        assert len(result) == 1
        assert result[0].cardinality == 100
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'


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


class TestDecadeIn:
    """in N decades -> future, year, N*10"""

    def test_in_1_decade(self):
        result = parse_time_references('in 1 decade')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'year'
        assert result[0].tense == 'future'

    def test_in_2_decades(self):
        result = parse_time_references('in 2 decades')
        assert len(result) == 1
        assert result[0].cardinality == 20
        assert result[0].frame == 'year'
        assert result[0].tense == 'future'

    def test_in_3_decades(self):
        result = parse_time_references('in 3 decades')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'year'
        assert result[0].tense == 'future'

    def test_in_4_decades(self):
        result = parse_time_references('in 4 decades')
        assert len(result) == 1
        assert result[0].cardinality == 40
        assert result[0].frame == 'year'
        assert result[0].tense == 'future'

    def test_in_5_decades(self):
        result = parse_time_references('in 5 decades')
        assert len(result) == 1
        assert result[0].cardinality == 50
        assert result[0].frame == 'year'
        assert result[0].tense == 'future'

    def test_in_6_decades(self):
        result = parse_time_references('in 6 decades')
        assert len(result) == 1
        assert result[0].cardinality == 60
        assert result[0].frame == 'year'
        assert result[0].tense == 'future'

    def test_in_7_decades(self):
        result = parse_time_references('in 7 decades')
        assert len(result) == 1
        assert result[0].cardinality == 70
        assert result[0].frame == 'year'
        assert result[0].tense == 'future'

    def test_in_8_decades(self):
        result = parse_time_references('in 8 decades')
        assert len(result) == 1
        assert result[0].cardinality == 80
        assert result[0].frame == 'year'
        assert result[0].tense == 'future'

    def test_in_9_decades(self):
        result = parse_time_references('in 9 decades')
        assert len(result) == 1
        assert result[0].cardinality == 90
        assert result[0].frame == 'year'
        assert result[0].tense == 'future'

    def test_in_10_decades(self):
        result = parse_time_references('in 10 decades')
        assert len(result) == 1
        assert result[0].cardinality == 100
        assert result[0].frame == 'year'
        assert result[0].tense == 'future'


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


class TestDecadeLastN:
    """last N decades -> past, year, N*10"""

    def test_last_2_decades(self):
        result = parse_time_references('last 2 decades')
        assert len(result) == 1
        assert result[0].cardinality == 20
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_last_3_decades(self):
        result = parse_time_references('last 3 decades')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_last_4_decades(self):
        result = parse_time_references('last 4 decades')
        assert len(result) == 1
        assert result[0].cardinality == 40
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_last_5_decades(self):
        result = parse_time_references('last 5 decades')
        assert len(result) == 1
        assert result[0].cardinality == 50
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_last_10_decades(self):
        result = parse_time_references('last 10 decades')
        assert len(result) == 1
        assert result[0].cardinality == 100
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'


class TestDecadeNextN:
    """next N decades -> future, year, N*10"""

    def test_next_2_decades(self):
        result = parse_time_references('next 2 decades')
        assert len(result) == 1
        assert result[0].cardinality == 20
        assert result[0].frame == 'year'
        assert result[0].tense == 'future'

    def test_next_3_decades(self):
        result = parse_time_references('next 3 decades')
        assert len(result) == 1
        assert result[0].cardinality == 30
        assert result[0].frame == 'year'
        assert result[0].tense == 'future'

    def test_next_4_decades(self):
        result = parse_time_references('next 4 decades')
        assert len(result) == 1
        assert result[0].cardinality == 40
        assert result[0].frame == 'year'
        assert result[0].tense == 'future'

    def test_next_5_decades(self):
        result = parse_time_references('next 5 decades')
        assert len(result) == 1
        assert result[0].cardinality == 50
        assert result[0].frame == 'year'
        assert result[0].tense == 'future'

    def test_next_10_decades(self):
        result = parse_time_references('next 10 decades')
        assert len(result) == 1
        assert result[0].cardinality == 100
        assert result[0].frame == 'year'
        assert result[0].tense == 'future'


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
