#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for get_date_range function."""

import pytest
from datetime import datetime
from fast_parse_time import get_date_range

class TestSameTenseRange:
    """Tests that two references in the same tense still form a valid range."""

    def test_both_past_forms_valid_range(self):
        """Two past-tense references should still yield a valid ordered range."""
        result = get_date_range('from 10 days ago to 5 days ago')
        assert result is not None
        start, end = result
        assert start < end

    def test_both_past_returns_tuple(self):
        """Two past-tense references should return a tuple."""
        result = get_date_range('between 14 days ago and 7 days ago')
        assert result is not None
        assert isinstance(result, tuple)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
