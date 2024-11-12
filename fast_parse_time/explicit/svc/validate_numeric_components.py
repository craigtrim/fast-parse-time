#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Validate Date/Time Extracted Components """


from fast_parse_time.explicit.dmo import DayMonthValidator
from fast_parse_time.explicit.dto import DateType, date_delims, MIN_YEAR, MAX_YEAR


class ValidateNumericComponents(object):
    """ Validate Date/Time Extracted Components """

    __day_month_validator: DayMonthValidator = None

    def __init__(self):
        """ Change Log

        Created:
            8-Apr-2024
            craigtrim@gmail.com
        """
        pass

    def _tokenize(self, explicit_date: str) -> list[str] | None:
        _date_delims = [
            date_delim for date_delim in date_delims
            if date_delim in explicit_date
        ]

        if not len(_date_delims):
            return None

        delim: str = _date_delims[0]
        return explicit_date.split(delim)

    def _is_valid_day_month(self, explicit_date: str, date_type: DateType) -> bool:
        if not self.__day_month_validator:
            self.__day_month_validator = DayMonthValidator()

        date_tokens: list[str] = self._tokenize(explicit_date)

        def get_day_month() -> tuple[str, str]:
            if date_type == DateType.DAY_MONTH:
                return date_tokens[1], date_tokens[0]
            elif date_type == DateType.MONTH_DAY:
                return date_tokens[0], date_tokens[1]

        month, day_of_month = get_day_month()

        return self.__day_month_validator.process(
            month=month, day_of_month=day_of_month)

    def process(self,

                d_date_types: dict[str, DateType]) -> dict[str, DateType] | None:

        d_validated: dict[str, DateType] = {}

        for explicit_date in d_date_types:
            date_type: DateType = DateType.find(d_date_types[explicit_date])

            if date_type in [DateType.DAY_MONTH, DateType.MONTH_DAY] and not self._is_valid_day_month(
                    explicit_date=explicit_date, date_type=date_type):
                continue

            d_validated[explicit_date] = date_type.name

        return d_validated
