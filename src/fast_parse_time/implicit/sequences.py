"""Extract, filter, and match relative-time keyword sequences."""

from fast_parse_time.implicit.knowledge_base import (
    d_keyterm_counter_kb, d_index_by_slot_kb, d_index_by_keyterm_kb,
)


class KeywordSequenceExtractor(object):
    """ Extract Keyword Sequences

    This is an extraction and correlation of contiguous time sequences within text

    Example 1:
        Sample Input Text:              "from Joe Smith 5 days ago"
        Sample Keyword Sequence:        [ ['from'], ['5', 'days', 'ago'] ]

    Example 2:
        Sample Input Text:              "from Joe Smith 4 years and 3 months ago"
        Sample Keyword Sequence:        [ ['from'], ['4', 'years'], ['3', 'months', 'ago'] ],
    """

    def __init__(self):
        """ Change Log

        Created:
            10-Aug-2022
            craigtrim@gmail.com
        """
        self._keyterms = set(d_keyterm_counter_kb.keys())

    def process(self,
                tokens: list) -> list:
        """ Extract Keyword Sequences

        Args:
            tokens (list): an incoming list of tokens from the user input text

        Returns:
            list: a list of lists
        """

        master = []

        buffer = []
        for token in tokens:
            if token in self._keyterms:
                buffer.append(token)
            else:
                if len(buffer):
                    master.append(buffer)
                    buffer = []
        if len(buffer):
            master.append(buffer)

        return master


class KeywordSequenceFilter(object):
    """ Filter Sequences for Invalid Keys

    Sample Input Text:
        from here show me all 5 items all the history from 5 days ago

    Sample Sequences:
        [
            ['from'],
            ['5'],
            ['from', '5', 'days', 'ago']
        ]
        -   the first two sequences don't exist in 'd_index_by_slot_kb'
            and can be discarded immediately
        -   the second sequence can be sliced and diced into candidates:
                [
                    ['from', '5', 'days'],
                    ['5', 'days', 'ago']
                ]
            and each candidate checked against 'd_index_by_slot_kb' for validity
    """

    def __init__(self):
        """ Change Log

        Created:
            10-Aug-2022
            craigtrim@gmail.com
        """
        pass

    def process(self,
                sequences: list) -> list:
        """ Filter Sequences for Invalid Keys

        Args:
            sequences (list): the incoming sequences

        Returns:
            list: the filtered sequences
        """
        normalized = []

        for sequence in sequences:
            slot = ' '.join(sequence).strip()
            exists = slot in d_index_by_slot_kb

            if exists:
                normalized.append(sequence)
            elif not exists and len(sequence) == 1:
                continue
            elif ' '.join(sequence[1:]) in d_index_by_slot_kb:
                normalized.append(sequence[1:])
            elif ' '.join(sequence[:-1]) in d_index_by_slot_kb:
                normalized.append(sequence[:-1])

        return normalized


class SequenceSolutionFinder(object):
    """ Find Solutions for Sequences """

    def __init__(self):
        """ Change Log

        Created:
            10-Aug-2022
            craigtrim@gmail.com
        """
        pass

    @staticmethod
    def _intersection(list_of_sets: list) -> set:
        master = list_of_sets[0]

        for s in list_of_sets[1:]:
            master = master.intersection(s)

        return master

    def process(self,
                sequences: list) -> list:

        solutions = []
        for sequence in sequences:

            sets = []
            for keyterm in sequence:
                sets.append(set(d_index_by_keyterm_kb[keyterm]))

            candidates = self._intersection(sets)
            if len(candidates) == 1:
                solutions.append(d_index_by_slot_kb[list(candidates)[0]])
            elif len(candidates) > 1:
                # Handle ambiguity: prefer exact sequence match
                # e.g., ['last', 'week'] matches 'last week' over 'last 1 week'
                exact_match = ' '.join(sequence)
                if exact_match in candidates:
                    solutions.append(d_index_by_slot_kb[exact_match])

        return solutions
