# Test Case 05: Missing Format Attribute

## Description
Tests handling of `<document-id>` elements that lack the `format` attribute entirely.

## Assumptions
- Well-formed XML
- Some `<document-id>` elements have no `format` attribute
- Mixed with elements that do have format attributes
- Represents incomplete or legacy data

## Expected Behavior
- Elements without format attribute should still be extracted
- Should be placed at lowest priority (after epo, patent-office, and unknown formats)
- Within no-format group, maintain document order

## Expected Output
```
111111111
222222222
333333333
444444444
```

## Notes
- Tests graceful degradation when expected attributes are missing
- Validates priority system handles None/missing values
- Important for handling legacy or incomplete data

