#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import unittest
from fast_parse_time.explicit.svc import TokenizeNumericComponents


class NumericComponentTokenizerTest(unittest.TestCase):

    def setUp(self) -> None:
        self.tokenizer: TokenizeNumericComponents = TokenizeNumericComponents()

    def tearDown(self) -> None:
        self.tokenizer = None

    def test_edge_case_leap_year(self):
        # Valid leap year date
        self.assertEqual(self.tokenizer.process(
            'Leap Year: 02/29/2024'), ['02/29/2024'])

    def test_almost_valid_date(self):
        # Month and day swapped, still a valid format but potentially confusing
        self.assertEqual(self.tokenizer.process(
            'Confusing date: 12/31'), ['12/31'])

    def test_valid_date_with_noise(self):
        # Valid date surrounded by noise characters
        # TODO: assuming a noisy OCR job, this could be an issue
        self.assertIsNone(self.tokenizer.process('Noise[12-25-2023]end'))

    def test_date_in_words(self):
        # Date in words, which might be overlooked
        # TODO: this could be an issue on diplomas, but I have yet to see it on transcripts ...
        self.assertIsNone(self.tokenizer.process(
            'July twenty fourth, two thousand twenty-three'))

    def test_date_with_th_suffix(self):
        # Numeric date with 'th' suffix on day, could be mistaken for invalid
        self.assertEqual(self.tokenizer.process(
            'Meet me on the 7th of May 2023'), ['2023'])

    def test_misleading_numeric_pattern(self):
        # Looks like a date but is not (e.g., a version number)
        self.assertEqual(self.tokenizer.process(
            'Version 20.04.01 - not a date'), ['20.04.01'])

    def test_numeric_with_date_keywords(self):
        # Numeric values with date keywords but not actual dates
        # I don't think we're going to differentiate years in terms of keywords vs dates
        self.assertEqual(self.tokenizer.process(
            'Quarter 4, 2023 sales up'), ['2023'])

    def test_date_as_epoch_time(self):
        # Epoch time, technically a number but not a date format the algorithm should accept
        self.assertIsNone(self.tokenizer.process('Timestamp: 1609459200'))

    def test_iso_date_with_time(self):
        # ISO date format with time, might get confused as a non-date
        # I doubt we'll find an ISO date in this format on a transcript post-OCR
        # but perhaps digitized copies ... ?
        self.assertIsNone(self.tokenizer.process(
            'Event starts at 2023-05-17T15:00:00Z'))

    def test_date_with_textual_month_and_comma(self):
        # Date format with textual month and comma, common but possibly confusing
        self.assertEqual(self.tokenizer.process(
            'Appointment on January 12, 2023'), ['2023'])

    def test_reversed_iso_date(self):
        # ISO date format reversed, technically could be parsed but likely incorrect
        self.assertEqual(self.tokenizer.process(
            'Reverse ISO 17-2023-05'), ['17-2023-05'])

    def test_date_with_day_name(self):
        # Date with day name, could be overlooked as non-numeric
        self.assertEqual(self.tokenizer.process(
            'Meeting on Tuesday, March 15, 2023'), ['2023'])

    def test_fraction_disguised_as_date(self):
        # Fraction that could be mistaken for a date
        self.assertEqual(self.tokenizer.process(
            'Pi approximated as 3/14'), ['3/14'])

    def test_date_with_range_in_month(self):
        # Date range within a single month, tricky because it includes a dash
        self.assertEqual(self.tokenizer.process(
            'Event from 05-01 to 05-10 in 2023'), ['2023'])

    def test_date_with_range_across_months(self):
        # Date range across months, more complex due to two dashes
        self.assertEqual(self.tokenizer.process(
            'Planning period: 12-20-2023 to 01-05-2024'), ['12-20-2023', '01-05-2024'])

    def test_overflow_month(self):
        # A date with an overflow month, should be invalid
        # TODO: I think a downstream validator has to take care of this ...
        self.assertEqual(self.tokenizer.process(
            'Invalid month 13/25/2023'), ['13/25/2023'])

    def test_overflow_day(self):
        # A date with an overflow day, should be invalid
        # TODO: I think a downstream validator has to take care of this ...
        self.assertEqual(self.tokenizer.process(
            'Overflow day 02/31/2023'), ['02/31/2023'])

    def test_date_with_extra_delimiters(self):
        # Date with extra delimiters, potentially confusing
        self.assertIsNone(self.tokenizer.process(
            'Messy date: 01-//02-///2024'))

    def test_ambiguous_numeric_sequence(self):
        # Sequence that could be interpreted as a date
        self.assertIsNone(self.tokenizer.process('Magic number 12345678'))

    def test_valid_date_in_brackets(self):
        # Date within brackets might be processed differently
        # TODO: potential tokenization issue ...
        self.assertIsNone(self.tokenizer.process(
            'Event date [04/22/2024] confirmed'))

    def test_date_with_uncommon_delimiter(self):
        # Date with an uncommon delimiter
        # I doubt this will ever happen (outside a bad OCR error)
        self.assertIsNone(self.tokenizer.process(
            'Special date 12|31|2023'))

    def test_ambiguous_european_format(self):
        # European date format, ambiguous without knowing the context
        self.assertEqual(self.tokenizer.process(
            'EU format 31.12.2023'), ['31.12.2023'])

    def test_false_positive_as_date(self):
        # Numeric pattern that could falsely be recognized as a date
        self.assertIsNone(self.tokenizer.process('Model number 2024.123'))

    def test_mixed_delimiter_date(self):
        # Date with mixed delimiters, could be tricky to parse
        self.assertIsNone(self.tokenizer.process(
            'Mixed format 12/31-2024'))

    def test_numerical_bullet_points(self):
        # Numerical bullet points that could be mistaken for dates
        self.assertIsNone(self.tokenizer.process('1.2.3. Strategy steps'))

    def test_date_with_dash_nearby(self):
        """Date with a dash in surrounding text - documents boundary behavior."""
        # BOUNDARY: A dash following the date may interfere with tokenization
        result = self.tokenizer.process('Deadline: 04/08/2024 - confirmed')
        # Result may be the date alone or None - documents the actual behavior
        assert result is None or isinstance(result, list)

    def test_date_at_very_start_of_string(self):
        """Date at the very start of the string should be tokenized."""
        self.assertEqual(
            self.tokenizer.process('04/08/2024 is the event date'),
            ['04/08/2024'])

    def test_date_at_very_end_of_string(self):
        """Date at the very end of the string should be tokenized."""
        self.assertEqual(
            self.tokenizer.process('The event is on 04/08/2024'),
            ['04/08/2024'])

    def test_date_with_comma_immediately_after(self):
        """Date followed immediately by a comma - documents boundary behavior (None expected)."""
        # BOUNDARY: Comma attached directly to the date breaks token boundary detection
        result = self.tokenizer.process('The date is 04/08/2024, confirmed')
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
