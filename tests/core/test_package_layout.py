"""Contracts that must survive reorganizing the installed package."""

from importlib import import_module, util
from pathlib import Path
import pickle
import subprocess
import sys
import textwrap

import pytest


@pytest.mark.parametrize(('legacy', 'canonical', 'name'), [
    ('explicit.bp.explicit_time_extractor', 'explicit.extraction', 'ExplicitTimeExtractor'),
    ('explicit.dmo.day_month_validator', 'explicit.validation', 'DayMonthValidator'),
    ('explicit.dmo.stdlib_date_validator', 'explicit.validation', 'try_parse_date'),
    ('explicit.dmo.delimited_date_classifier', 'explicit.classification', 'DelimitedDateClassifier'),
    ('explicit.svc.classify_numeric_components', 'explicit.classification', 'ClassifyNumericComponents'),
    ('explicit.svc.preclassify_numeric_components', 'explicit.tokenization', 'PreClassifyNumericComponents'),
    ('explicit.svc.tokenize_numeric_components', 'explicit.tokenization', 'TokenizeNumericComponents'),
    ('explicit.svc.validate_numeric_components', 'explicit.validation', 'ValidateNumericComponents'),
    ('explicit.svc.normalize_text', 'explicit.normalization', 'normalize_text'),
    ('implicit.svc.analyze_time_references', 'implicit.extraction', 'AnalyzeTimeReferences'),
    ('implicit.svc.resolve_time_references', 'implicit.resolution', 'ResolveTimeReferences'),
    ('implicit.dmo.digit_text_replacer', 'implicit.normalization', 'DigitTextReplacer'),
    ('implicit.dmo.keyword_sequence_extractor', 'implicit.sequences', 'KeywordSequenceExtractor'),
    ('implicit.dmo.keyword_sequence_filter', 'implicit.sequences', 'KeywordSequenceFilter'),
    ('implicit.dmo.sequence_solution_finder', 'implicit.sequences', 'SequenceSolutionFinder'),
    ('implicit.dto.index_by_slot_kb', 'implicit.models', 'Slot'),
    ('implicit.dto', 'implicit.knowledge_base', 'd_index_by_slot_kb'),
    ('implicit.dto.index_by_keyterm_kb', 'implicit.knowledge_base', 'd_index_by_keyterm_kb'),
    ('implicit.dto.keyterm_counter_kb', 'implicit.knowledge_base', 'd_keyterm_counter_kb'),
    ('explicit.dto', 'models', 'DateType'),
    ('explicit.dto', 'explicit.types', 'DateComponentType'),
    ('calendar_dates', 'models', 'ParsedDate'),
    ('calendar_dates', 'explicit.calendar_parser', 'parse_strings'),
    ('calendar_dates', 'explicit.calendar_parser', 'extract_strings'),
    ('core', '_logging', 'configure_logger'),
    ('core', '_timing', 'Stopwatch'),
])
def test_legacy_import_is_same_object(legacy, canonical, name):
    old = import_module(f'fast_parse_time.{legacy}')
    new = import_module(f'fast_parse_time.{canonical}')
    assert getattr(old, name) is getattr(new, name)


def test_root_exports_match_public_api():
    import fast_parse_time
    from fast_parse_time import api

    assert set(fast_parse_time.__all__) == set(api.__all__)
    namespace = {}
    exec('from fast_parse_time import *', namespace)
    for name in fast_parse_time.__all__:
        assert namespace[name] is getattr(api, name)


def run_isolated(code, tmp_path):
    result = subprocess.run(
        [sys.executable, '-I', '-c', textwrap.dedent(code)],
        cwd=tmp_path, capture_output=True, text=True, timeout=60,
    )
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize('operation', [
    'import fast_parse_time',
    '''from fast_parse_time import RelativeTime, ParsedDate, DateType
from fast_parse_time.implicit.dto.index_by_slot_kb import Slot
assert RelativeTime(2, 'day', 'past').to_timedelta().days == -2
assert Slot(2, 'day', 'past').cardinality == 2''',
    '''from fast_parse_time import parse_date_strings, extract_date_strings
texts = ['11/28/2025', '4/14/2026', 'March 13']
assert extract_date_strings(texts) == texts
assert parse_date_strings(texts)[-1].date.isoformat() == '2026-03-13' ''',
])
def test_imports_and_calendar_api_do_not_load_relative_tables(operation, tmp_path):
    run_isolated(operation + '''
import sys
tables = ('index_by_slot_kb', 'index_by_keyterm_kb', 'keyterm_counter_kb')
assert not any(f'fast_parse_time.implicit.knowledge_base.{name}' in sys.modules for name in tables)
assert 'fast_parse_time.implicit.extraction' not in sys.modules
''', tmp_path)


