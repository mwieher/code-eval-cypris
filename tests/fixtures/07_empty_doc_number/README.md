# Test Case 07: Empty Doc-Number Elements

## Description
Tests handling of `<doc-number>` elements that exist but are empty or contain only whitespace.

## Assumptions
- Well-formed XML
- `<doc-number>` elements exist but have no text content
- Some are completely empty, some have only whitespace
- Represents data quality issues or placeholder elements

## Expected Behavior
- Empty doc-number elements should be filtered out
- Whitespace-only doc-numbers should be filtered out (after trimming)
- Should only return non-empty values

## Expected Output
```
111111111
333333333
```

## Notes
- Tests data validation and filtering
- Validates that we don't return empty strings
- Important for data quality in downstream systems

