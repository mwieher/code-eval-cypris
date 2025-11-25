# Test Case 06: Missing Doc-Number Element

## Description
Tests handling of `<document-id>` elements that don't contain a `<doc-number>` child element.

## Assumptions
- Well-formed XML
- Some `<document-id>` elements have no `<doc-number>` child
- Other child elements may be present (country, kind, etc.)
- Represents incomplete data or different document-id types

## Expected Behavior
- Elements without `<doc-number>` should be silently skipped
- Should not cause errors or exceptions
- Should extract only valid doc-numbers from other elements

## Expected Output
```
111111111
333333333
```

## Notes
- Tests graceful handling of missing required data
- Validates that we don't crash on incomplete structures
- Important for production robustness with partial data

