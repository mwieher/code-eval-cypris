# Test Case 02: Priority Ordering

## Description
Tests that priority ordering works correctly when formats appear in reverse priority order in the document.

## Assumptions
- Well-formed XML
- Three `<document-id>` elements with different formats
- Formats appear in document as: unknown, patent-office, epo (reverse priority)
- All elements have valid doc-numbers

## Expected Behavior
- Should reorder results by priority regardless of document order
- Priority: epo (0) > patent-office (1) > unknown (2)
- Within same priority, maintain document order

## Expected Output
```
111111111
222222222
333333333
```

## Notes
- Tests the core sorting algorithm
- Validates that document order is overridden by priority
- Tests handling of unknown format values

