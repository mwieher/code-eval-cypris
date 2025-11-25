# Test Case 12: Duplicate Doc-Numbers

## Description
Tests handling of duplicate doc-number values appearing multiple times in the document.

## Assumptions
- Well-formed XML
- Same doc-number appears in multiple document-id elements
- May have same or different format attributes
- Represents data redundancy or related applications

## Expected Behavior
- Should preserve all occurrences (no deduplication)
- Duplicates should be ordered by their respective priorities
- Document order maintained within same priority

## Expected Output
```
111111111
111111111
222222222
```

## Notes
- Tests that we don't inadvertently deduplicate
- Requirement doesn't specify deduplication, so preserve all
- Important to understand if downstream systems expect duplicates
- Could be legitimate (same patent number in different contexts)

