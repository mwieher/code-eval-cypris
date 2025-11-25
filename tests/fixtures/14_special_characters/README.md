# Test Case 14: Special Characters in Doc-Numbers

## Description
Tests handling of doc-numbers containing special characters, hyphens, slashes, etc.

## Assumptions
- Well-formed XML
- Doc-numbers contain various special characters that are valid in patent numbers
- Represents real-world patent numbering schemes from different jurisdictions
- Characters like hyphens, slashes, periods are common in patent numbers

## Expected Behavior
- Should preserve special characters exactly as they appear
- No character escaping or modification
- Treat as literal string values

## Expected Output
```
US-2005-123456
EP/2005/789012
WO.2005.345678
```

## Notes
- Tests that we don't inadvertently modify or escape special characters
- Important for international patent numbers
- Validates string handling preserves original format

