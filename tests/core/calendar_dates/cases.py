"""Independent calendar oracles and explicit input format variations."""

from datetime import date, timedelta


MONTHS = (
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December',
)


def calendar_days(year):
    value = date(year, 1, 1)
    while value.year == year:
        yield value
        value += timedelta(days=1)


def ordinal(day):
    if day in (1, 21, 31):
        return f'{day}st'
    if day in (2, 22):
        return f'{day}nd'
    if day in (3, 23):
        return f'{day}rd'
    return f'{day}th'


def full_formats(value):
    month = MONTHS[value.month - 1]
    return [
        (value.isoformat(), 'auto'),
        (f'{value.year}/{value.month}/{value.day}', 'auto'),
        (f'{value.month}/{value.day}/{value.year}', 'mdy'),
        (f'{value.day:02}.{value.month:02}.{value.year}', 'dmy'),
        (f'{month} {value.day}, {value.year}', 'auto'),
        (f'{ordinal(value.day)} {month[:3]}. {value.year}', 'auto'),
    ]


def partial_formats(value):
    month = MONTHS[value.month - 1]
    return [
        (f'{month} {value.day}', 'auto'),
        (f'{ordinal(value.day)} of {month}', 'auto'),
        (f'{month[:3].upper()}.\t{value.day:02}', 'auto'),
        (f'{value.month}/{value.day}', 'mdy'),
    ]


WRAPPERS = ('{}', 'Term date: {}.', '[{}]', '"{}"; next item', 'before\n{}\nafter')


def dates_by_month_day(start, end):
    """Walk the actual calendar, rather than duplicating year-inference logic."""
    result = {}
    current = start
    while current <= end:
        result.setdefault((current.month, current.day), []).append(current)
        current += timedelta(days=1)
    return {key: tuple(values) for key, values in result.items()}
