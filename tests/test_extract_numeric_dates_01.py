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


if __name__ == '__main__':
    unittest.main()
