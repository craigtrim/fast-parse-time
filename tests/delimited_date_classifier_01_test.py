#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import unittest
from fast_parse_time.explicit.dmo import DelimitedDateClassifier
from fast_parse_time.explicit.dto import DateType


class DelimitedDateClassifierTest(unittest.TestCase):

    def setUp(self) -> None:
        self.classifier: DelimitedDateClassifier = DelimitedDateClassifier()

    def tearDown(self) -> None:
        self.classifier = None

    def test_full_date_01(self):

        self.assertEqual(
            self.classifier.process(input_text='02/29/2024', delimiter='/'),
            DateType.FULL_EXPLICIT_DATE)

        self.assertIsNone(
            self.classifier.process(input_text='02/29/2024', delimiter='-'))

    def test_partial_date_01(self):
        self.assertEqual(
            self.classifier.process(input_text='02/29', delimiter='/'),
            DateType.MONTH_DAY)

        self.assertEqual(
            self.classifier.process(input_text='29/2', delimiter='/'),
            DateType.DAY_MONTH)

        print('>>> ',
            self.classifier.process(input_text='30/2', delimiter='/')
        )


if __name__ == '__main__':
    unittest.main()
