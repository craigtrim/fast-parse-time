# Development

Install the checkout and its test dependencies in a virtual environment before
running the suite.

```sh
python -m venv .venv
```

Activate the environment, then install the package in editable mode:

```sh
python -m pip install -e ".[test]" build
python -m pytest -q
```

On Windows, you can use `.venv\Scripts\python.exe` in place of `python`
without activating the environment. With Poetry, use `poetry install` followed
by `poetry run python -m pytest -q`.

## Working on parser behavior

Public functions are defined in `src/fast_parse_time/api.py`, and public
result types are defined in `models.py`. Calendar extraction and missing-year
inference are implemented in `explicit/calendar_parser.py`. Relative
expression handling is under `implicit`.

For calendar-date changes, check both the matched text and the parsed result.
A string can be a valid date expression while its year or numeric order remains
unresolved. Cover those outcomes alongside resolved dates. Include cases at
both range boundaries and across year boundaries when changing year inference.

For relative-expression changes, check the extracted quantity, frame, and
tense before checking datetime conversion. Use a fixed reference for arithmetic
assertions. Tests for named weekdays also need to control the local date used
during extraction.

Keep examples focused on public imports from `fast_parse_time`. Older import
paths are covered by compatibility checks. Application code controls logging;
the library's named loggers leave root handlers and levels unchanged.

## Running tests

The test groups cover different behavior:

| Directory | Coverage |
|---|---|
| `tests/core` | Supported formats, API results, and regression cases |
| `tests/compat` | Comparisons with other date parsers |
| `tests/red_team` | Adversarial inputs and documented gaps |

The `test` extra includes `dateparser` for comparison tests. It is not a
runtime dependency of the library.

A run can include `xfailed` cases for known gaps and `xpassed` cases whose
assertions pass despite an expected-failure marker. Review a marker when the
supported behavior changes. Package checks also cover legacy imports, model
name resolution in pickles, deferred table loading, and generator serialization.

CI runs the complete suite on Python 3.10 to 3.14 on Linux, plus Python 3.11 and
3.14 on Windows. Publication waits for those tests and the installed-wheel check.

## Building and checking a distribution

Build the source distribution and wheel from the repository root:

```sh
python -m build
```

Install the built wheel with its `[test]` extra in a fresh virtual environment.
Run that environment's Python from outside the checkout, passing the path to
the repository's `tests` directory to `python -m pytest`.

The imported `fast_parse_time.__file__` should point into the environment's
`site-packages`. Leave `PYTHONPATH` unset so the check exercises the installed
distribution. CI performs this check before running the complete suite against
the wheel.

## Maintaining relative-expression tables

The `scripts/generate_*_kb.py` utilities add expression families to the tables
under `src/fast_parse_time/implicit/knowledge_base`. Run them after installing
the checkout in editable mode. Each script updates part of the knowledge base;
the scripts do not provide a complete rebuild from an empty table set.

Review the phrase table, keyterm index, and counter changes together. Run the
complete suite after an update. The `Slot` value type is defined in
`implicit/models.py` and is shared by the generators and the parser.
