#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from enum import Enum, auto
from datetime import datetime
from typing import Optional

date_delims = [
    '/', '.', '-'
]

MAX_YEAR = datetime.now().year + 10
MIN_YEAR = datetime.now().year - 100


class DateComponentType(Enum):
    YEAR = auto()  # e.g., now-100 < now < now+5
    MONTH = auto()  # e.g., 1-12 (with context)
    DAY = auto()  # e.g., 1-31 (with context)
    DAY_OR_MONTH = auto()  # e.g., 1-31 (without context)


class DateType(Enum):

    # Full Explicit Date:
    FULL_EXPLICIT_DATE = auto()  # e.g., 03/19/2023, March 19, 2023

    # Partial Explicit Dates:
    YEAR_ONLY = auto()  # e.g., 2024
    DAY_MONTH = auto()  # e.g., March 15th
    MONTH_DAY = auto()  # e.g., 15th of March
    DAY_MONTH_AMBIGUOUS = auto()  # e.g., 4/8
    MONTH_YEAR = auto()  # e.g., March 2023
    YEAR_MONTH = auto()  # e.g., 2023-MARCH

    YEAR_RANGE = auto()  # e.g., 2014-2015
    SEASON_YEAR = auto()  # e.g., Summer 2013
    TIMEFRAME_RELATIVE_TO_NOW = auto()  # e.g., 5 days ago, next week
    NON_SPECIFIC_FUTURE_PAST = auto()  # e.g., in the future, a long time ago
    EVENT_BASED_RELATIVE_DATE = auto()  # e.g., the day after New Year's
    SEASONAL_OR_QUARTERLY = auto()  # e.g., this winter, Q1
    RECURRENT_DATE = auto()  # e.g., every Monday, annually on July 4th
    FUZZY_DATE = auto()  # e.g., late March, early 2020s
    NO_DATE = auto()  # Text chunks with no date information

    def find(input_text: str) -> Optional['DateType']:

        if not isinstance(input_text, str):
            return None

        input_text = input_text.upper().strip()
        for date_type in DateType:
            if date_type.name == input_text:
                return date_type
