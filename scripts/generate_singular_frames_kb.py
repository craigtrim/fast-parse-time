#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Generate KB entries for singular uninflected time frames.

Related GitHub Issue:
    #58 - Support 'before' as past-tense marker and singular uninflected time frames
    https://github.com/craigtrim/fast-parse-time/issues/58

Adds patterns like '2 week ago', '5 month ago', '10 year ago' (singular frames)
in addition to the plural forms that already exist.

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
    Build all singular frame slot entries with 'ago' and 'back'.
    Returns dict mapping phrase -> Slot(cardinality, frame, tense).

    Generates patterns like:
        '2 week ago' -> Slot(cardinality=2, frame='week', tense='past')
        '5 month ago' -> Slot(cardinality=5, frame='month', tense='past')
        '10 year ago' -> Slot(cardinality=10, frame='year', tense='past')
    """
    # Import Slot from the KB file
    from fast_parse_time.implicit.dto.index_by_slot_kb import Slot

    entries = {}

    # Define all time units (singular form)
    units = [
        'second',
        'minute',
        'hour',
        'day',
        'week',
        'month',
        'year',
    ]

    # Generate entries for each unit and cardinality with 'ago' and 'back'
    for unit in units:
        frame = unit  # frame is always singular
        for n in range(1, MAX_CARDINALITY + 1):
            # Singular form with 'ago'
            entries[f'{n} {unit} ago'] = Slot(cardinality=n, frame=frame, tense='past')
            # Singular form with 'back'
            entries[f'{n} {unit} back'] = Slot(cardinality=n, frame=frame, tense='past')

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
    """Add singular frame entries to index_by_slot_kb.py."""
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
    Update index_by_keyterm_kb.py for singular frame support.

    The intersection algorithm requires that EVERY token in a phrase appears
    as a key in the keyterm KB, and that the phrase appears in the list for
    EACH of those keys.

    For example, '2 week ago' must appear in: kb['2'], kb['week'], kb['ago']
    """
    print(f'Loading keyterm KB from {KEYTERM_KB_PATH}...')
    kb, var_name = load_kb(KEYTERM_KB_PATH)

    # Get all unit words (singular forms)
    units = ['second', 'minute', 'hour', 'day', 'week', 'month', 'year']

    # Ensure unit keys exist
    for unit in units:
        if unit not in kb:
            kb[unit] = []
            print(f'  Added keyterm "{unit}"')

    # For every new phrase, add it to all relevant keys
    existing_keys = set(kb.keys())
    updates = 0

    for phrase in new_entries:
        tokens = phrase.lower().split()

        # Add to all relevant keys (numbers, units, 'ago', 'back')
        for token in tokens:
            if token in existing_keys:
                phrase_set = set(kb[token])
                if phrase not in phrase_set:
                    kb[token] = sorted(set(kb[token]) | {phrase})
                    updates += 1

    print(f'  Updated {updates} keyterm entries with singular frame phrases')

    header = get_file_header(KEYTERM_KB_PATH)
    source = serialize_kb(var_name, kb, header)

    ast.parse(source)

    with open(KEYTERM_KB_PATH, 'w', encoding='utf-8') as f:
        f.write(source)
    print(f'  Written: {KEYTERM_KB_PATH}')


def update_counter_kb(new_entries: dict):
    """
    Add/update counts for singular unit words in keyterm_counter_kb.py.
    """
    print(f'Loading counter KB from {COUNTER_KB_PATH}...')
    kb, var_name = load_kb(COUNTER_KB_PATH)

    units = ['second', 'minute', 'hour', 'day', 'week', 'month', 'year']
    unit_counts = {}
    for unit in units:
        unit_counts[unit] = sum(1 for p in new_entries if unit in p.lower().split())

    added = 0
    updated = 0
    for unit, count in unit_counts.items():
        if unit not in kb:
            kb[unit] = count
            added += 1
            print(f'  Added counter "{unit}" = {count}')
        else:
            old_count = kb[unit]
            kb[unit] = old_count + count
            updated += 1
            print(f'  Updated counter "{unit}" from {old_count} to {kb[unit]} (+{count})')

    if added == 0 and updated == 0:
        print('  No changes needed.')
        return

    header = get_file_header(COUNTER_KB_PATH)
    source = serialize_kb(var_name, kb, header)

    ast.parse(source)

    with open(COUNTER_KB_PATH, 'w', encoding='utf-8') as f:
        f.write(source)
    print(f'  Written: {COUNTER_KB_PATH}')


def main():
    print('Building singular frame slot entries...')
    new_entries = build_slot_entries()
    print(f'  Generated {len(new_entries)} singular frame patterns')

    update_slot_kb(new_entries)
    update_keyterm_kb(new_entries)
    update_counter_kb(new_entries)

    print('\nDone. Run `pytest tests/test_tense_markers_and_singular_frames.py` to verify.')


if __name__ == '__main__':
    main()
