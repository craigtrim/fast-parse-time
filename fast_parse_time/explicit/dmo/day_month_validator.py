#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Validate DAY_MONTH Patterns """


from typing import List


class DayMonthValidator(object):
    """ Validate DAY_MONTH Patterns """

    def __init__(self):
        """ Change Log

        Created:
            8-Apr-2024
            craigtrim@gmail.com
        """
        pass

    def process(self, month: int, day_of_month: int) -> bool:
        """
        Validates the given month and day_of_month values.

        Args:
            month (int): The month value to be validated.
            day_of_month (int): The day of the month value to be validated.

        Returns:
            bool: True if the month and day_of_month values are valid, False otherwise.
        """

        if isinstance(month, str):
            month = int(month)

        if isinstance(day_of_month, str):
            day_of_month = int(day_of_month)

        if month == 1:
            return 1 <= day_of_month <= 31
        elif month == 2:
            return 1 <= day_of_month <= 29
        elif month == 3:
            return 1 <= day_of_month <= 31
        elif month == 4:
            return 1 <= day_of_month <= 30
        elif month == 5:
            return 1 <= day_of_month <= 31
        elif month == 6:
            return 1 <= day_of_month <= 30
        elif month == 7:
            return 1 <= day_of_month <= 31
        elif month == 8:
            return 1 <= day_of_month <= 31
        elif month == 9:
            return 1 <= day_of_month <= 30
        elif month == 10:
            return 1 <= day_of_month <= 31
        elif month == 11:
            return 1 <= day_of_month <= 30
        elif month == 12:
            return 1 <= day_of_month <= 31

        return False
