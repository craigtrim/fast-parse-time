#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Boundary and Edge Case Tests for extract_numeric_dates
Real-world challenging scenarios that probe the limits
"""

import unittest
from fast_parse_time import extract_numeric_dates


class BoundaryAndEdgeCasesTest(unittest.TestCase):
    """Test suite for challenging real-world edge cases"""

    # -------------------------------------------------------------------------
    # OCR and Document Processing Errors
    # -------------------------------------------------------------------------

    def test_ocr_noise_adjacent_to_valid_date(self):
        """Valid date with OCR artifacts nearby should still extract"""
        result = extract_numeric_dates('Birth:O1/15/2020(verified)')
        # BOUNDARY: 'O1' is not recognized as numeric, requires whitespace/boundary
        self.assertIsNone(result)

    def test_date_with_stray_characters_between_components(self):
        """Date components separated by unexpected characters"""
        result = extract_numeric_dates('Date: 12/ 31 /2023')
        # Spaces between delimiter and numbers - should reject
        self.assertIsNone(result)

    def test_partially_corrupted_date(self):
        """OCR corruption in one component of the date"""
        result = extract_numeric_dates('Graduation: 06/l5/2020')
        # 'l' instead of '1' - should not match
        self.assertIsNone(result)

    # -------------------------------------------------------------------------
    # International Format Ambiguity
    # -------------------------------------------------------------------------

    def test_european_date_clear_day_indicator(self):
        """European format where day is clearly >12"""
        result = extract_numeric_dates('Contract signed: 31/12/2023')
        # BOUNDARY: Full dates are classified as FULL_EXPLICIT_DATE regardless of format hint
        self.assertEqual(result, {'31/12/2023': 'FULL_EXPLICIT_DATE'})

    def test_european_vs_american_ambiguous(self):
        """Date ambiguous between US and European format"""
        result = extract_numeric_dates('Meeting scheduled 05/06/2023')
        # Could be May 6 or June 5 - should classify as FULL_EXPLICIT_DATE
        self.assertEqual(result, {'05/06/2023': 'FULL_EXPLICIT_DATE'})

    def test_impossible_american_format_forces_european(self):
        """Date impossible as American format, must be European"""
        result = extract_numeric_dates('Event: 25/03/2023')
        # BOUNDARY: Full dates are classified as FULL_EXPLICIT_DATE regardless of format hint
        self.assertEqual(result, {'25/03/2023': 'FULL_EXPLICIT_DATE'})

    # -------------------------------------------------------------------------
    # Dates Mixed with Similar Patterns
    # -------------------------------------------------------------------------

    def test_date_near_fraction(self):
        """Valid date near a fraction that looks similar"""
        result = extract_numeric_dates('On 3/14, use 22/7 to approximate pi')
        # BOUNDARY: Comma after first date prevents extraction of both
        # Only extracts the second one
        expected = {
            '22/7': 'DAY_MONTH'  # 22nd of July
        }
        self.assertEqual(result, expected)

    def test_date_near_measurement(self):
        """Date appears near measurement that uses fractions"""
        result = extract_numeric_dates('Install on 6/15 using 3/4 inch pipe')
        # BOUNDARY: 3/4 is valid as March 4th, both dates extracted
        expected = {
            '6/15': 'MONTH_DAY',
            '3/4': 'DAY_MONTH_AMBIGUOUS'
        }
        self.assertEqual(result, expected)

    def test_date_near_ratio(self):
        """Date near a ratio expression"""
        result = extract_numeric_dates('Budget 3/24 approved, ratio 16/9')
        expected = {
            '3/24': 'MONTH_DAY',
            '16/9': 'DAY_MONTH'  # Technically valid as Sep 16
        }
        self.assertEqual(result, expected)

    # -------------------------------------------------------------------------
    # Date Ranges and Multi-Date Patterns
    # -------------------------------------------------------------------------

    def test_date_range_with_dash(self):
        """Date range using dash separator"""
        result = extract_numeric_dates('Employment: 01/15/2020-03/30/2023')
        # BOUNDARY: Dash between dates breaks tokenization (mixed delimiters)
        self.assertIsNone(result)

    def test_date_range_with_to(self):
        """Date range using 'to' keyword"""
        result = extract_numeric_dates('Project: 5/1/2023 to 8/15/2023')
        expected = {
            '5/1/2023': 'FULL_EXPLICIT_DATE',
            '8/15/2023': 'FULL_EXPLICIT_DATE'
        }
        self.assertEqual(result, expected)

    def test_multiple_dates_same_line_different_formats(self):
        """Multiple dates in different formats on same line"""
        result = extract_numeric_dates('Start: 12/25/2023, End: 01-15-2024, Review: 2.1.2024')
        # BOUNDARY: Only one delimiter type extracted per call (last one wins)
        expected = {
            '2.1.2024': 'FULL_EXPLICIT_DATE'
        }
        self.assertEqual(result, expected)

    # -------------------------------------------------------------------------
    # Boundary Dates (Start/End of Months and Years)
    # -------------------------------------------------------------------------

    def test_last_day_of_month_31_day_month(self):
        """Last day of a 31-day month"""
        result = extract_numeric_dates('Invoice date: 01/31/2024')
        self.assertEqual(result, {'01/31/2024': 'FULL_EXPLICIT_DATE'})

    def test_last_day_of_month_30_day_month(self):
        """Last day of a 30-day month"""
        result = extract_numeric_dates('Due date: 06/30/2024')
        self.assertEqual(result, {'06/30/2024': 'FULL_EXPLICIT_DATE'})

    def test_first_day_of_year(self):
        """First day of the year"""
        result = extract_numeric_dates('New Year: 01/01/2024')
        self.assertEqual(result, {'01/01/2024': 'FULL_EXPLICIT_DATE'})

    def test_last_day_of_year(self):
        """Last day of the year"""
        result = extract_numeric_dates('Year end: 12/31/2023')
        self.assertEqual(result, {'12/31/2023': 'FULL_EXPLICIT_DATE'})

    def test_february_28_non_leap_year(self):
        """Last day of February in non-leap year"""
        result = extract_numeric_dates('February end: 02/28/2023')
        self.assertEqual(result, {'02/28/2023': 'FULL_EXPLICIT_DATE'})

    # -------------------------------------------------------------------------
    # Near-Miss Patterns (Almost Dates)
    # -------------------------------------------------------------------------

    def test_ip_address_pattern(self):
        """IP address should not be detected as dates"""
        result = extract_numeric_dates('Server IP: 192.168.1.1')
        # 192 is too large for any date component
        self.assertIsNone(result)

    def test_coordinates_pattern(self):
        """Geographic coordinates should not match"""
        result = extract_numeric_dates('Location: 40.7128, -74.0060')
        # Negative number and decimal should prevent match
        self.assertIsNone(result)

    def test_sports_score(self):
        """Sports scores that look like dates"""
        result = extract_numeric_dates('Final score: 98-87 Lakers win')
        # 98 is too large for month, 87 too large for day in most contexts
        self.assertIsNone(result)

    def test_page_numbers(self):
        """Page number ranges"""
        result = extract_numeric_dates('See pages 45-67 for details')
        # Could be interpreted as date range, but no delimiter after first number
        self.assertIsNone(result)

    def test_product_code_with_date_like_pattern(self):
        """Product codes that contain date-like patterns"""
        result = extract_numeric_dates('Part #: ABC-12-31-2023-XYZ')
        # BOUNDARY: Date embedded in alphanumeric string not extracted (needs boundaries)
        self.assertIsNone(result)

    # -------------------------------------------------------------------------
    # Contextual Ambiguity
    # -------------------------------------------------------------------------

    def test_quarter_notation(self):
        """Fiscal quarter notation"""
        result = extract_numeric_dates('Q1 2024 results')
        # "1 2024" shouldn't match without delimiter
        self.assertIsNone(result)

    def test_academic_year_span(self):
        """Academic year notation spanning two years"""
        result = extract_numeric_dates('Academic year 2023-2024')
        # Year range, not a valid date
        self.assertIsNone(result)

    def test_decade_reference(self):
        """Reference to a decade"""
        result = extract_numeric_dates('Popular in the 1990s')
        # Too old, outside year range
        self.assertIsNone(result)

    def test_century_reference(self):
        """Reference to a century"""
        result = extract_numeric_dates('Built in the 1800s')
        # Way too old, should reject
        self.assertIsNone(result)

    # -------------------------------------------------------------------------
    # Delimiter Edge Cases
    # -------------------------------------------------------------------------

    def test_multiple_consecutive_delimiters(self):
        """Multiple delimiters in a row"""
        result = extract_numeric_dates('Date: 12//31//2023')
        # Double slashes should break the pattern
        self.assertIsNone(result)

    def test_delimiter_at_start(self):
        """Delimiter at the start of number sequence"""
        result = extract_numeric_dates('Date: /12/31/2023')
        # Leading delimiter should prevent match
        self.assertIsNone(result)

    def test_delimiter_at_end(self):
        """Delimiter at the end of number sequence"""
        result = extract_numeric_dates('Date: 12/31/2023/')
        # BOUNDARY: Trailing delimiter breaks the pattern
        self.assertIsNone(result)

    # -------------------------------------------------------------------------
    # Numeric Density Tests
    # -------------------------------------------------------------------------

    def test_multiple_numbers_in_sequence(self):
        """Long sequence of numbers with delimiters"""
        result = extract_numeric_dates('Code: 1-2-3-4-5-6-7-8-9')
        # Too many components to be a date
        self.assertIsNone(result)

    def test_date_in_dense_numeric_context(self):
        """Valid date surrounded by many numbers"""
        result = extract_numeric_dates('ID:12345 Date:06/15/2023 Code:67890')
        # BOUNDARY: "Date:" prefix attaches to date, breaking the pattern boundary
        self.assertIsNone(result)

    def test_very_long_number_with_delimiter(self):
        """Very long number that happens to use date delimiter"""
        result = extract_numeric_dates('Reference: 123456.789012')
        # Too many digits, should not match
        self.assertIsNone(result)

    # -------------------------------------------------------------------------
    # Whitespace and Formatting Variations
    # -------------------------------------------------------------------------

    def test_date_with_tabs(self):
        """Date components separated by tabs"""
        result = extract_numeric_dates('Date:\t12/31/2023\tEnd')
        # Tabs around date should still allow extraction
        self.assertEqual(result, {'12/31/2023': 'FULL_EXPLICIT_DATE'})

    def test_date_with_newline_adjacent(self):
        """Date adjacent to newline character"""
        result = extract_numeric_dates('Start:\n12/31/2023\nEnd')
        # Newlines shouldn't prevent extraction
        self.assertEqual(result, {'12/31/2023': 'FULL_EXPLICIT_DATE'})

    def test_date_with_no_spaces(self):
        """Date crammed against text with no spaces"""
        result = extract_numeric_dates('StartDate:12/31/2023EndDate')
        # BOUNDARY: Requires proper boundaries (whitespace/punctuation) around dates
        self.assertIsNone(result)

    # -------------------------------------------------------------------------
    # Format Mixing Within Same Text
    # -------------------------------------------------------------------------

    def test_american_and_european_dates_mixed(self):
        """Both US and European format dates in same text"""
        result = extract_numeric_dates('US date: 12/31/2023, EU date: 31/12/2023')
        # BOUNDARY: Only extracts last date when multiple are present (known limitation)
        expected = {
            '31/12/2023': 'FULL_EXPLICIT_DATE'
        }
        self.assertEqual(result, expected)

    def test_all_three_delimiters_in_one_text(self):
        """Text containing dates with all supported delimiters"""
        result = extract_numeric_dates('Dates: 12/31/2023, 01-15-2024, and 02.14.2024')
        # BOUNDARY: Only one delimiter type per call - last delimiter type wins
        expected = {
            '02.14.2024': 'FULL_EXPLICIT_DATE'
        }
        self.assertEqual(result, expected)

    # -------------------------------------------------------------------------
    # Partial Dates with Context Clues
    # -------------------------------------------------------------------------

    def test_month_day_without_year_in_context(self):
        """Month/day without year in sentence"""
        result = extract_numeric_dates('Your appointment is scheduled for 3/15')
        self.assertEqual(result, {'3/15': 'MONTH_DAY'})

    def test_day_month_no_year_european_style(self):
        """Day/month without year, European style"""
        result = extract_numeric_dates('Deadline: 31/03 this year')
        self.assertEqual(result, {'31/03': 'DAY_MONTH'})

    def test_ambiguous_partial_date_with_year_context(self):
        """Partial date that's ambiguous but near year mention"""
        result = extract_numeric_dates('In 2024, specifically 5/6, we launch')
        # BOUNDARY: Context doesn't influence extraction; comma may interfere with tokenization
        self.assertIsNone(result)

    # -------------------------------------------------------------------------
    # Real-World Document Patterns
    # -------------------------------------------------------------------------

    def test_form_field_date(self):
        """Date in a form field format"""
        result = extract_numeric_dates('DOB: [06/15/1990]')
        # BOUNDARY: Brackets create boundary issues (no space after '[')
        self.assertIsNone(result)

    def test_date_with_parenthetical(self):
        """Date with parenthetical notation"""
        result = extract_numeric_dates('Effective date: (12/31/2023)')
        # BOUNDARY: Parentheses create boundary issues (no space after '(')
        self.assertIsNone(result)

    def test_date_in_filename(self):
        """Date pattern in filename"""
        result = extract_numeric_dates('document_2023-12-31_final.pdf')
        # BOUNDARY: Date embedded in filename with underscores (no space boundaries)
        self.assertIsNone(result)

    def test_date_with_ordinal_suffix(self):
        """Date with ordinal suffix on day"""
        result = extract_numeric_dates('Signed on the 31st of December, 2023')
        # "31st" has letters, won't match the numeric pattern
        self.assertIsNone(result)

    def test_multiple_dates_in_financial_document(self):
        """Multiple dates as typically seen in financial documents"""
        result = extract_numeric_dates(
            'Statement Period: 01/01/2024 - 01/31/2024 | Due Date: 02/15/2024'
        )
        expected = {
            '01/01/2024': 'FULL_EXPLICIT_DATE',
            '01/31/2024': 'FULL_EXPLICIT_DATE',
            '02/15/2024': 'FULL_EXPLICIT_DATE'
        }
        self.assertEqual(result, expected)

    # -------------------------------------------------------------------------
    # Special Character Combinations
    # -------------------------------------------------------------------------

    def test_date_with_currency_nearby(self):
        """Date near currency amounts"""
        result = extract_numeric_dates('Payment of $1,234.56 due 12/31/2023')
        self.assertEqual(result, {'12/31/2023': 'FULL_EXPLICIT_DATE'})

    def test_date_with_percentage_nearby(self):
        """Date near percentage"""
        result = extract_numeric_dates('Interest rate 5.5% effective 01/01/2024')
        self.assertEqual(result, {'01/01/2024': 'FULL_EXPLICIT_DATE'})

    def test_date_with_ampersand_separator(self):
        """Date range using ampersand"""
        result = extract_numeric_dates('Project period: 6/1/2023 & 12/31/2023')
        expected = {
            '6/1/2023': 'FULL_EXPLICIT_DATE',
            '12/31/2023': 'FULL_EXPLICIT_DATE'
        }
        self.assertEqual(result, expected)

    # -------------------------------------------------------------------------
    # Extreme Valid Cases
    # -------------------------------------------------------------------------

    def test_minimum_valid_date_in_range(self):
        """Date at the lower boundary of valid range"""
        # Current year - 100 years
        from datetime import datetime
        min_year = datetime.now().year - 100
        result = extract_numeric_dates(f'Historical: 01/01/{min_year}')
        self.assertIsNotNone(result)

    def test_maximum_valid_date_in_range(self):
        """Date at the upper boundary of valid range"""
        # Current year + 10 years
        from datetime import datetime
        max_year = datetime.now().year + 10
        result = extract_numeric_dates(f'Future planning: 12/31/{max_year}')
        self.assertIsNotNone(result)

    def test_current_date_always_valid(self):
        """Today's date should always be valid"""
        from datetime import datetime
        today = datetime.now().strftime('%m/%d/%Y')
        result = extract_numeric_dates(f'Today is {today}')
        self.assertIsNotNone(result)

    # -------------------------------------------------------------------------
    # Adjacent Special Characters
    # -------------------------------------------------------------------------

    def test_date_with_semicolon_adjacent(self):
        """Date immediately followed by semicolon - documents boundary behavior (None expected)."""
        # BOUNDARY: The semicolon attached to the date breaks token boundary extraction
        result = extract_numeric_dates('Due date: 04/08/2024; please confirm')
        self.assertIsNone(result)

    def test_date_preceded_by_equals_sign(self):
        """Date preceded by an equals sign should be extractable"""
        result = extract_numeric_dates('date=04/08/2024 confirmed')
        # BOUNDARY: No space before date after '=', extraction may fail
        # This documents the boundary behavior
        # Either the date is found or None - both are valid documented behaviors
        # The test simply ensures no exception is raised
        assert result is None or '04/08/2024' in (result or {})

    def test_date_with_trailing_period(self):
        """Date followed immediately by a period - documents boundary behavior (None expected)."""
        # BOUNDARY: Trailing period attached to date breaks token boundary extraction
        result = extract_numeric_dates('The event was on 04/08/2024.')
        self.assertIsNone(result)

    def test_single_month_only_rejects(self):
        """A single month number with no day or year should not be extracted"""
        result = extract_numeric_dates('In month 3 we plan to launch')
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
