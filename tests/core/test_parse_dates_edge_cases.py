#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Edge case tests for parse_dates and related functions."""

import pytest
from fast_parse_time import (
    parse_dates,
    has_temporal_info,
    ParseResult,
    ExplicitDate,
    RelativeTime,
)


class TestEmptyAndNoContent:
    """Tests for empty string and text with no temporal content."""

    def test_empty_string_returns_parse_result(self):
        """Empty string should return a ParseResult, not None or raise."""
        result = parse_dates('')
        assert isinstance(result, ParseResult)

    def test_empty_string_has_no_explicit_dates(self):
        """Empty string should yield no explicit dates."""
        result = parse_dates('')
        assert result.explicit_dates == []

    def test_empty_string_has_no_relative_times(self):
        """Empty string should yield no relative times."""
        result = parse_dates('')
        assert result.relative_times == []

    def test_empty_string_has_dates_is_false(self):
        """Empty string should have has_dates == False."""
        result = parse_dates('')
        assert result.has_dates is False

    def test_no_temporal_text_returns_parse_result(self):
        """Text with no dates should return a ParseResult."""
        result = parse_dates('Hello world, this is just text')
        assert isinstance(result, ParseResult)

    def test_no_temporal_text_has_no_dates(self):
        """Text with no dates should have empty lists."""
        result = parse_dates('Hello world, this is just text')
        assert result.explicit_dates == []
        assert result.relative_times == []

    def test_no_temporal_text_has_dates_is_false(self):
        """Text with no dates should have has_dates == False."""
        result = parse_dates('Hello world, this is just text')
        assert result.has_dates is False


class TestOnlyExplicitDates:
    """Tests for text containing only explicit dates."""

    def test_only_explicit_date_has_dates_is_true(self):
        """Text with only an explicit date should have has_dates == True."""
        result = parse_dates('Event on 04/08/2024')
        assert result.has_dates is True

    def test_only_explicit_date_has_one_explicit(self):
        """Text with one date should have one explicit date."""
        result = parse_dates('Event on 04/08/2024')
        assert len(result.explicit_dates) == 1

    def test_only_explicit_date_has_no_relative_times(self):
        """Text with only an explicit date should have no relative times."""
        result = parse_dates('Event on 04/08/2024')
        assert result.relative_times == []

    def test_explicit_date_type(self):
        """Explicit date should be an ExplicitDate instance."""
        result = parse_dates('Event on 04/08/2024')
        assert isinstance(result.explicit_dates[0], ExplicitDate)

    def test_explicit_date_text_preserved(self):
        """Explicit date text should match original."""
        result = parse_dates('Event on 04/08/2024')
        assert result.explicit_dates[0].text == '04/08/2024'

    def test_explicit_date_type_classified(self):
        """Explicit date should have a date_type field."""
        result = parse_dates('Event on 04/08/2024')
        assert result.explicit_dates[0].date_type == 'FULL_EXPLICIT_DATE'


class TestOnlyRelativeTimes:
    """Tests for text containing only relative time references."""

    def test_only_relative_time_has_dates_is_true(self):
        """Text with only a relative time should have has_dates == True."""
        result = parse_dates('5 days ago')
        assert result.has_dates is True

    def test_only_relative_time_has_no_explicit_dates(self):
        """Text with only a relative time should have no explicit dates."""
        result = parse_dates('5 days ago')
        assert result.explicit_dates == []

    def test_only_relative_time_has_one_relative(self):
        """Text with one relative time should have one entry."""
        result = parse_dates('5 days ago')
        assert len(result.relative_times) == 1

    def test_relative_time_type(self):
        """Relative time should be a RelativeTime instance."""
        result = parse_dates('5 days ago')
        assert isinstance(result.relative_times[0], RelativeTime)

    def test_relative_time_cardinality(self):
        """Relative time cardinality should be correct."""
        result = parse_dates('5 days ago')
        assert result.relative_times[0].cardinality == 5

    def test_relative_time_frame(self):
        """Relative time frame should be correct."""
        result = parse_dates('5 days ago')
        assert result.relative_times[0].frame == 'day'

    def test_relative_time_tense(self):
        """Relative time tense should be correct."""
        result = parse_dates('5 days ago')
        assert result.relative_times[0].tense == 'past'


class TestBothTypes:
    """Tests for text with both explicit dates and relative times."""

    def test_both_types_has_dates_is_true(self):
        """Text with both types should have has_dates == True."""
        result = parse_dates('Meeting on 04/08/2024 about issues from 5 days ago')
        assert result.has_dates is True

    def test_both_types_explicit_dates_count(self):
        """Should have one explicit date."""
        result = parse_dates('Meeting on 04/08/2024 about issues from 5 days ago')
        assert len(result.explicit_dates) == 1

    def test_both_types_relative_times_count(self):
        """Should have one relative time."""
        result = parse_dates('Meeting on 04/08/2024 about issues from 5 days ago')
        assert len(result.relative_times) == 1

    def test_both_types_explicit_date_value(self):
        """Explicit date text should be correct."""
        result = parse_dates('Meeting on 04/08/2024 about issues from 5 days ago')
        assert result.explicit_dates[0].text == '04/08/2024'

    def test_both_types_relative_time_values(self):
        """Relative time values should be correct."""
        result = parse_dates('Meeting on 04/08/2024 about issues from 5 days ago')
        rt = result.relative_times[0]
        assert rt.cardinality == 5
        assert rt.frame == 'day'
        assert rt.tense == 'past'


