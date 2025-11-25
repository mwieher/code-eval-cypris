# Test Case 10: Malformed XML - Unclosed Tag

## Description
Tests handling of malformed XML with an unclosed tag, simulating network interruption or corrupted data.

## Assumptions
- Invalid XML - missing closing tag for `<application-reference>`
- Represents network blip, truncated file, or storage corruption
- Parser should attempt recovery or fail gracefully

## Expected Behavior
- **Option A**: lxml's recovery parser fixes the issue and extracts available data
- **Option B**: Raises XMLParseError with clear message
- Should not crash the application

## Expected Output
```
Either:
- 111111111 (if recovery successful)
- XMLParseError exception (if recovery fails)
```

## Notes
- Tests error handling for malformed XML
- Challenge specifically mentions "network blips" and "messy XML"
- lxml's recover=True should handle this gracefully
- Important for production robustness

