# Test Fixtures - XML Attribute Extraction

This directory contains comprehensive test cases for the XML doc-number extraction system.

## Test Case Organization

Each test case is in its own subdirectory with:
- `input.xml` - The XML test data
- `README.md` - Description, assumptions, and expected behavior

## Test Case Index

### Valid XML Cases (Happy Path)

| # | Name | Description | Key Test |
|---|------|-------------|----------|
| 01 | basic_sample | Exact sample from challenge | Baseline functionality |
| 02 | priority_ordering | Reverse priority order in document | Priority sorting algorithm |
| 03 | multiple_application_refs | Multiple parent elements | Global extraction across document |
| 13 | large_document | 20+ document-id elements | Scalability and performance |
| 14 | special_characters | Special chars in doc-numbers | String preservation |

### Edge Cases (Data Quality)

| # | Name | Description | Key Test |
|---|------|-------------|----------|
| 04 | whitespace_handling | Leading/trailing/internal whitespace | Data normalization |
| 05 | missing_format_attribute | No format attribute | Graceful degradation |
| 06 | missing_doc_number_element | No doc-number child | Skip incomplete data |
| 07 | empty_doc_number | Empty or whitespace-only values | Data validation |
| 08 | no_document_ids | Valid XML, no document-id elements | Empty result handling |
| 09 | minimal_xml | Just root element | Minimal valid XML |
| 12 | duplicate_doc_numbers | Same doc-number multiple times | Duplicate handling |

### Error Cases (Malformed XML)

| # | Name | Description | Key Test |
|---|------|-------------|----------|
| 10 | malformed_unclosed_tag | Missing closing tag | Parser recovery |
| 11 | malformed_invalid_chars | Invalid XML characters | Corruption handling |

## Running Tests

### Run all fixture-based tests:
```bash
pytest tests/test_fixtures.py -v
```

### Run specific test case:
```bash
pytest tests/test_fixtures.py::test_fixture[01_basic_sample] -v
```

### Run only valid cases:
```bash
pytest tests/test_fixtures.py -k "not malformed" -v
```

## Test Coverage

- ✅ **Priority Ordering**: Cases 01, 02, 05, 13
- ✅ **Data Quality**: Cases 04, 06, 07, 12, 14
- ✅ **Edge Cases**: Cases 08, 09
- ✅ **Scalability**: Case 13
- ✅ **Error Handling**: Cases 10, 11
- ✅ **Multiple Parents**: Case 03

## Adding New Test Cases

To add a new test case:

1. Create a new directory: `tests/fixtures/NN_test_name/`
2. Add `input.xml` with test data
3. Add `README.md` with:
   - Description
   - Assumptions
   - Expected Behavior
   - Expected Output
   - Notes
4. Update this index
5. Add expected output to test runner if needed

## Expected Outputs

Each test case README documents the expected output. For automated testing, see `tests/test_fixtures.py` which contains the expected results for each case.

## Notes

- Test cases are designed to be independent and can run in any order
- Malformed XML cases may behave differently depending on lxml parser settings
- Some cases test multiple aspects simultaneously (e.g., priority + whitespace)
- Real-world patent XML may combine multiple issues from different test cases