class TestHasTemporalInfo:
    """Tests for has_temporal_info function edge cases."""

    def test_empty_string_is_false(self):
        """Empty string should return False."""
        assert has_temporal_info('') is False

    def test_plain_text_is_false(self):
        """Plain text without dates should return False."""
        assert has_temporal_info('Just a regular sentence about stuff') is False

    def test_explicit_date_is_true(self):
        """Text with explicit date should return True."""
        assert has_temporal_info('Meeting on 04/08/2024') is True

    def test_relative_time_is_true(self):
        """Text with relative time should return True."""
        assert has_temporal_info('5 days ago') is True

    def test_yesterday_is_true(self):
        """'yesterday' should return True."""
        assert has_temporal_info('I saw this yesterday') is True

    def test_last_week_is_true(self):
        """'last week' should return True."""
        assert has_temporal_info('show data from last week') is True

    def test_written_month_is_true(self):
        """Written month date should return True."""
        assert has_temporal_info('Meeting on March 15, 2024') is True

    def test_numbers_only_is_false(self):
        """Text with numbers but no dates should return False."""
        assert has_temporal_info('The answer is 42') is False


class TestWrittenMonthThroughParseDate:
    """Tests for written month formats going through parse_dates."""

    def test_written_month_extracted(self):
        """Written month date should be in explicit_dates."""
        result = parse_dates('Meeting on March 15, 2024')
        assert len(result.explicit_dates) >= 1

    def test_written_month_has_dates(self):
        """Written month date should set has_dates True."""
        result = parse_dates('Meeting on March 15, 2024')
        assert result.has_dates is True

    def test_written_month_type(self):
        """Written month date should be classified as FULL_EXPLICIT_DATE."""
        result = parse_dates('Meeting on March 15, 2024')
        assert any(ed.date_type == 'FULL_EXPLICIT_DATE' for ed in result.explicit_dates)


class TestWhitespaceAndNoDateStrings:
    """Tests for whitespace-only and numbers-only strings."""

    def test_whitespace_only_string(self):
        """Whitespace-only string should return a ParseResult with no dates."""
        result = parse_dates('   ')
        assert isinstance(result, ParseResult)
        assert result.has_dates is False

    def test_whitespace_only_has_temporal_info_false(self):
        """Whitespace-only string should return False from has_temporal_info."""
        assert has_temporal_info('   ') is False

    def test_numbers_only_no_dates(self):
        """String with only numbers (no date format) should have no dates."""
        result = parse_dates('42 100 999')
        assert result.has_dates is False

    def test_numbers_only_has_temporal_info_false(self):
        """String with only unstructured numbers should return False."""
        assert has_temporal_info('42 100 999') is False


class TestMultipleRelativeTimes:
    """Tests for multiple relative time expressions in one sentence."""

    def test_two_relative_times_in_sentence(self):
        """Two relative time references in one sentence should both be extracted."""
        result = parse_dates('data from 7 days ago and 3 days ago')
        assert result.has_dates is True
        assert len(result.relative_times) == 2

    def test_two_relative_times_cardinalities(self):
        """Both relative time cardinalities should be correct."""
        result = parse_dates('data from 7 days ago and 3 days ago')
        cardinalities = {rt.cardinality for rt in result.relative_times}
        assert 7 in cardinalities
        assert 3 in cardinalities


class TestRelativeAndExplicitMixed:
    """Tests for a relative time and explicit date in the same sentence."""

    def test_relative_and_explicit_has_dates(self):
        """Sentence with both a relative time and an explicit date should have_dates True."""
        result = parse_dates('set deadline 04/15/2024 based on data from 30 days ago')
        assert result.has_dates is True

    def test_relative_and_explicit_both_extracted(self):
        """Both the explicit date and relative time should be extracted."""
        result = parse_dates('set deadline 04/15/2024 based on data from 30 days ago')
        assert len(result.explicit_dates) >= 1
        assert len(result.relative_times) >= 1


class TestMoreHasTemporalInfoVariants:
    """Additional has_temporal_info variant tests."""

    def test_tomorrow_is_true(self):
        """'tomorrow' should return True."""
        assert has_temporal_info('tomorrow') is True

    def test_next_week_is_true(self):
        """'next week' should return True."""
        assert has_temporal_info('next week') is True

    def test_numeric_date_is_true(self):
        """A numeric date string should return True."""
        assert has_temporal_info('04/08/2024') is True

    def test_random_words_is_false(self):
        """Sentence with no temporal references should return False."""
        assert has_temporal_info('the quick brown fox') is False


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
