#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import unittest
from fast_parse_time.explicit.svc import TokenizeNumericComponents


class TokenizeNumericComponentsTest(unittest.TestCase):
    '''
    Common Test Cases
    '''

    def setUp(self) -> None:
        self.tokenizer: TokenizeNumericComponents = TokenizeNumericComponents()

    def tearDown(self) -> None:
        self.tokenizer = None

    def test_date_of_birth(self):
        self.assertEqual(self.tokenizer.process(
            'Date of Birth: 06/23/2004'), ['06/23/2004'])

    def test_dash_delimited_date(self):
        self.assertEqual(self.tokenizer.process(
            'Event on 12-31-2023'), ['12-31-2023'])

    def test_dot_delimited_date(self):
        self.assertEqual(self.tokenizer.process(
            'Deadline is 11.30.2024'), ['11.30.2024'])

    def test_invalid_date_01(self):
        self.assertIsNone(self.tokenizer.process('Invalid date 32/13/2003'))

    def test_invalid_date_02(self):
        self.assertIsNone(self.tokenizer.process('Invalid date 32/13/2003'))

    def test_year_only(self):
        self.assertEqual(self.tokenizer.process('Copyright 2023'), ['2023'])

    def test_year_out_of_range(self):
        self.assertIsNone(self.tokenizer.process('Time machine to 1820'))

    def test_future_year_within_range(self):
        self.assertEqual(self.tokenizer.process('Planning for 2030'), ['2030'])

    def test_phone_number(self):
        self.assertIsNone(self.tokenizer.process('Call me at 800-123-4567'))

    def test_with_time(self):
        self.assertIsNone(self.tokenizer.process('Alarm set for 08:00 AM'))

    def test_with_iso_date(self):
        self.assertEqual(self.tokenizer.process(
            'ISO date format 2023-05-17'), ['2023-05-17'])

    def test_with_multiple_dates(self):
        self.assertEqual(self.tokenizer.process(
            'Holidays are 12/25/2023 and 01/01/2024'), ['12/25/2023', '01/01/2024'])

    def test_with_text_and_numbers(self):
        self.assertIsNone(self.tokenizer.process('One hundred twenty-three'))

    def test_mixed_date_and_text(self):
        self.assertEqual(self.tokenizer.process(
            'Meet on the 5th of July 2023'), ['2023'])

    def test_date_with_text_month(self):
        self.assertEqual(self.tokenizer.process(
            'Your appointment is April 15th, 2023'), ['2023'])

    def test_only_month_and_day(self):
        self.assertEqual(self.tokenizer.process(
            'Birthday party on 07/24'), ['07/24'])

    def test_invalid_numeric_string(self):
        self.assertIsNone(self.tokenizer.process('Version 1234.567.89'))

    def test_price_tag(self):
        self.assertIsNone(self.tokenizer.process('Total cost is $299.99'))

    def test_with_large_number(self):
        self.assertIsNone(self.tokenizer.process('Population reaches 7891234'))

    def test_with_negative_number(self):
        self.assertIsNone(self.tokenizer.process('Temperature drops to -15C'))

    def test_incorrect_delimiter(self):
        self.assertIsNone(self.tokenizer.process('Mistyped date 12_31_2023'))

    def test_decimal_number(self):
        self.assertIsNone(self.tokenizer.process('Average rating is 4.5'))

    def test_empty_string(self):
        self.assertIsNone(self.tokenizer.process(''))

    def test_single_number(self):
        self.assertIsNone(self.tokenizer.process('Number 42'))

    def test_date_with_leading_zeros(self):
        self.assertEqual(self.tokenizer.process(
            'Deadline by 01/02/2024'), ['01/02/2024'])

    # ------------------------------------------------------------------------------
    # Cluster:    Test Cases with Probable Tokenization Requirements
    #
    def test_date_with_extra_characters(self):
        self.assertIsNone(self.tokenizer.process('Important: 01-01-2024!'))

    def test_date_span(self):
        self.assertIsNone(self.tokenizer.process('Project duration 2023-2024'))
    # ------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------
    # Cluster:    Test Cases with Edge Case Tokenization
    #
    def test_year_with_prefix(self):
        self.assertIsNone(self.tokenizer.process('Since the year AD2023'))
    # ------------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
