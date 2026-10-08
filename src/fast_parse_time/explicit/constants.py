"""Vocabulary and legacy date-classification bounds."""

from datetime import datetime

date_delims = [
    '/', '.', '-'
]

MAX_YEAR = datetime.now().year + 10
MIN_YEAR = datetime.now().year - 100

# Month names for written date format detection
MONTH_NAMES_FULL = {
    'january', 'february', 'march', 'april', 'may', 'june',
    'july', 'august', 'september', 'october', 'november', 'december'
}
MONTH_NAMES_ABBREV = {
    'jan', 'feb', 'mar', 'apr', 'may', 'jun',
    'jul', 'aug', 'sep', 'sept', 'oct', 'nov', 'dec'
}
MONTH_NAMES = MONTH_NAMES_FULL | MONTH_NAMES_ABBREV
