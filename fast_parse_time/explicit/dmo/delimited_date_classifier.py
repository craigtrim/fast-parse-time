#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Classify Delimited Numerical Dates """


import dateparser
from datetime import datetime
from fast_parse_time.explicit.dto import DateType, DateComponentType,  MIN_YEAR, MAX_YEAR


class DelimitedDateClassifier(object):
    """ Classify Delimited Numerical Dates """

    def __init__(self):
        """ Change Log

        Created:
            8-Apr-2024
            craigtrim@gmail.com
        """
        pass

    def _parse_datetime(self, input_text: str) -> str | None:
        result: datetime = dateparser.parse(input_text)
        if result:
            return result.strftime('%Y-%m-%d')

    def _classify_token(self,
                        input_text: str) -> DateComponentType | None:
        try:
            n = int(input_text)
        except ValueError:
            return None

        # e.g., a range of viable years (given 2024, range is 1924 - 2034)
        if MIN_YEAR <= n <= MAX_YEAR:
            return DateComponentType.YEAR

        if 13 <= n <= 31:
            return DateComponentType.DAY

        if 1 <= n <= 12:
            return DateComponentType.DAY_OR_MONTH

    def _normalize_date_components(self, date_component_types: list[DateComponentType]):
        """
        Normalize the date components based on the given list of date component types.

        This method assumes the incoming date-component-types are valid
        and resolved ambiguity based on hints

        Sample Input:
            30/4

        Sample Date Component Type Classification:
            DateComponentType.DAY
            DateComponentType.DAY_OR_MONTH

        Sample Output:
            DateComponentType.DAY
            DateComponentType.MONTH

        Rationale:
            Assumes input is valid
            If the first component is a day, the second component must be a month

        Args:
            date_component_types (List[DateComponentType]): A list of DateComponentType objects representing the date components.

        Returns:
            List[DateComponentType]: The normalized list of date component types.

        """
        incoming_names = [
            date_component_type.name
            for date_component_type in date_component_types
        ]

        if incoming_names == ['DAY', 'DAY_OR_MONTH']:
            return [
                DateComponentType.DAY,
                DateComponentType.MONTH,
            ]

        elif incoming_names == ['DAY_OR_MONTH', 'DAY_OR_MONTH']:
            return [
                DateComponentType.DAY_OR_MONTH,
                DateComponentType.DAY_OR_MONTH,
            ]

        elif incoming_names == ['DAY_OR_MONTH', 'DAY']:
            return [
                DateComponentType.MONTH,
                DateComponentType.DAY,
            ]

        elif incoming_names == ['DAY_OR_MONTH', 'MONTH']:
            return [
                DateComponentType.DAY,
                DateComponentType.MONTH,
            ]

        elif incoming_names == ['MONTH', 'DAY_OR_MONTH']:
            return [
                DateComponentType.MONTH,
                DateComponentType.DAY,
            ]

        elif incoming_names == ['YEAR', 'DAY_OR_MONTH']:
            return [
                DateComponentType.YEAR,
                DateComponentType.MONTH,
            ]

        elif incoming_names == ['DAY_OR_MONTH', 'YEAR']:
            return [
                DateComponentType.MONTH,
                DateComponentType.YEAR,
            ]

        if 'DAY_OR_MONTH' in incoming_names:
            raise ValueError(f'Unresolved Ambiguity: {incoming_names}')

        return date_component_types

    def _process(self,
                 input_text: str,
                 delimiter: str) -> DateType | None:

        total_delimiters = input_text.count(delimiter)
        if total_delimiters == 0 or total_delimiters >= 3:
            return None

        if not self._parse_datetime(input_text):
            return None

        if total_delimiters == 2:
            return DateType.FULL_EXPLICIT_DATE

        input_tokens: list[str] = input_text.split(delimiter)
        if not input_tokens or not len(input_tokens):
            return None

        date_component_types: list[DateComponentType] | None = [
            self._classify_token(token)
            for token in input_tokens
        ]

        if not date_component_types or not len(date_component_types):
            return None

        date_component_types: list[DateComponentType] = [
            token for token in date_component_types if token
        ]

        if not date_component_types or not len(date_component_types):
            return None

        date_component_types: list[DateComponentType] = self._normalize_date_components(
            date_component_types)

        # Year/Month
        if date_component_types in [
            [DateComponentType.YEAR, DateComponentType.MONTH],
        ]:
            return DateType.YEAR_MONTH
        elif date_component_types in [
            [DateComponentType.MONTH, DateComponentType.YEAR],
        ]:
            return DateType.MONTH_YEAR

        # Day/Month
        elif date_component_types in [
            [DateComponentType.DAY, DateComponentType.MONTH],
        ]:
            return DateType.DAY_MONTH
        elif date_component_types in [
            [DateComponentType.MONTH, DateComponentType.DAY],
        ]:
            return DateType.MONTH_DAY
        elif date_component_types in [
            [DateComponentType.DAY_OR_MONTH, DateComponentType.DAY_OR_MONTH],
        ]:
            return DateType.DAY_MONTH_AMBIGUOUS

        # Year Only
        elif date_component_types in [
            [DateComponentType.YEAR]
        ]:
            return DateType.YEAR_ONLY

        if self.isEnabledForInfo:
            date_component_type_str = [
                date_component_type.name for date_component_type in date_component_types
            ]
            self.logger.info(
                f'Unrecognized Date Component Classification: {date_component_type_str}')

    def process(self,
                input_text: str,
                delimiter: str) -> DateType | None:

        result: DateType | None = self._process(
            input_text=input_text, delimiter=delimiter)

        if result and not isinstance(result, DateType):
            raise TypeError(
                f'Input Text: {input_text} has wrong type: {type(input_text)}')

        return result
