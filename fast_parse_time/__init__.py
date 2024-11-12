from .core import *
from .explicit import *
from fast_parse_time.explicit.dto import DateType
from fast_parse_time.explicit.bp import ExplicitTimeExtractor
from .implicit import *


from typing import Dict, Optional


def extract_numeric_dates(input_text: str) -> Optional[Dict[str, DateType]]:
    """
    Extracts numeric dates from the given input text.

    Args:
        input_text (str): The input text from which to extract numeric dates.

    Returns:
        Optional[List[str]]: A list of extracted numeric dates, or None if no dates were found.
    """
    return ExplicitTimeExtractor().extract_numeric_dates(input_text=input_text)
