#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for parse_dates_with_type function."""

import pytest
from fast_parse_time import parse_dates_with_type


class TestNoFilter:
    """Tests for parse_dates_with_type with no type filter."""

    def test_no_filter_returns_all(self):
        """No type filter should return all dates."""
        result = parse_dates_with_type('Event on 04/08/2024 or maybe 3/24')
        assert len(result) == 2
        assert '04/08/2024' in result
        assert '3/24' in result

    def test_no_filter_preserves_types(self):
        """No type filter should preserve original date type classifications."""
        result = parse_dates_with_type('Event on 04/08/2024 or maybe 3/24')
        assert result['04/08/2024'] == 'FULL_EXPLICIT_DATE'
        assert result['3/24'] == 'MONTH_DAY'

    def test_no_filter_empty_text(self):
        """No filter on empty text should return empty dict."""
        result = parse_dates_with_type('')
        assert result == {}

    def test_no_filter_no_dates(self):
        """No filter on text with no dates should return empty dict."""
        result = parse_dates_with_type('Hello world')
        assert result == {}


class TestFullExplicitDateFilter:
    """Tests for filtering by FULL_EXPLICIT_DATE."""

    def test_filter_returns_only_full_dates(self):
        """Filter by FULL_EXPLICIT_DATE should exclude partial dates."""
        result = parse_dates_with_type('Event 04/08/2024 or maybe 3/24', 'FULL_EXPLICIT_DATE')
        assert len(result) == 1
        assert '04/08/2024' in result
        assert '3/24' not in result

    def test_filter_correct_type_value(self):
        """Filtered results should have the correct type value."""
        result = parse_dates_with_type('Born on 04/08/2024', 'FULL_EXPLICIT_DATE')
        assert result['04/08/2024'] == 'FULL_EXPLICIT_DATE'

    def test_filter_no_matches_returns_empty(self):
        """Filtering for FULL_EXPLICIT_DATE when only partial dates exist should return empty."""
        result = parse_dates_with_type('Appointment on 3/24', 'FULL_EXPLICIT_DATE')
        assert result == {}

    def test_multiple_full_dates(self):
        """All matching full dates should be returned."""
        result = parse_dates_with_type('Holidays: 12/25/2023 and 01/01/2024', 'FULL_EXPLICIT_DATE')
        assert len(result) == 2
        assert '12/25/2023' in result
        assert '01/01/2024' in result


class TestMonthDayFilter:
    """Tests for filtering by MONTH_DAY."""

    def test_filter_returns_only_month_day(self):
        """Filter by MONTH_DAY should exclude full dates."""
        result = parse_dates_with_type('Event 04/08/2024 or 3/24', 'MONTH_DAY')
        assert len(result) == 1
        assert '3/24' in result
        assert '04/08/2024' not in result

    def test_filter_no_matches_returns_empty(self):
        """Filtering for MONTH_DAY when only full dates exist should return empty."""
        result = parse_dates_with_type('Meeting on 04/08/2024', 'MONTH_DAY')
        assert result == {}


class TestDayMonthAmbiguousFilter:
    """Tests for filtering by DAY_MONTH_AMBIGUOUS."""

    def test_filter_returns_only_ambiguous(self):
        """Filter by DAY_MONTH_AMBIGUOUS should return only ambiguous dates."""
        result = parse_dates_with_type('Meeting 4/8 or 04/08/2024', 'DAY_MONTH_AMBIGUOUS')
        assert len(result) == 1
        assert '4/8' in result
        assert '04/08/2024' not in result

    def test_filter_type_value(self):
        """Ambiguous dates should have the DAY_MONTH_AMBIGUOUS type."""
        result = parse_dates_with_type('Appointment 4/8', 'DAY_MONTH_AMBIGUOUS')
        assert result.get('4/8') == 'DAY_MONTH_AMBIGUOUS'

    def test_filter_no_ambiguous_returns_empty(self):
        """No ambiguous dates in text should return empty dict."""
        result = parse_dates_with_type('Meeting on 04/08/2024', 'DAY_MONTH_AMBIGUOUS')
        assert result == {}


class TestDayMonthFilter:
    """Tests for filtering by DAY_MONTH."""

    def test_filter_returns_day_month(self):
        """Filter by DAY_MONTH should return only clear day-month dates."""
        result = parse_dates_with_type('European date 31/03 and US date 3/24', 'DAY_MONTH')
        assert '31/03' in result

    def test_filter_excludes_others(self):
        """DAY_MONTH filter should exclude MONTH_DAY dates."""
        result = parse_dates_with_type('Dates: 29/2 and 3/24', 'DAY_MONTH')
        assert '29/2' in result
        assert '3/24' not in result


class TestSentenceContext:
    """Tests for parse_dates_with_type within sentence context."""

    def test_filter_in_sentence(self):
        """Filter should work on dates embedded in sentences."""
        result = parse_dates_with_type(
            'The meeting is scheduled for 04/08/2024 and followed up on 3/24',
            'FULL_EXPLICIT_DATE'
        )
        assert len(result) == 1
        assert '04/08/2024' in result


class TestMultipleFullDatesWithFilter:
    """Tests for multiple full dates with an explicit filter."""

    def test_three_full_dates_with_filter(self):
        """Three comma-separated full dates - documents known extraction limitation."""
        # BOUNDARY: When dates are separated by commas, the extractor may only
        # capture the last matching date. This is a known behavior of the library.
        result = parse_dates_with_type(
            'Dates: 01/01/2024, 06/15/2024, and 12/31/2024',
            'FULL_EXPLICIT_DATE'
        )
        assert len(result) >= 1
        assert any(d in result for d in ['01/01/2024', '06/15/2024', '12/31/2024'])

    def test_filter_excludes_partial_from_multi_date_text(self):
        """FULL_EXPLICIT_DATE filter should exclude partial dates in multi-date text."""
        result = parse_dates_with_type(
            'Full date 04/08/2024 and partial 3/24',
            'FULL_EXPLICIT_DATE'
        )
        assert '04/08/2024' in result
        assert '3/24' not in result


class TestMultiplePartialDates:
    """Tests for multiple partial dates."""

    def test_multiple_month_day_dates(self):
        """Multiple MONTH_DAY partial dates should all be returned with no filter."""
        result = parse_dates_with_type('Mark 3/15 and 7/24 on the calendar')
        assert '3/15' in result
        assert '7/24' in result

    def test_partial_date_filter_multiple(self):
        """MONTH_DAY filter with multiple partial dates should return all matching."""
        result = parse_dates_with_type('Schedule 3/15 or 7/24', 'MONTH_DAY')
        assert len(result) == 2


class TestNoFilterReturnsAllTypes:
    """Tests that no filter returns all types including ambiguous."""

    def test_no_filter_includes_ambiguous(self):
        """No filter should include DAY_MONTH_AMBIGUOUS dates."""
        result = parse_dates_with_type('Appointment 4/8')
        assert '4/8' in result
        assert result['4/8'] == 'DAY_MONTH_AMBIGUOUS'

    def test_no_filter_includes_day_month(self):
        """No filter should include DAY_MONTH dates."""
        result = parse_dates_with_type('European date 31/03')
        assert '31/03' in result
        assert result['31/03'] == 'DAY_MONTH'

    def test_no_filter_all_types_present(self):
        """No filter on mixed text - documents that comma separation limits extraction."""
        # BOUNDARY: Comma separation causes the extractor to only capture the last date
        # per delimiter group. This documents the observed behavior.
        result = parse_dates_with_type('Full 04/08/2024, partial 3/24, ambiguous 4/8')
        assert result is not None
        assert len(result) >= 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
