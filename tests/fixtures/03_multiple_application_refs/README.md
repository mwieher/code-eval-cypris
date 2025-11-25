# Test Case 03: Multiple Application References

## Description
Tests handling of multiple `<application-reference>` elements in a single document, which is realistic for patent data.

## Assumptions
- Well-formed XML
- Three separate `<application-reference>` elements
- Each contains multiple `<document-id>` elements
- Mix of epo and patent-office formats across all references
- Document represents related patent applications (continuation, divisional, etc.)

## Expected Behavior
- Should extract doc-numbers from ALL application-reference elements
- Should maintain priority ordering across the entire document
- All epo formats first, then all patent-office formats

## Expected Output
```
100001111
200002222
300003333
100004444
200005555
300006666
```

## Notes
- Tests that we don't stop after the first application-reference
- Validates global priority ordering across multiple parent elements
- Realistic scenario for patent family data

