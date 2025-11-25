# Test Case 11: Malformed XML - Invalid Characters

## Description
Tests handling of XML with invalid/control characters that shouldn't appear in XML.

## Assumptions
- XML contains invalid control characters
- Represents data corruption or encoding issues
- May occur during transmission or storage

## Expected Behavior
- lxml parser should either:
  - Strip/ignore invalid characters and parse successfully
  - Raise XMLParseError with clear message
- Should not crash the application

## Expected Output
```
Either:
- 111111111 (if parser handles it)
- XMLParseError exception
```

## Notes
- Tests handling of corrupted data
- Important for production systems dealing with real-world messy data
- XML spec prohibits certain control characters

