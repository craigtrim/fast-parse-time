# Tests

The test suite is organized into three top-level packages, each serving a distinct purpose. `core` contains the primary regression and behavioral tests for every pattern the library supports. `compat` verifies that the library produces correct or improved results relative to established NLP date parsing libraries. `red_team` contains adversarial tests designed to expose silent failures, boundary conditions, and inputs the parser should reject.
