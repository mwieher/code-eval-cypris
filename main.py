"""CLI entry point for XML doc-number extraction."""

import sys
from pathlib import Path

from xml_extractor.exceptions import ExtractionError
from xml_extractor.extractor import extract_doc_numbers


def main():
    """Main CLI function."""
    # Check for file argument
    if len(sys.argv) > 1:
        # Read from file
        file_path = Path(sys.argv[1])

        if not file_path.exists():
            print(f"Error: File not found: {file_path}", file=sys.stderr)
            sys.exit(1)

        try:
            xml_content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Read from stdin
        xml_content = sys.stdin.read()

    # Extract doc-numbers
    try:
        doc_numbers = extract_doc_numbers(xml_content)

        # Output results (one per line)
        for doc_num in doc_numbers:
            print(doc_num)

    except ExtractionError as e:
        print(f"Extraction error: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(3)


if __name__ == "__main__":
    main()
