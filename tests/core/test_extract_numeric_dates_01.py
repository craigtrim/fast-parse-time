#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import unittest
from typing import Dict
from fast_parse_time import extract_numeric_dates, DateType


class DelimitedDateClassifierTest(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def compare(self, input_text: str, d_expected: Dict[str, DateType]) -> None:
        d_actual: Dict[str, DateType] = extract_numeric_dates(input_text)

        if d_actual is None:
            if d_expected is not None:
                print(
                    f'Error: Input Text `{input_text}` is unexpectedly null')
            self.assertIsNone(d_actual)

        if d_expected is None and d_actual is not None:
            self.assertIsNotNone(d_actual)

        if d_actual != d_expected:
            print(
                f'Error: Input Text `{input_text}` is {d_actual} not {d_expected}')

        self.assertEqual(d_actual, d_expected)

    def test_full_dates(self):
        self.compare(
            input_text='date of birth: 04/08/2024',
            d_expected={'04/08/2024': 'FULL_EXPLICIT_DATE'})

    def test_month_days_true_positives(self):
        self.compare(
            input_text='blah blah 3 / 24', d_expected=None)
        self.compare(
            input_text='blah blah 3/24', d_expected={'3/24': 'MONTH_DAY'})

    def test_month_days_false_positives(self):
        self.compare(
            input_text='blah blah 3/32 blah blah', d_expected=None)

    def test_needs_validation(self):
        self.compare(
            input_text='blah blah 2/30 blah blah', d_expected=None)

    def test_month_days_ambiguous(self):
        self.compare(
            input_text='4-8', d_expected=None)
        self.compare(
            input_text='4.8', d_expected=None)

        # TODO: assumption ...
        self.compare(
            input_text='4/8', d_expected={'4/8': 'DAY_MONTH_AMBIGUOUS'})

    def test_full_date_dash_delimiter(self):
        """A full date with dash delimiter should be extracted as FULL_EXPLICIT_DATE."""
        self.compare(
            input_text='appointment on 12-31-2023',
            d_expected={'12-31-2023': 'FULL_EXPLICIT_DATE'})

    def test_full_date_dot_delimiter(self):
        """A full date with dot delimiter should be extracted as FULL_EXPLICIT_DATE."""
        self.compare(
            input_text='deadline is 11.30.2024',
            d_expected={'11.30.2024': 'FULL_EXPLICIT_DATE'})

    def test_iso_format_date(self):
        """An ISO format date (YYYY-MM-DD) should be extracted as FULL_EXPLICIT_DATE."""
        self.compare(
            input_text='ISO date format 2023-05-17',
            d_expected={'2023-05-17': 'FULL_EXPLICIT_DATE'})

    def test_day_month_partial(self):
        """A partial date where first component exceeds 12 should be DAY_MONTH."""
        self.compare(
            input_text='blah blah 31/03',
            d_expected={'31/03': 'DAY_MONTH'})

    def test_multiple_dates_in_text(self):
        """Multiple full dates in one string should all be extracted."""
        self.compare(
            input_text='holidays are 12/25/2023 and 01/01/2024',
            d_expected={'12/25/2023': 'FULL_EXPLICIT_DATE', '01/01/2024': 'FULL_EXPLICIT_DATE'})

    def test_month_day_unambiguous(self):
        """Month/day partial date where second component exceeds 12 should be MONTH_DAY."""
        self.compare(
            input_text='party on 7/24',
            d_expected={'7/24': 'MONTH_DAY'})

    def test_full_date_slash_additional(self):
        """Additional slash-delimited full date should be extracted."""
        self.compare(
            input_text='event on 06/15/2020',
            d_expected={'06/15/2020': 'FULL_EXPLICIT_DATE'})


if __name__ == '__main__':
    unittest.main()
