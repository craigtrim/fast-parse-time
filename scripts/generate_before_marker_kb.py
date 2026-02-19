#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Generate KB entries for 'before' as a past-tense marker (like 'ago').

Related GitHub Issue:
    #58 - Support 'before' as past-tense marker and singular uninflected time frames
    https://github.com/craigtrim/fast-parse-time/issues/58

Adds patterns like '1 day before', '5 hours before', '3 weeks before' (without 'now')
that default to past tense, matching the behavior of 'ago'.

Updates three KB files:
    - index_by_slot_kb.py (phrase -> {Cardinality, Frame, Tense})
    - index_by_keyterm_kb.py (keyterm -> [phrases])
    - keyterm_counter_kb.py (keyterm -> count)
"""

import ast
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DTO_DIR = os.path.join(BASE, 'fast_parse_time', 'implicit', 'dto')

SLOT_KB_PATH = os.path.join(DTO_DIR, 'index_by_slot_kb.py')
KEYTERM_KB_PATH = os.path.join(DTO_DIR, 'index_by_keyterm_kb.py')
COUNTER_KB_PATH = os.path.join(DTO_DIR, 'keyterm_counter_kb.py')

# Range of cardinalities to generate patterns for
MAX_CARDINALITY = 999  # matches existing pattern in KB


def build_slot_entries() -> dict:
    """
    Build all 'before' marker slot entries (past tense).
    Returns dict mapping phrase -> Slot(cardinality, frame, tense).

    Generates patterns like:
        '1 day before' -> Slot(cardinality=1, frame='day', tense='past')
        '5 hours before' -> Slot(cardinality=5, frame='hour', tense='past')
        '3 weeks before' -> Slot(cardinality=3, frame='week', tense='past')
    """
    # Import Slot from the KB file
    from fast_parse_time.implicit.dto.index_by_slot_kb import Slot

    entries = {}

    # Define all time units (singular and plural forms)
    units = [
        ('second', 'seconds'),
        ('minute', 'minutes'),
        ('hour', 'hours'),
        ('day', 'days'),
        ('week', 'weeks'),
        ('month', 'months'),
        ('year', 'years'),
    ]

    # Generate entries for each unit and cardinality
    for singular, plural in units:
        frame = singular  # frame is always singular
        for n in range(1, MAX_CARDINALITY + 1):
            # Singular form (for n=1 or when used without regard to grammar)
            entries[f'{n} {singular} before'] = Slot(cardinality=n, frame=frame, tense='past')
            # Plural form (grammatically correct for n>1, but also works for n=1)
            entries[f'{n} {plural} before'] = Slot(cardinality=n, frame=frame, tense='past')

    # Also add abbreviated forms
    abbrev_units = [
        ('sec', 'secs', 'second'),
        ('min', 'mins', 'minute'),
        ('hr', 'hrs', 'hour'),
        ('wk', 'wks', 'week'),
        ('mo', 'mos', 'month'),
        ('yr', 'yrs', 'year'),
    ]

    for sing_abbrev, plur_abbrev, frame in abbrev_units:
        for n in range(1, MAX_CARDINALITY + 1):
            entries[f'{n} {sing_abbrev} before'] = Slot(cardinality=n, frame=frame, tense='past')
            entries[f'{n} {plur_abbrev} before'] = Slot(cardinality=n, frame=frame, tense='past')

    return entries


def load_kb(path: str) -> tuple:
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
    # Frame and tense constant mappings (from index_by_slot_kb.py)
    frame_to_const = {
        'day': 'D', 'hour': 'H', 'minute': 'MN', 'month': 'M',
        'second': 'S', 'week': 'W', 'year': 'Y'
    }
    tense_to_const = {'future': 'F', 'past': 'P', 'present': 'N'}

    lines = [
        header,
        f'{var_name} = {{',
    ]
    for key, value in kb.items():
        # Handle Slot NamedTuple properly
        if hasattr(value, '_asdict'):
            # It's a NamedTuple
            fields = value._asdict()
            # Handle string vs int cardinality
            cardinality = repr(fields['cardinality']) if isinstance(fields['cardinality'], str) else fields['cardinality']
            frame = frame_to_const.get(fields['frame'], repr(fields['frame']))
            tense = tense_to_const.get(fields['tense'], repr(fields['tense']))
            slot_repr = f'Slot({cardinality}, {frame}, {tense})'
            lines.append(f'    {repr(key)}: {slot_repr},')
        else:
            lines.append(f'    {repr(key)}: {repr(value)},')
    lines.append('}')
    return '\n'.join(lines) + '\n'


def get_file_header(path: str) -> str:
    """Extract everything before the dict definition from a KB file."""
    with open(path, 'r', encoding='utf-8') as f:
        lines = []
        for line in f:
            # Stop when we hit the dict definition line
            if '=' in line and 'd_index_by' in line or 'd_keyterm_counter_kb' in line:
                break
            lines.append(line.rstrip())
    return '\n'.join(lines)


def update_slot_kb(new_entries: dict):
    """Add 'before' marker entries to index_by_slot_kb.py."""
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
    Update index_by_keyterm_kb.py for 'before' marker support.

    The intersection algorithm in sequence_solution_finder.py requires that
    EVERY token in a phrase appears as a key in the keyterm KB, and that the
    phrase appears in the list for EACH of those keys.

    For example, '5 days before' must appear in: kb['5'], kb['days'], kb['before']
    """
    print(f'Loading keyterm KB from {KEYTERM_KB_PATH}...')
    kb, var_name = load_kb(KEYTERM_KB_PATH)

    # Ensure 'before' key exists
    if 'before' not in kb:
        kb['before'] = []
        print(f'  Added keyterm "before"')

    # For every new phrase, add it to 'before' key and other relevant keys
    existing_keys = set(kb.keys())
    updates = 0

    for phrase in new_entries:
        tokens = phrase.lower().split()

        # Add to 'before' key
        if phrase not in kb['before']:
            kb['before'].append(phrase)
            updates += 1

        # Add to all other relevant keys (numbers, units)
        for token in tokens:
            if token in existing_keys and token != 'before':
                phrase_set = set(kb[token])
                if phrase not in phrase_set:
                    kb[token] = sorted(set(kb[token]) | {phrase})
                    updates += 1

    # Sort 'before' key
    kb['before'] = sorted(kb['before'])

    print(f'  Updated {updates} keyterm entries with new "before" marker phrases')

    header = get_file_header(KEYTERM_KB_PATH)
    source = serialize_kb(var_name, kb, header)

    ast.parse(source)

    with open(KEYTERM_KB_PATH, 'w', encoding='utf-8') as f:
        f.write(source)
    print(f'  Written: {KEYTERM_KB_PATH}')


