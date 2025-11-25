# Test Case 04: Whitespace Handling

## Description
Tests handling of various whitespace scenarios in doc-number values, which can occur due to formatting or data entry issues.

## Assumptions
- Well-formed XML
- Doc-number values contain leading/trailing whitespace, newlines, tabs
- Some values have internal whitespace (should be preserved)
- Realistic data quality issues from manual entry or formatting

## Expected Behavior
- Leading and trailing whitespace should be stripped
- Internal whitespace should be preserved (if any)
- Empty or whitespace-only values should be filtered out

## Expected Output
```
AAA111BBB
CCC222DDD
EEE333FFF
```

## Notes
- Tests data cleaning/normalization
- Validates that we handle real-world messy data
- Important for production robustness

