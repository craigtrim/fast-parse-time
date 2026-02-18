#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Generate KB entries for decade unit support.

Related GitHub Issue:
    #19 - Gap: decade as a time unit not recognized
    https://github.com/craigtrim/fast-parse-time/issues/19

decade = 10 years. All patterns normalize to frame='year' with cardinality=N*10.

Updates three KB files:
    - index_by_slot_kb.py
    - index_by_keyterm_kb.py
    - keyterm_counter_kb.py
"""

import ast
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DTO_DIR = os.path.join(BASE, 'fast_parse_time', 'implicit', 'dto')

SLOT_KB_PATH = os.path.join(DTO_DIR, 'index_by_slot_kb.py')
KEYTERM_KB_PATH = os.path.join(DTO_DIR, 'index_by_keyterm_kb.py')
COUNTER_KB_PATH = os.path.join(DTO_DIR, 'keyterm_counter_kb.py')

DECADE_MULTIPLIER = 10
MAX_DECADES = 100  # supports 1..100 decades (= 10..1000 years)


def unit_word(n: int) -> str:
    """Return 'decade' for n=1, 'decades' for n>1."""
    return 'decade' if n == 1 else 'decades'


def build_slot_entries() -> dict:
    """
    Build all decade slot entries.
    Returns dict mapping phrase -> {Cardinality, Frame, Tense}.
    """
    entries = {}
    cardinality = DECADE_MULTIPLIER  # always N * 10

    # Bare singular forms (article 'a' or bare '1 decade')
    singular_past = [
        'a decade ago',
        'a decade back',
        'a decade before now',
        'a decade prior',
        'last decade',
        'past decade',
        '1 decade',  # bare, defaults to past per dateparser convention
    ]
    singular_future = [
        'a decade from now',
        'in a decade',
        'next decade',
    ]

    for phrase in singular_past:
        entries[phrase] = {'Cardinality': cardinality, 'Frame': 'year', 'Tense': 'past'}
    for phrase in singular_future:
        entries[phrase] = {'Cardinality': cardinality, 'Frame': 'year', 'Tense': 'future'}

    # Numeric patterns for N=1..MAX_DECADES
    for n in range(1, MAX_DECADES + 1):
        unit = unit_word(n)
        years = n * DECADE_MULTIPLIER

        past_suffixes = ['ago', 'back', 'before now', 'prior']
        for suffix in past_suffixes:
            phrase = f'{n} {unit} {suffix}'
            entries[phrase] = {'Cardinality': years, 'Frame': 'year', 'Tense': 'past'}

        future_suffixes = ['from now']
        for suffix in future_suffixes:
            phrase = f'{n} {unit} {suffix}'
            entries[phrase] = {'Cardinality': years, 'Frame': 'year', 'Tense': 'future'}

        # in N decade(s)
        entries[f'in {n} {unit}'] = {'Cardinality': years, 'Frame': 'year', 'Tense': 'future'}

        # last/next/past N decade(s) — for N >= 2 (N=1 handled via 'last decade' etc.)
        if n >= 2:
            entries[f'last {n} {unit}'] = {'Cardinality': years, 'Frame': 'year', 'Tense': 'past'}
            entries[f'next {n} {unit}'] = {'Cardinality': years, 'Frame': 'year', 'Tense': 'future'}
            entries[f'past {n} {unit}'] = {'Cardinality': years, 'Frame': 'year', 'Tense': 'past'}

    return entries


def load_kb(path: str) -> dict:
    """Load a KB file by executing it and extracting the dict variable."""
    with open(path, 'r', encoding='utf-8') as f:
        source = f.read()
    ns = {}
    exec(source, ns)  # noqa: S102
    # Find the dict variable (the one that isn't a module-level dunder)
    for k, v in ns.items():
        if isinstance(v, dict) and not k.startswith('__'):
            return v, k
    raise ValueError(f'No dict found in {path}')


def serialize_kb(var_name: str, kb: dict, header: str) -> str:
    """Serialize a KB dict back to Python source with a standard header."""
    lines = [
        header,
        '',
        f'{var_name} = {{',
    ]
    for key, value in kb.items():
        lines.append(f'    {repr(key)}: {repr(value)},')
    lines.append('}')
    return '\n'.join(lines) + '\n'


def get_file_header(path: str) -> str:
    """Extract the shebang + encoding comment from a KB file."""
    with open(path, 'r', encoding='utf-8') as f:
        lines = []
        for line in f:
            if line.startswith('#') or line.strip() == '':
                lines.append(line.rstrip())
            else:
                break
    return '\n'.join(lines)


def update_slot_kb(new_entries: dict):
    """Add decade entries to index_by_slot_kb.py."""
    print(f'Loading slot KB from {SLOT_KB_PATH}...')
    kb, var_name = load_kb(SLOT_KB_PATH)
    before = len(kb)

    added = 0
    for phrase, value in new_entries.items():
        if phrase not in kb:
            kb[phrase] = value
            added += 1

    print(f'  Adding {added} new entries (had {before}, now {len(kb)})')

    header = get_file_header(SLOT_KB_PATH)
    source = serialize_kb(var_name, kb, header)

    # Validate syntax
    ast.parse(source)

    with open(SLOT_KB_PATH, 'w', encoding='utf-8') as f:
        f.write(source)
    print(f'  Written: {SLOT_KB_PATH}')


def update_keyterm_kb(new_entries: dict):
    """
    Update index_by_keyterm_kb.py for decade support.

    The intersection algorithm in sequence_solution_finder.py requires that
    EVERY token in a phrase appears as a key in the keyterm KB, and that the
    phrase appears in the list for EACH of those keys.

    For example, '1 decade ago' must appear in:
        kb['1'], kb['decade'], kb['ago']

    This function:
        1. Adds new 'decade' and 'decades' keys with all their phrases.
        2. For every new phrase, appends it to any existing keyterm key whose
           token appears in that phrase (e.g., adds '1 decade ago' to kb['1']
           and kb['ago']).
    """
    print(f'Loading keyterm KB from {KEYTERM_KB_PATH}...')
    kb, var_name = load_kb(KEYTERM_KB_PATH)

    # Step 1: build phrase lists for the new 'decade'/'decades' keys
    decade_phrases = []
    decades_phrases = []
    for phrase in new_entries:
        tokens = phrase.lower().split()
        if 'decade' in tokens:
            decade_phrases.append(phrase)
        if 'decades' in tokens:
            decades_phrases.append(phrase)

    decade_phrases.sort()
    decades_phrases.sort()

    if 'decade' not in kb:
        kb['decade'] = decade_phrases
        print(f'  Added keyterm "decade" with {len(decade_phrases)} phrases')
    if 'decades' not in kb:
        kb['decades'] = decades_phrases
        print(f'  Added keyterm "decades" with {len(decades_phrases)} phrases')

    # Step 2: for every new phrase, add it to every existing keyterm key whose
    # token appears in that phrase (so the intersection finds the phrase).
    existing_keys = set(kb.keys())
    updates = 0
    for phrase in new_entries:
        tokens = phrase.lower().split()
        for token in tokens:
            if token in existing_keys and token not in ('decade', 'decades'):
                phrase_set = set(kb[token])
                if phrase not in phrase_set:
                    kb[token] = sorted(set(kb[token]) | {phrase})
                    updates += 1

    print(f'  Updated {updates} existing keyterm entries with new decade phrases')

    header = get_file_header(KEYTERM_KB_PATH)
    source = serialize_kb(var_name, kb, header)

    ast.parse(source)

    with open(KEYTERM_KB_PATH, 'w', encoding='utf-8') as f:
        f.write(source)
    print(f'  Written: {KEYTERM_KB_PATH}')


def update_counter_kb(new_entries: dict):
    """
    Add counts for 'decade' and 'decades' in keyterm_counter_kb.py.
    """
    print(f'Loading counter KB from {COUNTER_KB_PATH}...')
    kb, var_name = load_kb(COUNTER_KB_PATH)

    decade_count = sum(1 for p in new_entries if 'decade' in p.lower().split())
    decades_count = sum(1 for p in new_entries if 'decades' in p.lower().split())

    added = 0
    if 'decade' not in kb:
        kb['decade'] = decade_count
        added += 1
        print(f'  Added counter "decade" = {decade_count}')
    if 'decades' not in kb:
        kb['decades'] = decades_count
        added += 1
        print(f'  Added counter "decades" = {decades_count}')

    if added == 0:
        print('  No changes needed.')
        return

    header = get_file_header(COUNTER_KB_PATH)
    source = serialize_kb(var_name, kb, header)

    ast.parse(source)

    with open(COUNTER_KB_PATH, 'w', encoding='utf-8') as f:
        f.write(source)
    print(f'  Written: {COUNTER_KB_PATH}')


def main():
    print('Building decade slot entries...')
    new_entries = build_slot_entries()
    print(f'  Generated {len(new_entries)} decade patterns')

    update_slot_kb(new_entries)
    update_keyterm_kb(new_entries)
    update_counter_kb(new_entries)

    print('\nDone. Run `poetry run pytest tests/test_decade_unit.py` to verify.')


if __name__ == '__main__':
    main()
