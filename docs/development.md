# Development and package layout

Install the checkout before running tests. The `src` layout keeps tests from
accidentally importing an uninstalled copy of the package.

```sh
python -m venv .venv
# Activate .venv using your shell's activation command, then:
python -m pip install -e ".[test]" build
python -m pytest -q
```

On Windows, activation is optional: use `.venv\Scripts\python.exe` in place of
`python`. With Poetry, run `poetry install` and `poetry run python -m pytest -q`.

## Source organization

```text
src/fast_parse_time/
    __init__.py                 Public exports, loaded on demand
    api.py                      Public parsing functions
    models.py                   Public result types and DateType
    _logging.py                 Named loggers; no application configuration
    _timing.py                  Internal timing helper
    explicit/
        calendar_parser.py      Calendar dates, batches, and year inference
        extraction.py           Explicit date extraction
        classification.py       Numeric date classification
        tokenization.py         Numeric token recognition and splitting
        validation.py           Calendar and component validation
        normalization.py        Text normalization
        constants.py            Date vocabulary and bounds
        types.py                Internal component classifications
    implicit/
        extraction.py           Relative expression analysis
        resolution.py           Apply relative offsets to a datetime
        normalization.py        Written numbers and relative vocabulary
        sequences.py            Keyword extraction, filtering, and matching
        models.py               Lightweight internal Slot type
        knowledge_base/         Committed lookup tables
tests/
    core/                       Regression and behavior tests
    compat/                     Comparisons with other parsers
    red_team/                   Adversarial inputs and known gaps
scripts/                        Lookup-table maintenance utilities
```

`api.py` coordinates parsing; implementation belongs in the corresponding
`explicit` or `implicit` module. Public models depend on standard-library types,
not parsing services. Parsing modules import canonical modules directly.

The previous `bp`, `svc`, `dmo`, `dto`, `core`, and `calendar_dates` import paths
remain as compatibility modules. They forward to the same implementations and
types, preserving existing callers and model references in older pickles. New
code should use package-root public imports or the descriptive internal modules.
The root-level `calendar_dates.py` contains only this compatibility forwarding;
the implementation is in `explicit/calendar_parser.py`.

Importing public models or using the calendar-date API does not load the relative
lookup tables. They load when relative parsing needs them. Library loggers leave
root handlers and levels to the calling application.

## Tests and builds

The existing test groups and expected-failure markers are retained. A successful
run can include `xfailed` cases for known gaps and `xpassed` cases that now work.
Neither means those cases were removed or skipped. The package-layout regression
tests cover legacy imports, pickle name resolution, lazy table loading, logging,
and generator serialization.

CI runs the complete suite on Python 3.10–3.14 on Linux and 3.11/3.14 on Windows.
A separate job builds the source distribution and wheel, installs the wheel, and
runs the same tests from outside the checkout. Release publication depends on
these checks. To build locally:

```sh
python -m build
```

For a local wheel check, install the built wheel with its `[test]` extra in a
fresh virtual environment. From a directory outside the checkout, run that
environment's Python with `-m pytest /path/to/checkout/tests -q`. Do not set
`PYTHONPATH` to `src`; the test must exercise the installed artifact.

## Lookup-table maintenance

The `scripts/generate_*_kb.py` utilities update the committed tables under
`src/fast_parse_time/implicit/knowledge_base`. Install the checkout in editable
mode before running them. Each script adds a specific family of expressions;
these scripts do not regenerate the entire knowledge base from scratch.

Review all three table diffs together and run the complete suite after updates.
Keep the `Slot` type in `implicit/models.py`, outside generated data. Moving the
package did not change the existing table entries.
