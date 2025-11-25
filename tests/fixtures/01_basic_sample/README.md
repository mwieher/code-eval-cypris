# Test Case 01: Basic Sample from Challenge

## Description
This is the exact XML snippet provided in the challenge document. It represents the baseline "happy path" scenario.

## Assumptions
- Well-formed XML with proper closing tags
- Single `<application-reference>` element
- Two `<document-id>` elements with different formats
- First has `format="epo"`, second has `format="original"` (not "patent-office")
- All required child elements present (`<country>`, `<doc-number>`, etc.)
- No whitespace issues in doc-number values

## Expected Behavior
- Should extract both doc-numbers: `999000888` and `66667777`
- EPO format should come first despite appearing first in document
- Original format should come second (priority 2, as it's not "patent-office")

## Expected Output
```
999000888
66667777
```

## Notes
- The challenge mentions "patent-office" but the sample uses "original" - this tests our handling of non-standard format values
- Tests that we correctly prioritize epo (priority 0) over other formats (priority 2)

