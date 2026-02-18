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
