# System Boundaries

## Philosophy

Every software system has boundaries. This is not a limitation to apologize for—it's an inherent property of design.

When we discover a boundary, we face a choice:
1. **Expand the system** to handle the edge case
2. **Document the boundary** and keep scope focused

The temptation is always to expand. But systems grow in complexity with each addition. Larger, more complex systems have **more boundaries**, and those boundaries become **harder to discover**.

This document identifies and documents the boundaries of `fast-parse-time`. These boundaries represent **conscious design decisions** that keep the library focused, predictable, and maintainable.

---

## Discovered Boundaries

### 1. Single Delimiter Type Per Extraction

**Behavior**: Only one delimiter type (`/`, `-`, or `.`) is processed per function call.

**Example**:
```python
extract_numeric_dates("Dates: 12/31/2023, 01-15-2024, 02.14.2024")
# Returns: {'02.14.2024': 'FULL_EXPLICIT_DATE'}
# Missing: 12/31/2023 and 01-15-2024
```

**Rationale**: Tokenizer optimization—processing one delimiter pattern at a time simplifies parsing and reduces false positives.

**Workaround**: Process text multiple times with different expected formats, or normalize delimiters before extraction.

---

### 2. Whitespace Boundary Requirements

**Behavior**: Dates must be surrounded by whitespace or punctuation. Dates embedded in continuous alphanumeric strings are not extracted.

**Examples**:
```python
# ❌ Not extracted
extract_numeric_dates("StartDate:12/31/2023EndDate")  # No boundaries
extract_numeric_dates("[06/15/1990]")                  # Bracket touches date
extract_numeric_dates("document_2023-12-31_final.pdf") # Filename embedding
extract_numeric_dates("ABC-12-31-2023-XYZ")            # Product code

# ✅ Extracted
extract_numeric_dates("Date: 12/31/2023 End")         # Clear boundaries
extract_numeric_dates("DOB: 06/15/1990")               # Space after colon
```

**Rationale**: Boundary detection prevents false positives in dense numeric contexts and reduces misidentification of version numbers, IDs, and codes.

**Workaround**: Pre-process text to add spaces around dates, or use regex to extract candidates first.

---

### 3. No Contextual Format Inference

**Behavior**: Context (nearby text, year mentions) does not influence date extraction or classification.

**Example**:
```python
extract_numeric_dates("In 2024, specifically 5/6, we launch")
# Returns: None (comma interferes with tokenization)
```

**Rationale**: Context-free parsing is faster and more predictable. Adding context awareness would dramatically increase complexity.

---

### 4. Generic Classification for Complete Dates

**Behavior**: Full dates (MM/DD/YYYY) are always classified as `FULL_EXPLICIT_DATE`, even when format hints suggest specific interpretation.

**Example**:
```python
extract_numeric_dates("Event: 25/03/2023")
# Returns: {'25/03/2023': 'FULL_EXPLICIT_DATE'}
# Not: 'DAY_MONTH' (even though 25 > 12, indicating European format)
```

**Rationale**: Avoids assumptions about locale. Applications requiring format-specific interpretation can implement their own logic using the date string.

---

### 5. Trailing or Multiple Delimiters Break Patterns

**Behavior**: Extra delimiters prevent extraction.

**Examples**:
```python
extract_numeric_dates("Date: 12/31/2023/")  # Trailing delimiter
# Returns: None

extract_numeric_dates("Date: 12//31//2023")  # Double delimiters
# Returns: None
```

**Rationale**: Strict pattern matching reduces ambiguity and false positives.

---

### 6. Alphanumeric Prefix Attachment

**Behavior**: Text labels directly adjacent to dates (no space) prevent extraction.

**Example**:
```python
extract_numeric_dates("Date:06/15/2023")  # No space after colon
# Returns: None

extract_numeric_dates("Date: 06/15/2023")  # Space after colon
# Returns: {'06/15/2023': 'FULL_EXPLICIT_DATE'}
```

**Rationale**: Tokenization requires clean boundaries to distinguish dates from other numeric patterns.

---

### 7. Special Character Enclosure

**Behavior**: Dates enclosed in brackets or parentheses without spaces are not extracted.

**Examples**:
```python
extract_numeric_dates("[06/15/1990]")      # No extraction
extract_numeric_dates("(12/31/2023)")       # No extraction
extract_numeric_dates("[ 06/15/1990 ]")     # Would extract with spaces
```

**Rationale**: Boundary detection treats these as alphanumeric continuations without spacing.

---

## Testing Boundaries

All boundaries are documented through automated tests:

- **`tests/test_key_behaviors.py`**: 39 tests covering core functionality
- **`tests/test_boundary_cases.py`**: 51 tests probing system limits

These tests serve as:
1. **Regression prevention**: Boundaries stay stable
2. **Documentation**: Examples of what works and what doesn't
3. **Design specification**: Intentional behavior, not bugs

---

## When to Expand Boundaries

Consider expanding the system when:

1. **Core use case is blocked**: A boundary prevents the primary use case
2. **Simple, contained solution exists**: Fix doesn't ripple through the system
3. **Clear demand**: Multiple users encounter the same boundary

Don't expand when:
- The boundary affects edge cases only
- Workarounds exist at the application level
- Expansion would significantly increase complexity

---

## Contributing

If you encounter a boundary:

1. **Check this document** to see if it's known
2. **Consider workarounds** at your application level
3. **Open an issue** if the boundary blocks your core use case

Include:
- Real-world example of the boundary
- Why application-level workarounds aren't viable
- Proposed solution that maintains simplicity
