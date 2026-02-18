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


if __name__ == '__main__':
    unittest.main()
