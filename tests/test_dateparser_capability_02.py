#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import unittest
import dateparser
from typing import Optional
from datetime import datetime


class TestDateParser(unittest.TestCase):
    '''
    False Positive Test Cases
    '''

    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def parse(self, input_text: str) -> Optional[str]:
        result: datetime = dateparser.parse(input_text)
        if result:
            return result.strftime('%Y-%m-%d')

    def test_02_29_2024(self):
        self.assertEqual(self.parse('02/29/2024'), '2024-02-29')
        self.assertEqual(self.parse('29/02/2024'), '2024-02-29')

    def test_bad_day(self):
        self.assertIsNone(self.parse('02/32/2024'))
        self.assertIsNone(self.parse('32/02/2024'))

    def test_bad_month(self):
        self.assertEqual(self.parse('12/25/2024'), '2024-12-25')
        self.assertIsNone(self.parse('13/25/2024'))

    def test_partial_date(self):
        # dangerous ... assumes current year
        self.assertEqual(self.parse('12/25'), f'{datetime.now().year}-12-25')

        # this is a little crazy, but does show how the explicit date parser may make strange assumptions
        # we might want to protect against these edges cases ...
        # dateparser interprets '30/2' as Feb 30, 2030, which rolls to Feb 20 (always, regardless of current date)
        self.assertEqual(
            self.parse('30/2'),
            '2030-02-20')

    def test_year_only(self):
        # dangerous ... will always assume current month/day (regardless of year)

        month = datetime.now().strftime('%m')
        day = datetime.now().strftime('%d')

        # self.assertEqual(self.parse("2023"), f"2023-{month}-{day}")
        # self.assertEqual(self.parse("2024"), f"2024-{month}-{day}")

        # next_year = str(datetime.now().year + 1)
        # self.assertEqual(self.parse(next_year), f"{next_year}-{month}-{day}")


if __name__ == '__main__':
    unittest.main()
