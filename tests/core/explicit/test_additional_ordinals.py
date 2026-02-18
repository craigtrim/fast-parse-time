#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for written month name formats in explicit dates."""

import pytest
from fast_parse_time import extract_explicit_dates

class TestAdditionalOrdinals:
    """Tests for additional ordinal day suffixes."""

    def test_ordinal_5th(self):
        """'March 5th, 2024' should be parsed."""
        result = extract_explicit_dates('March 5th, 2024')
        assert len(result) == 1

    def test_ordinal_11th(self):
        """'July 11th, 2024' should be parsed."""
        result = extract_explicit_dates('July 11th, 2024')
        assert len(result) == 1

    def test_ordinal_12th(self):
        """'August 12th, 2024' should be parsed."""
        result = extract_explicit_dates('August 12th, 2024')
        assert len(result) == 1

    def test_ordinal_21st(self):
        """'October 21st, 2024' should be parsed."""
        result = extract_explicit_dates('October 21st, 2024')
        assert len(result) == 1

    def test_ordinal_22nd(self):
        """'November 22nd, 2024' should be parsed."""
        result = extract_explicit_dates('November 22nd, 2024')
        assert len(result) == 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
