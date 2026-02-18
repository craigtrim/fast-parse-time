# -*- coding: utf-8 -*-
"""
Test parsing of natural language phrases.
Source: https://github.com/bear/parsedatetime/blob/master/tests/TestPhrases.py
"""
import pytest
from fast_parse_time import parse_time_references

pytestmark = pytest.mark.xfail(strict=False, reason='Compatibility test - implementation gap')


class TestLastPhrases:
    """Source: testLastPhrases -- 'last <weekday>' patterns"""

    def test_last_friday(self):
        result = parse_time_references('last friday')
        assert len(result) == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_last_monday(self):
        result = parse_time_references('last monday')
        assert len(result) == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_last_wednesday(self):
        result = parse_time_references('last wednesday')
        assert len(result) == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'


class TestEndOfPhrases:
    """
    Source: testEndOfPhrases -- 'eom', 'eoy' (end-of-month, end-of-year) abbreviations.
    parsedatetime resolves these to the last day of the current month/year.
    """

    def test_eod(self):
        """end of day"""
        result = parse_time_references('eod')
        assert len(result) == 1
        assert result[0].frame in ('hour', 'day')
        assert result[0].tense == 'future'

    def test_eom(self):
        """end of month"""
        result = parse_time_references('eom')
        assert len(result) == 1
        assert result[0].frame == 'month'
        assert result[0].tense == 'future'

    def test_eoy(self):
        """end of year"""
        result = parse_time_references('eoy')
        assert len(result) == 1
        assert result[0].frame == 'year'
        assert result[0].tense == 'future'
