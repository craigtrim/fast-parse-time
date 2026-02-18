#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import unittest
import dateparser


class TestDateParser(unittest.TestCase):
    '''
    True Positive Test Cases
    '''

    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_add(self):
        self.assertIsNone(dateparser.parse('Education Date: 06/05/2016'))
        self.assertEqual(dateparser.parse(
            '06/05/2016').strftime('%Y-%m-%d'), '2016-06-05')

        # try formatting issues
        self.assertEqual(dateparser.parse(
            '     06/05/2016').strftime('%Y-%m-%d'), '2016-06-05')
        self.assertEqual(dateparser.parse(
            '     06/05/2016       ').strftime('%Y-%m-%d'), '2016-06-05')

        # alternate delims
        self.assertEqual(dateparser.parse(
            '06 / 05 / 2016').strftime('%Y-%m-%d'), '2016-06-05')
        self.assertEqual(dateparser.parse(
            '06-05-2016').strftime('%Y-%m-%d'), '2016-06-05')
        self.assertEqual(dateparser.parse(
            '06.05.2016').strftime('%Y-%m-%d'), '2016-06-05')
        self.assertEqual(dateparser.parse(
            '06.05.16').strftime('%Y-%m-%d'), '2016-06-05')

    def test_dash_delimiter_various_years(self):
        """Dash-delimited dates for several years should parse correctly."""
        self.assertEqual(dateparser.parse(
            '01-15-2023').strftime('%Y-%m-%d'), '2023-01-15')
        self.assertEqual(dateparser.parse(
            '12-25-2022').strftime('%Y-%m-%d'), '2022-12-25')
        self.assertEqual(dateparser.parse(
            '07-04-2020').strftime('%Y-%m-%d'), '2020-07-04')

    def test_dot_delimiter_various_years(self):
        """Dot-delimited dates for several years should parse correctly."""
        self.assertEqual(dateparser.parse(
            '03.14.2019').strftime('%Y-%m-%d'), '2019-03-14')
        self.assertEqual(dateparser.parse(
            '11.30.2024').strftime('%Y-%m-%d'), '2024-11-30')

    def test_dates_with_leading_zeros(self):
        """Dates with leading zeros should parse correctly."""
        self.assertEqual(dateparser.parse(
            '01/02/2024').strftime('%Y-%m-%d'), '2024-01-02')
        self.assertEqual(dateparser.parse(
            '09/01/2021').strftime('%Y-%m-%d'), '2021-09-01')
        self.assertEqual(dateparser.parse(
            '02/08/2018').strftime('%Y-%m-%d'), '2018-02-08')


if __name__ == '__main__':
    unittest.main()
