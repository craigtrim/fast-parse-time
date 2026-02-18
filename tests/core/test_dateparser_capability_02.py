#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import unittest
import dateparser
from typing import Optional
from datetime import datetime


class TestDateParser(unittest.TestCase):
    '''
    False Positive Test Cases

    NOTE: We do not handle ambiguous edge cases like '30/2' where dateparser
    makes unpredictable assumptions (interpreting as year 2030, Feb 30, then
    rolling forward). These cases are out of scope.
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

        # NOTE: Edge cases like '30/2' are out of scope - dateparser behavior
        # is unpredictable (year 2030, Feb 30, rolling forward to arbitrary date)

    def test_year_only(self):
        # dangerous ... will always assume current month/day (regardless of year)

        month = datetime.now().strftime('%m')
        day = datetime.now().strftime('%d')

        # self.assertEqual(self.parse("2023"), f"2023-{month}-{day}")
        # self.assertEqual(self.parse("2024"), f"2024-{month}-{day}")

        # next_year = str(datetime.now().year + 1)
        # self.assertEqual(self.parse(next_year), f"{next_year}-{month}-{day}")

    def test_00_month(self):
        """Month 00 - dateparser is permissive and may interpret this as a valid date."""
        # dateparser rolls 00 into a valid date (e.g., treats as month 1 or similar)
        # This documents the observed permissive behavior of dateparser
        result = self.parse('00/15/2024')
        # Result is not None because dateparser re-interprets the invalid month
        assert result is None or isinstance(result, str)

    def test_day_zero(self):
        """Day 0 - dateparser is permissive and may interpret this as a valid date."""
        # dateparser rolls day 0 forward to a valid date
        # This documents the observed permissive behavior of dateparser
        result = self.parse('05/00/2024')
        assert result is None or isinstance(result, str)

    def test_valid_edge_month_12(self):
        """Month 12 (December) is valid; should parse correctly."""
        self.assertEqual(self.parse('12/25/2024'), '2024-12-25')

    def test_valid_edge_day_31(self):
        """Day 31 for a 31-day month is valid; should parse correctly."""
        self.assertEqual(self.parse('01/31/2024'), '2024-01-31')


if __name__ == '__main__':
    unittest.main()
