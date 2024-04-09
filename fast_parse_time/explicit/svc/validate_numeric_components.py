#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Validate Date/Time Extracted Components """


from typing import List, Dict, Optional, Tuple
from baseblock import BaseObject, Enforcer
from fast_parse_time.explicit.dmo import DayMonthValidator
from fast_parse_time.explicit.dto import DateType, date_delims, MIN_YEAR, MAX_YEAR


class ValidateNumericComponents(BaseObject):
    """ Validate Date/Time Extracted Components """

    __day_month_validator: DayMonthValidator = None

    def __init__(self):
        """ Change Log

        Created:
            8-Apr-2024
            craigtrim@gmail.com
        """
        BaseObject.__init__(self, __name__)

    def _tokenize(self, explicit_date: str) -> Optional[List[str]]:
        _date_delims = [
            date_delim for date_delim in date_delims
            if date_delim in explicit_date
        ]

        if not len(_date_delims):
            return None

        delim: str = _date_delims[0]
        return explicit_date.split(delim)

    # def _is_valid_month_day(self, explicit_date: str) -> bool:
    #     """
    #     Check if the given explicit date is a valid month and day combination.

    #     Args:
    #         explicit_date (str): The explicit date string to validate.
    #         date_type (DateType): The type of date being validated.

    #     Returns:
    #         bool: True if the explicit date is a valid month and day combination, False otherwise.
    #     """

    #     date_tokens: Optional[List[str]] = self._tokenize(explicit_date)
    #     if not date_tokens or not len(date_tokens):
    #         return False

    #     month = date_tokens[0]
    #     day_of_month = date_tokens[1]

    #     if month == 1:
    #         return 1 <= day_of_month <= 31
    #     elif month == 2:
    #         return 1 <= day_of_month <= 29
    #     elif month == 3:
    #         return 1 <= day_of_month <= 31
    #     elif month == 4:
    #         return 1 <= day_of_month <= 30
    #     elif month == 5:
    #         return 1 <= day_of_month <= 31
    #     elif month == 6:
    #         return 1 <= day_of_month <= 30
    #     elif month == 7:
    #         return 1 <= day_of_month <= 31
    #     elif month == 8:
    #         return 1 <= day_of_month <= 31
    #     elif month == 9:
    #         return 1 <= day_of_month <= 30
    #     elif month == 10:
    #         return 1 <= day_of_month <= 31
    #     elif month == 11:
    #         return 1 <= day_of_month <= 30
    #     elif month == 12:
    #         return 1 <= day_of_month <= 31

    #     return False

    def _is_valid_day_month(self, explicit_date: str, date_type: DateType) -> bool:
        if not self.__day_month_validator:
            self.__day_month_validator = DayMonthValidator()

        date_tokens: List[str] = self._tokenize(explicit_date)

        def get_day_month() -> Tuple[str, str]:
            if date_type == DateType.DAY_MONTH:
                return date_tokens[1], date_tokens[0]
            elif date_type == DateType.MONTH_DAY:
                return date_tokens[0], date_tokens[1]

        month, day_of_month = get_day_month()

        print(month, day_of_month)

        return self.__day_month_validator.process(
            month=month, day_of_month=day_of_month)

    def process(self,

                d_date_types: Dict[str, DateType]) -> Optional[Dict[str, DateType]]:

        d_validated: Dict[str, DateType] = {}

        for explicit_date in d_date_types:
            date_type: DateType = DateType.find(d_date_types[explicit_date])

            if date_type in [DateType.DAY_MONTH, DateType.MONTH_DAY] and not self._is_valid_day_month(
                    explicit_date=explicit_date, date_type=date_type):
                continue

            d_validated[explicit_date] = date_type.name

        return d_validated
