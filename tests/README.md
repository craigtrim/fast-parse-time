# Tests

The test suite is organized into three top-level packages, each serving a distinct purpose. `core` contains the primary regression and behavioral tests for every pattern the library supports. `compat` verifies that the library produces correct or improved results relative to established NLP date parsing libraries. `red_team` contains adversarial tests designed to expose silent failures, boundary conditions, and inputs the parser should reject.

Install the checkout with `python -m pip install -e ".[test]"`, then run
`python -m pytest -q`. The test extra includes the comparison dependency
`dateparser`; the runtime package does not require it. Tests use importlib mode
and also run against the installed wheel in CI. See
[Development and package layout](../docs/development.md).
