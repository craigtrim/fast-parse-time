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


if __name__ == '__main__':
    unittest.main()
