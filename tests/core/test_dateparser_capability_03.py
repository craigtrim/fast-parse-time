#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import unittest
import dateparser
from typing import Optional
from datetime import datetime


class TestDateParser(unittest.TestCase):
    '''
    Purpose:
    1.  True Positive Test Cases
    '''

    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def parse(self, input_text: str) -> Optional[str]:
        result: datetime = dateparser.parse(input_text)
        if result:
            return result.strftime('%Y-%m-%d')

    def test_10_02_2001(self):
        self.assertEqual(self.parse('10/02/2001'), '2001-10-02')

    def test_01_15_2023(self):
        """01/15/2023 should parse to 2023-01-15."""
        self.assertEqual(self.parse('01/15/2023'), '2023-01-15')

    def test_12_25_2022(self):
        """12/25/2022 should parse to 2022-12-25."""
        self.assertEqual(self.parse('12/25/2022'), '2022-12-25')

    def test_06_30_2021(self):
        """06/30/2021 should parse to 2021-06-30."""
        self.assertEqual(self.parse('06/30/2021'), '2021-06-30')

    def test_03_14_2019(self):
        """03/14/2019 should parse to 2019-03-14."""
        self.assertEqual(self.parse('03/14/2019'), '2019-03-14')

    def test_11_11_2011(self):
        """11/11/2011 should parse to 2011-11-11."""
        self.assertEqual(self.parse('11/11/2011'), '2011-11-11')

    def test_07_04_2020(self):
        """07/04/2020 should parse to 2020-07-04."""
        self.assertEqual(self.parse('07/04/2020'), '2020-07-04')

    def test_09_01_2018(self):
        """09/01/2018 should parse to 2018-09-01."""
        self.assertEqual(self.parse('09/01/2018'), '2018-09-01')

    def test_02_28_2023(self):
        """02/28/2023 should parse to 2023-02-28."""
        self.assertEqual(self.parse('02/28/2023'), '2023-02-28')

    def test_05_31_2024(self):
        """05/31/2024 should parse to 2024-05-31."""
        self.assertEqual(self.parse('05/31/2024'), '2024-05-31')


if __name__ == '__main__':
    unittest.main()
