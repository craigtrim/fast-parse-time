#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Generate KB entries for short unit abbreviations with implicit past tense.

Related GitHub Issue:
    #56 - Support short unit abbreviations (hr, hrs, min, mins, sec) in relative time parsing
    https://github.com/craigtrim/fast-parse-time/issues/56

Adds bare patterns like '15 hr', '2 min', '3 sec' (without 'ago') that default to past tense.

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

# Range of cardinalities to generate bare patterns for
MAX_CARDINALITY = 999  # matches existing pattern in KB


def build_slot_entries() -> dict:
    """
    Build all bare short unit slot entries (implicit past tense).
    Returns dict mapping phrase -> Slot(cardinality, frame, tense).

    Generates patterns like:
        '1 hr' -> Slot(cardinality=1, frame='hour', tense='past')
        '15 hrs' -> Slot(cardinality=15, frame='hour', tense='past')
        '2 min' -> Slot(cardinality=2, frame='minute', tense='past')
        '30 mins' -> Slot(cardinality=30, frame='minute', tense='past')
        '3 sec' -> Slot(cardinality=3, frame='second', tense='past')
        '45 secs' -> Slot(cardinality=45, frame='second', tense='past')
    """
    # Import Slot from the KB file
    from fast_parse_time.implicit.dto.index_by_slot_kb import Slot

    entries = {}

    # Hour abbreviations: hr, hrs
    for n in range(1, MAX_CARDINALITY + 1):
        entries[f'{n} hr'] = Slot(cardinality=n, frame='hour', tense='past')
        entries[f'{n} hrs'] = Slot(cardinality=n, frame='hour', tense='past')

    # Minute abbreviations: min, mins
    for n in range(1, MAX_CARDINALITY + 1):
        entries[f'{n} min'] = Slot(cardinality=n, frame='minute', tense='past')
        entries[f'{n} mins'] = Slot(cardinality=n, frame='minute', tense='past')

    # Second abbreviations: sec, secs
    for n in range(1, MAX_CARDINALITY + 1):
        entries[f'{n} sec'] = Slot(cardinality=n, frame='second', tense='past')
        entries[f'{n} secs'] = Slot(cardinality=n, frame='second', tense='past')

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
    """Add bare short unit entries to index_by_slot_kb.py."""
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
    Update index_by_keyterm_kb.py for bare short unit support.

    The intersection algorithm in sequence_solution_finder.py requires that
    EVERY token in a phrase appears as a key in the keyterm KB, and that the
    phrase appears in the list for EACH of those keys.

    For example, '15 hr' must appear in: kb['15'], kb['hr']

    This function:
        1. Adds new 'hr', 'hrs', 'min', 'mins', 'sec', 'secs' keys if missing.
        2. For every new phrase, appends it to any existing keyterm key whose
           token appears in that phrase (e.g., adds '15 hr' to kb['15'] and kb['hr']).
    """
    print(f'Loading keyterm KB from {KEYTERM_KB_PATH}...')
    kb, var_name = load_kb(KEYTERM_KB_PATH)

    # Step 1: build phrase lists for the new short unit keys
    unit_keys = ['hr', 'hrs', 'min', 'mins', 'sec', 'secs']
    unit_phrases = {key: [] for key in unit_keys}

    for phrase in new_entries:
        tokens = phrase.lower().split()
        for unit in unit_keys:
            if unit in tokens:
                unit_phrases[unit].append(phrase)

    for unit in unit_keys:
        unit_phrases[unit].sort()
        if unit not in kb:
            kb[unit] = unit_phrases[unit]
            print(f'  Added keyterm "{unit}" with {len(unit_phrases[unit])} phrases')
        else:
            # Update existing key by merging
            existing_set = set(kb[unit])
            new_set = set(unit_phrases[unit])
            kb[unit] = sorted(existing_set | new_set)
            print(f'  Updated keyterm "{unit}" with {len(new_set - existing_set)} new phrases')

    # Step 2: for every new phrase, add it to every existing keyterm key whose
    # token appears in that phrase (so the intersection finds the phrase).
    existing_keys = set(kb.keys())
    updates = 0
    for phrase in new_entries:
        tokens = phrase.lower().split()
        for token in tokens:
            if token in existing_keys and token not in unit_keys:
                phrase_set = set(kb[token])
                if phrase not in phrase_set:
                    kb[token] = sorted(set(kb[token]) | {phrase})
                    updates += 1

    print(f'  Updated {updates} existing keyterm entries with new bare short unit phrases')

    header = get_file_header(KEYTERM_KB_PATH)
    source = serialize_kb(var_name, kb, header)

    ast.parse(source)

    with open(KEYTERM_KB_PATH, 'w', encoding='utf-8') as f:
        f.write(source)
    print(f'  Written: {KEYTERM_KB_PATH}')


def update_counter_kb(new_entries: dict):
    """
    Add/update counts for 'hr', 'hrs', 'min', 'mins', 'sec', 'secs' in keyterm_counter_kb.py.
    """
    print(f'Loading counter KB from {COUNTER_KB_PATH}...')
    kb, var_name = load_kb(COUNTER_KB_PATH)

    unit_keys = ['hr', 'hrs', 'min', 'mins', 'sec', 'secs']
    unit_counts = {}
    for unit in unit_keys:
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
    print('Building bare short unit slot entries (implicit past tense)...')
    new_entries = build_slot_entries()
    print(f'  Generated {len(new_entries)} bare short unit patterns')

    update_slot_kb(new_entries)
    update_keyterm_kb(new_entries)
    update_counter_kb(new_entries)

    print('\nDone. Run `pytest tests/core/relative/test_short_unit_abbreviations.py` to verify.')


if __name__ == '__main__':
    main()
