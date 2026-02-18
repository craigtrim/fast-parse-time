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

        self.assertEqual(self.classifier.process(
            input_text='30/2', delimiter='/'), DateType.DAY_MONTH)

    def test_full_date_dash_delimiter(self):
        """A full date using dash delimiter should classify as FULL_EXPLICIT_DATE."""
        self.assertEqual(
            self.classifier.process(input_text='12-31-2023', delimiter='-'),
            DateType.FULL_EXPLICIT_DATE)

    def test_full_date_dot_delimiter(self):
        """A full date using dot delimiter should classify as FULL_EXPLICIT_DATE."""
        self.assertEqual(
            self.classifier.process(input_text='11.30.2024', delimiter='.'),
            DateType.FULL_EXPLICIT_DATE)

    def test_wrong_delimiter_returns_none(self):
        """Providing a delimiter that does not match the date string should return None."""
        self.assertIsNone(
            self.classifier.process(input_text='12-31-2023', delimiter='/'))

    def test_dot_delimiter_wrong_returns_none(self):
        """Using slash delimiter on a dot-delimited date should return None."""
        self.assertIsNone(
            self.classifier.process(input_text='11.30.2024', delimiter='/'))

    def test_day_month_partial_dash(self):
        """A partial day/month using dash delimiter should classify as DAY_MONTH."""
        self.assertEqual(
            self.classifier.process(input_text='31-12', delimiter='-'),
            DateType.DAY_MONTH)

    def test_day_month_partial_dot(self):
        """A partial day/month using dot delimiter should classify as DAY_MONTH."""
        self.assertEqual(
            self.classifier.process(input_text='31.12', delimiter='.'),
            DateType.DAY_MONTH)

    def test_month_day_partial_dash(self):
        """A partial month/day using dash delimiter should classify as MONTH_DAY."""
        self.assertEqual(
            self.classifier.process(input_text='02-28', delimiter='-'),
            DateType.MONTH_DAY)

    def test_full_date_slash_additional(self):
        """Another full date with slash delimiter should classify as FULL_EXPLICIT_DATE."""
        self.assertEqual(
            self.classifier.process(input_text='06/15/2020', delimiter='/'),
            DateType.FULL_EXPLICIT_DATE)

    def test_full_date_slash_wrong_dash_delimiter(self):
        """Slash date with dash delimiter should return None."""
        self.assertIsNone(
            self.classifier.process(input_text='06/15/2020', delimiter='-'))


if __name__ == '__main__':
    unittest.main()
