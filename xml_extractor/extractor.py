"""Core extraction logic for doc-number values."""

from .parser import parse_xml


def get_priority(format_value: str | None) -> int:
    """Get priority value for a format attribute.

    Args:
        format_value: The format attribute value (e.g., 'epo', 'patent-office')

    Returns:
        Priority integer (lower is higher priority)
    """
    priority_map = {
        "epo": 0,
        "patent-office": 1,
    }
    if format_value is None:
        return 3
    return priority_map.get(format_value, 2)


def extract_doc_numbers(xml_content: str) -> list[str]:
    """Extract doc-number values from XML in priority order.

    Args:
        xml_content: String containing XML content

    Returns:
        List of doc-number values in priority order:
        1. format="epo" first
        2. format="patent-office" second
        3. Other formats third
        4. No format attribute last

    Example:
        >>> xml = '''<root>
        ...   <document-id format="patent-office">
        ...     <doc-number>66667777</doc-number>
        ...   </document-id>
        ...   <document-id format="epo">
        ...     <doc-number>999000888</doc-number>
        ...   </document-id>
        ... </root>'''
        >>> extract_doc_numbers(xml)
        ['999000888', '66667777']
    """
    # Parse XML
    root = parse_xml(xml_content)

    # Find all document-id elements
    # Use XPath to handle potential namespaces
    document_ids = root.xpath(".//document-id")

    # Extract doc-numbers with their format and order
    doc_data: list[tuple[str, int, int]] = []

    for idx, doc_id in enumerate(document_ids):
        # Get format attribute
        format_value = doc_id.get("format")

        # Find doc-number child element
        doc_number_elements = doc_id.xpath("./doc-number")

        if not doc_number_elements:
            continue

        # Get text content and clean it
        doc_number = doc_number_elements[0].text

        if doc_number:
            doc_number = doc_number.strip()

            # Skip empty values
            if doc_number:
                priority = get_priority(format_value)
                doc_data.append((doc_number, priority, idx))

    # Sort by priority, then by document order
    doc_data.sort(key=lambda x: (x[1], x[2]))

    # Return just the doc-numbers
    return [doc_num for doc_num, _, _ in doc_data]
