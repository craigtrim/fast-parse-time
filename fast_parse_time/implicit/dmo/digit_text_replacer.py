#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Replace Spelled-Out forms of Numbers with their Digits """


from word2number import w2n


class DigitTextReplacer(object):
    """ Replace Spelled-Out forms of Numbers with their Digits

    e.g., 'three' => 3
    """

    # Indefinite articles that imply cardinality of 1
    INDEFINITE_ARTICLES = {'a', 'an'}

    # Informal quantity words mapped to numeric values
    # Note: 'couple' is already in KB with explicit patterns like 'last couple of weeks'
    INFORMAL_QUANTITIES = {'several': '3', 'few': '3'}

    # Multi-token phrase replacements (order matters - longer phrases first)
    PHRASE_REPLACEMENTS = [
        ('half an hour', '30 minutes'),
        ('half a day', '12 hours'),
    ]

    def __init__(self):
        """ Change Log

        Created:
            11-Aug-2022
            craigtrim@gmail.com
        Updated:
            23-Jan-2026
            craigtrim@gmail.com
            *   Handle indefinite articles 'a' and 'an' as 1
                https://github.com/craigtrim/fast-parse-time/issues/4
            *   Handle informal expressions 'half an hour', 'several'
                https://github.com/craigtrim/fast-parse-time/issues/5
        """
        pass

    def _replace_phrases(self, tokens: list) -> list:
        """Replace multi-token phrases before individual token processing."""
        text = ' '.join(tokens)
        for phrase, replacement in self.PHRASE_REPLACEMENTS:
            text = text.replace(phrase, replacement)
        return text.split()

    def process(self,
                tokens: list) -> list:
        # First, handle multi-token phrase replacements
        tokens = self._replace_phrases(tokens)

        normalized = []

        for token in tokens:
            # Handle indefinite articles as 1
            if token in self.INDEFINITE_ARTICLES:
                normalized.append('1')
            # Handle informal quantity words
            elif token in self.INFORMAL_QUANTITIES:
                normalized.append(self.INFORMAL_QUANTITIES[token])
            else:
                try:
                    normalized.append(str(w2n.word_to_num(token)))
                except ValueError:
                    normalized.append(token)

        return normalized
