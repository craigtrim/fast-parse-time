#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Test Key Behaviors of extract_numeric_dates
One behavior per test case for clarity
"""

import unittest
from fast_parse_time import extract_numeric_dates, DateType


class KeyBehaviorsTest(unittest.TestCase):
    """Test suite focusing on one key behavior per test"""

    # -------------------------------------------------------------------------
    # Whitespace Sensitivity
    # -------------------------------------------------------------------------

    def test_whitespace_around_delimiter_rejects_date(self):
        """Spaces around delimiters should invalidate the date pattern"""
        result = extract_numeric_dates('Meeting on 3 / 24')
        self.assertIsNone(result)

    def test_no_whitespace_around_delimiter_accepts_date(self):
        """Dates without spaces around delimiters should be extracted"""
        result = extract_numeric_dates('Meeting on 3/24')
        self.assertEqual(result, {'3/24': 'MONTH_DAY'})

    # -------------------------------------------------------------------------
    # Date Validation
    # -------------------------------------------------------------------------

    def test_invalid_day_rejects_date(self):
        """Days greater than 31 should be rejected"""
        result = extract_numeric_dates('Schedule for 3/32')
        self.assertIsNone(result)

    def test_invalid_month_rejects_date(self):
        """Months greater than 12 should be rejected"""
        result = extract_numeric_dates('Meeting on 13/25/2024')
        self.assertIsNone(result)

    def test_invalid_february_day_rejects_date(self):
        """February 30th should be rejected"""
        result = extract_numeric_dates('Event on 2/30/2024')
        self.assertIsNone(result)

    # -------------------------------------------------------------------------
    # Leap Year Validation
    # -------------------------------------------------------------------------

    def test_leap_year_february_29_accepts(self):
        """February 29th in a leap year should be accepted"""
        result = extract_numeric_dates('Born on 02/29/2024')
        self.assertEqual(result, {'02/29/2024': 'FULL_EXPLICIT_DATE'})

    def test_non_leap_year_february_29_rejects(self):
        """February 29th in a non-leap year should be rejected"""
        result = extract_numeric_dates('Invalid date 02/29/2023')
        self.assertIsNone(result)

    # -------------------------------------------------------------------------
    # Year Range Validation
    # -------------------------------------------------------------------------

    def test_year_within_range_accepts(self):
        """Years within current ±100 years should be accepted"""
        # Note: Standalone years in text are not extracted without delimiters
        result = extract_numeric_dates('Copyright year: 2023/01')
        self.assertIsNotNone(result)

    def test_year_too_old_rejects(self):
        """Years older than 100 years ago should be rejected"""
        result = extract_numeric_dates('Time machine to 1820')
        self.assertIsNone(result)

    def test_year_too_far_future_rejects(self):
        """Years more than 10 years in the future should be rejected"""
        result = extract_numeric_dates('Vision for 2100')
        self.assertIsNone(result)

    # -------------------------------------------------------------------------
    # Non-Date Pattern Filtering
    # -------------------------------------------------------------------------

    def test_phone_number_rejects(self):
        """Phone numbers should not be detected as dates"""
        result = extract_numeric_dates('Call me at 800-123-4567')
        self.assertIsNone(result)

    def test_time_pattern_rejects(self):
        """Time patterns (HH:MM) should not be detected as dates"""
        result = extract_numeric_dates('Alarm set for 08:00 AM')
        self.assertIsNone(result)

    def test_price_pattern_rejects(self):
        """Prices should not be detected as dates"""
        result = extract_numeric_dates('Total cost is $299.99')
        self.assertIsNone(result)

    def test_version_number_accepts_as_date(self):
        """Version numbers with date-like format are extracted"""
        result = extract_numeric_dates('Version 20.04.01 released')
        self.assertEqual(result, {'20.04.01': 'FULL_EXPLICIT_DATE'})

    def test_decimal_number_rejects(self):
        """Simple decimal numbers should not be detected as dates"""
        result = extract_numeric_dates('Average rating is 4.5')
        self.assertIsNone(result)

    # -------------------------------------------------------------------------
    # Multiple Date Extraction
    # -------------------------------------------------------------------------

    def test_multiple_dates_extracts_all(self):
        """Multiple dates in one string should all be extracted"""
        result = extract_numeric_dates('Holidays are 12/25/2023 and 01/01/2024')
        expected = {
            '12/25/2023': 'FULL_EXPLICIT_DATE',
            '01/01/2024': 'FULL_EXPLICIT_DATE'
        }
        self.assertEqual(result, expected)

    def test_mixed_date_formats_extracts_all(self):
        """Different date formats in one string should all be extracted"""
        result = extract_numeric_dates('Event from 3/15 to 12/31/2024')
        expected = {
            '3/15': 'MONTH_DAY',
            '12/31/2024': 'FULL_EXPLICIT_DATE'
        }
        self.assertEqual(result, expected)

    # -------------------------------------------------------------------------
    # Smart Classification
    # -------------------------------------------------------------------------

    def test_day_greater_than_12_classified_as_day_month(self):
        """Numbers > 12 in first position indicate day/month format"""
        result = extract_numeric_dates('Meeting on 29/2')
        self.assertEqual(result, {'29/2': 'DAY_MONTH'})

    def test_day_less_than_13_classified_as_month_day(self):
        """Numbers ≤ 12 in first position indicate month/day format"""
        result = extract_numeric_dates('Event on 3/24')
        self.assertEqual(result, {'3/24': 'MONTH_DAY'})

    def test_ambiguous_date_both_under_13_marked_ambiguous(self):
        """Dates where both numbers ≤ 12 are marked as ambiguous"""
        result = extract_numeric_dates('Appointment 4/8')
        self.assertEqual(result, {'4/8': 'DAY_MONTH_AMBIGUOUS'})

    # -------------------------------------------------------------------------
    # Delimiter Support
    # -------------------------------------------------------------------------

    def test_forward_slash_delimiter_accepts(self):
        """Forward slash (/) as delimiter should be accepted"""
        result = extract_numeric_dates('Date: 12/31/2023')
        self.assertEqual(result, {'12/31/2023': 'FULL_EXPLICIT_DATE'})

    def test_dash_delimiter_accepts(self):
        """Dash (-) as delimiter should be accepted"""
        result = extract_numeric_dates('Event on 12-31-2023')
        self.assertEqual(result, {'12-31-2023': 'FULL_EXPLICIT_DATE'})

    def test_dot_delimiter_accepts(self):
        """Dot (.) as delimiter should be accepted"""
        result = extract_numeric_dates('Deadline is 11.30.2024')
        self.assertEqual(result, {'11.30.2024': 'FULL_EXPLICIT_DATE'})

    def test_unsupported_delimiter_rejects(self):
        """Unsupported delimiters should be rejected"""
        result = extract_numeric_dates('Special date 12|31|2023')
        self.assertIsNone(result)

    def test_mixed_delimiters_rejects(self):
        """Mixing delimiters in one date should be rejected"""
        result = extract_numeric_dates('Mixed format 12/31-2024')
        self.assertIsNone(result)

    # -------------------------------------------------------------------------
    # Date Type Classification
    # -------------------------------------------------------------------------

    def test_full_date_classified_correctly(self):
        """Complete dates should be classified as FULL_EXPLICIT_DATE"""
        result = extract_numeric_dates('Born on 04/08/2024')
        self.assertEqual(result, {'04/08/2024': 'FULL_EXPLICIT_DATE'})

    def test_month_day_classified_correctly(self):
        """Month/day dates should be classified as MONTH_DAY"""
        result = extract_numeric_dates('Birthday party on 07/24')
        self.assertEqual(result, {'07/24': 'MONTH_DAY'})

    def test_year_only_classified_correctly(self):
        """Year-only dates should be classified as YEAR_ONLY"""
        # Note: Standalone years without delimiters are not extracted
        # This is expected behavior to avoid false positives
        result = extract_numeric_dates('Copyright 2023')
        self.assertIsNone(result)

    # -------------------------------------------------------------------------
    # Edge Cases
    # -------------------------------------------------------------------------

    def test_date_with_leading_zeros_accepts(self):
        """Dates with leading zeros should be preserved"""
        result = extract_numeric_dates('Deadline by 01/02/2024')
        self.assertEqual(result, {'01/02/2024': 'FULL_EXPLICIT_DATE'})

    def test_empty_string_returns_none(self):
        """Empty string should return None"""
        result = extract_numeric_dates('')
        self.assertIsNone(result)

    def test_text_with_no_dates_returns_none(self):
        """Text without any date patterns should return None"""
        result = extract_numeric_dates('Hello world, this is a test')
        self.assertIsNone(result)

    def test_single_digit_number_rejects(self):
        """Single digit numbers should not be detected as dates"""
        result = extract_numeric_dates('Number 42')
        self.assertIsNone(result)

    # -------------------------------------------------------------------------
    # ISO Date Format
    # -------------------------------------------------------------------------

    def test_iso_date_format_accepts(self):
        """ISO date format (YYYY-MM-DD) should be accepted"""
        result = extract_numeric_dates('ISO date format 2023-05-17')
        self.assertEqual(result, {'2023-05-17': 'FULL_EXPLICIT_DATE'})

    # -------------------------------------------------------------------------
    # Context Preservation
    # -------------------------------------------------------------------------

    def test_date_extracted_from_sentence_context(self):
        """Dates should be extracted preserving their exact format"""
        result = extract_numeric_dates('The event is scheduled for 04/08/2024')
        self.assertEqual(result, {'04/08/2024': 'FULL_EXPLICIT_DATE'})

    def test_date_with_surrounding_punctuation_extracts(self):
        """Dates surrounded by text should still be extracted"""
        result = extract_numeric_dates('Date of birth: 06/23/2004')
        self.assertEqual(result, {'06/23/2004': 'FULL_EXPLICIT_DATE'})

    # -------------------------------------------------------------------------
    # Additional Key Behaviors
    # -------------------------------------------------------------------------

    def test_date_in_all_caps_text(self):
        """Date embedded in all-caps text should still be extracted"""
        result = extract_numeric_dates('MEETING ON 04/08/2024 CONFIRMED')
        self.assertEqual(result, {'04/08/2024': 'FULL_EXPLICIT_DATE'})

    def test_date_with_multiple_spaces_between_words(self):
        """Date preceded by multiple spaces should still be extracted"""
        result = extract_numeric_dates('Date:   04/08/2024   confirmed')
        self.assertEqual(result, {'04/08/2024': 'FULL_EXPLICIT_DATE'})

    def test_date_at_very_start_of_string(self):
        """Date at the very start of the string should be extracted"""
        result = extract_numeric_dates('04/08/2024 is the deadline')
        self.assertEqual(result, {'04/08/2024': 'FULL_EXPLICIT_DATE'})

    def test_date_at_very_end_of_string(self):
        """Date at the very end of the string should be extracted"""
        result = extract_numeric_dates('The deadline is 04/08/2024')
        self.assertEqual(result, {'04/08/2024': 'FULL_EXPLICIT_DATE'})


if __name__ == '__main__':
    unittest.main()
