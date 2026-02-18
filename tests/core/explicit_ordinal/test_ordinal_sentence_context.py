#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for ordinal date patterns embedded in sentence context.

Related GitHub Issue:
    #22 - Gap: ordinal day format not supported (12th day of December, 19th day of May)
    https://github.com/craigtrim/fast-parse-time/issues/22
"""

import pytest
from fast_parse_time import extract_explicit_dates


class TestOrdinalSentenceContext:
    """Ordinal date patterns embedded in natural language sentences."""

    # ── 'NNth day of Month YYYY' in sentences ─────────────────────────────────

    def test_contract_signed_12th_day_of_december_2001(self):
        result = extract_explicit_dates(
            'This agreement was entered into on the 12th day of December, 2001.'
        )
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_born_19th_day_of_may_2015(self):
        result = extract_explicit_dates(
            'He was born on the 19th day of May, 2015 at dawn.'
        )
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_legal_effective_1st_day_of_january(self):
        result = extract_explicit_dates(
            'Effective the 1st day of January, 2024, all provisions shall apply.'
        )
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    # ── 'the NNth of Month' in sentences ─────────────────────────────────────

    def test_meeting_on_the_3rd_of_march_2024(self):
        result = extract_explicit_dates('meeting on the 3rd of March 2024 at noon')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_she_was_born_the_12th_of_december(self):
        result = extract_explicit_dates('She was born on the 12th of December.')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_deadline_the_31st_of_october_2025(self):
        result = extract_explicit_dates(
            'Please submit your application by the 31st of October 2025.'
        )
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_event_on_the_15th_of_june(self):
        result = extract_explicit_dates(
            'The annual event occurs on the 15th of June each year.'
        )
        assert result
        assert 'DAY_MONTH' in result.values()

    # ── 'NNth of Month' in sentences ─────────────────────────────────────────

    def test_submit_by_2nd_of_february(self):
        result = extract_explicit_dates('Submit your report by 2nd of February.')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_appointment_21st_of_july_2024(self):
        result = extract_explicit_dates(
            'Your appointment is on 21st of July 2024.'
        )
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_returned_3rd_of_march_2022(self):
        result = extract_explicit_dates(
            'The package was returned on 3rd of March 2022.'
        )
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    # ── 'Month NNth' in sentences ─────────────────────────────────────────────

    def test_deadline_is_december_12th(self):
        result = extract_explicit_dates('The deadline is December 12th.')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_report_due_may_19th(self):
        result = extract_explicit_dates('The report is due May 19th.')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_meeting_oct_23rd(self):
        result = extract_explicit_dates('We have a meeting on Oct 23rd.')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_training_sep_3rd(self):
        result = extract_explicit_dates('Training begins Sep 3rd.')
        assert result
        assert 'DAY_MONTH' in result.values()

    # ── 'NNth Month' in sentences ─────────────────────────────────────────────

    def test_event_on_3rd_march(self):
        result = extract_explicit_dates('The event is on 3rd March.')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_closes_25th_dec(self):
        result = extract_explicit_dates('Office closes 25th Dec.')
        assert result
        assert 'DAY_MONTH' in result.values()

    def test_starts_1st_jan(self):
        result = extract_explicit_dates('The new policy starts 1st Jan.')
        assert result
        assert 'DAY_MONTH' in result.values()

    # ── multiple dates in one sentence ────────────────────────────────────────

    def test_date_range_written(self):
        result = extract_explicit_dates(
            'i am looking for a date june 4th 1996 to july 3rd 2013'
        )
        assert result
        assert len(result) >= 1

    def test_two_ordinal_dates(self):
        result = extract_explicit_dates(
            'Meetings on the 1st of January and the 15th of February.'
        )
        assert result
        assert len(result) >= 1
