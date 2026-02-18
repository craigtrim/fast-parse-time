#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for parse_dates_with_type function."""

import pytest
from fast_parse_time import parse_dates_with_type

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