@pytest.mark.parametrize('configured', [False, True])
def test_library_leaves_root_logging_unchanged(configured, tmp_path):
    run_isolated(f'''
        import logging
        root = logging.getLogger()
        root.handlers.clear()
        if {configured!r}:
            root.addHandler(logging.NullHandler())
            root.setLevel(logging.ERROR)
        handlers, level = root.handlers[:], root.level
        from fast_parse_time import parse_dates
        assert parse_dates('3/28/2011 and 5 days ago').has_dates
        assert root.handlers == handlers
        assert root.level == level
    ''', tmp_path)


@pytest.mark.parametrize(('legacy', 'name', 'canonical'), [
    ('api', 'RelativeTime', 'models'),
    ('api', 'ExplicitDate', 'models'),
    ('api', 'ParseResult', 'models'),
    ('calendar_dates', 'ParsedDate', 'models'),
    ('explicit.dto', 'DateType', 'models'),
    ('implicit.dto.index_by_slot_kb', 'Slot', 'implicit.models'),
])
def test_pickle_can_resolve_original_model_paths(legacy, name, canonical):
    # Protocol 0 GLOBAL records use the qualified names stored in old pickles.
    record = f'cfast_parse_time.{legacy}\n{name}\n.'.encode('ascii')
    assert pickle.loads(record) is getattr(import_module(f'fast_parse_time.{canonical}'), name)


@pytest.mark.parametrize('script_name', [
    'generate_before_marker_kb', 'generate_decade_kb',
    'generate_short_units_kb', 'generate_singular_frames_kb',
])
def test_generators_target_relocated_tables_and_preserve_slot_values(script_name, tmp_path, monkeypatch):
    from fast_parse_time.implicit.models import Slot

    root = Path(__file__).resolve().parents[2]
    spec = util.spec_from_file_location(script_name, root / 'scripts' / f'{script_name}.py')
    generator = util.module_from_spec(spec)
    spec.loader.exec_module(generator)
    assert Path(generator.KB_DIR) == root / 'src' / 'fast_parse_time' / 'implicit' / 'knowledge_base'
    for attribute in ('SLOT_KB_PATH', 'KEYTERM_KB_PATH', 'COUNTER_KB_PATH'):
        assert Path(getattr(generator, attribute)).is_file()
    monkeypatch.setattr(generator, 'MAX_CARDINALITY', 2, raising=False)
    monkeypatch.setattr(generator, 'MAX_DECADES', 2, raising=False)
    entries = generator.build_slot_entries()
    assert entries and all(isinstance(value, Slot) for value in entries.values())

    # Run the real update functions against small temporary tables only.
    header = (
        'from fast_parse_time.implicit.models import Slot\n'
        "D='day'; H='hour'; MN='minute'; M='month'; S='second'; W='week'; Y='year'\n"
        "F='future'; P='past'; N='present'\n"
    )
    original = Slot(7, 'day', 'past')
    fixtures = [
        ('SLOT_KB_PATH', 'd_index_by_slot_kb', {'original phrase': original}),
        ('KEYTERM_KB_PATH', 'd_index_by_keyterm_kb', {'original': ['original phrase']}),
        ('COUNTER_KB_PATH', 'd_keyterm_counter_kb', {'original': 1}),
    ]
    for attribute, variable, values in fixtures:
        path = tmp_path / Path(getattr(generator, attribute)).name
        path.write_text(header + f'{variable} = {values!r}\n', encoding='utf-8')
        monkeypatch.setattr(generator, attribute, str(path))
    generator.update_slot_kb(entries)
    generator.update_keyterm_kb(entries)
    generator.update_counter_kb(entries)
    slots, _ = generator.load_kb(generator.SLOT_KB_PATH)
    assert slots == {'original phrase': original, **entries}
    assert generator.load_kb(generator.KEYTERM_KB_PATH)[0]['original'] == ['original phrase']
    assert generator.load_kb(generator.COUNTER_KB_PATH)[0]['original'] == 1
