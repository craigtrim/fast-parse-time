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
