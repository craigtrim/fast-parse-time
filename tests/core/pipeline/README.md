# Pipeline Tests

These tests cover the internal preprocessing stages that run before pattern matching: numeric component tokenization, digit-to-text replacement, and pre-classification of numeric tokens. They also include tests derived from `dateparser` capability comparisons. Verifying pipeline correctness here protects the downstream extractors from receiving malformed input.