def update_counter_kb(new_entries: dict):
    """
    Add/update count for 'before' in keyterm_counter_kb.py.
    """
    print(f'Loading counter KB from {COUNTER_KB_PATH}...')
    kb, var_name = load_kb(COUNTER_KB_PATH)

    # Count how many phrases contain 'before'
    before_count = sum(1 for p in new_entries if 'before' in p.lower().split())

    if 'before' not in kb:
        kb['before'] = before_count
        print(f'  Added counter "before" = {before_count}')
    else:
        old_count = kb['before']
        kb['before'] = old_count + before_count
        print(f'  Updated counter "before" from {old_count} to {kb["before"]} (+{before_count})')

    header = get_file_header(COUNTER_KB_PATH)
    source = serialize_kb(var_name, kb, header)

    ast.parse(source)

    with open(COUNTER_KB_PATH, 'w', encoding='utf-8') as f:
        f.write(source)
    print(f'  Written: {COUNTER_KB_PATH}')


def main():
    print('Building "before" marker slot entries (past tense)...')
    new_entries = build_slot_entries()
    print(f'  Generated {len(new_entries)} "before" marker patterns')

    update_slot_kb(new_entries)
    update_keyterm_kb(new_entries)
    update_counter_kb(new_entries)

    print('\nDone. Run `pytest tests/test_tense_markers_and_singular_frames.py` to verify.')


if __name__ == '__main__':
    main()
