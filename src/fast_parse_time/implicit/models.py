"""Small internal relative-time value types."""

from typing import NamedTuple


class Slot(NamedTuple):
    """Structured representation of a resolved time slot."""
    cardinality: int | str  # str for informal cardinalities e.g. '2+'
    frame: str
    tense: str
