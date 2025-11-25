# Test Case 13: Large Document

## Description
Tests handling of a larger, more realistic patent document with many document-id elements.

## Assumptions
- Well-formed XML
- 20+ document-id elements
- Mix of all format types
- Represents realistic patent family with many related applications
- Tests performance and scalability

## Expected Behavior
- Should handle large number of elements efficiently
- Correct priority ordering across all elements
- No performance degradation

## Expected Output
```
(10 epo entries, then 5 patent-office entries, then 5 other entries)
EPO-001
EPO-002
EPO-003
EPO-004
EPO-005
EPO-006
EPO-007
EPO-008
EPO-009
EPO-010
PO-001
PO-002
PO-003
PO-004
PO-005
OTHER-001
OTHER-002
OTHER-003
OTHER-004
OTHER-005
```

## Notes
- Tests scalability
- Validates sorting algorithm works with larger datasets
- Important for production use with real patent data

