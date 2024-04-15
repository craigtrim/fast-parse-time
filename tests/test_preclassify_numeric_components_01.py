#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import unittest
from fast_parse_time.explicit.svc import TokenizeNumericComponents


class TokenizeNumericComponentsTest(unittest.TestCase):

    def setUp(self) -> None:
        self.tokenizer: TokenizeNumericComponents = TokenizeNumericComponents()

    def tearDown(self) -> None:
        self.tokenizer = None

    def test_date_of_birth(self):
        self.assertTrue(self.tokenizer.process('Date of Birth: 06/23/2004'))

    def test_with_dash_delimited_date(self):
        self.assertTrue(self.tokenizer.process('Meeting on 12-05-2020'))

    def test_with_dot_delimited_date(self):
        self.assertTrue(self.tokenizer.process(
            'Vacation starts on 21.07.2023'))

    def test_with_mixed_characters(self):
        self.assertFalse(self.tokenizer.process('Deadline: 30-06.2024'))

    def test_with_numeric_only(self):
        self.assertTrue(self.tokenizer.process('Reminder set for 2025'))

    def test_with_no_numeric(self):
        self.assertFalse(self.tokenizer.process('Tomorrow is the deadline'))

    def test_with_text_month(self):
        self.assertFalse(self.tokenizer.process('Appointment on January 12th'))

    def test_with_alphanumeric(self):
        self.assertFalse(self.tokenizer.process('Code ABC1234 is active'))

    def test_with_time(self):
        self.assertFalse(self.tokenizer.process('Alarm at 12:00'))

    def test_with_date_and_time(self):
        self.assertTrue(self.tokenizer.process('Event on 03/15/2023 at 18:00'))

    def test_with_iso_date(self):
        self.assertTrue(self.tokenizer.process('ISO date 2023-04-05'))

    def test_with_leading_zeros(self):
        self.assertFalse(self.tokenizer.process('Version 0.12.0'))

    def test_with_trailing_zeros(self):
        self.assertFalse(self.tokenizer.process('Balance: 123.00'))

    def test_with_internal_zeros(self):
        self.assertFalse(self.tokenizer.process('ID 00204 found'))

    def test_with_numeric_word(self):
        self.assertFalse(self.tokenizer.process('One hundred files processed'))

    def test_with_phone_number(self):
        self.assertFalse(self.tokenizer.process('Call me at 123-456-7890'))

    def test_with_postal_code(self):
        self.assertFalse(self.tokenizer.process('Address: 12345 Main St.'))

    def test_with_price(self):
        self.assertFalse(self.tokenizer.process('Total is $123.45'))

    def test_with_negative_number(self):
        self.assertFalse(self.tokenizer.process('Temperature is -20 degrees'))

    def test_with_year_only(self):
        self.assertTrue(self.tokenizer.process('Copyright 2024'))

    def test_with_day_month_no_year(self):
        self.assertTrue(self.tokenizer.process('Birthday on 05/12'))

    def test_with_slash_delimited_numbers(self):
        self.assertTrue(self.tokenizer.process('Ratio 5/4'))

    def test_with_decimal_number(self):
        self.assertFalse(self.tokenizer.process('Average score was 97.5'))

    def test_with_no_delimiters(self):
        self.assertFalse(self.tokenizer.process('Version four point two'))

    def test_with_special_characters(self):
        self.assertFalse(self.tokenizer.process('Symbol: @#&'))

    def test_with_empty_string(self):
        self.assertFalse(self.tokenizer.process(''))


if __name__ == '__main__':
    unittest.main()
