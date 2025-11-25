"""XML parsing utilities."""

from lxml import etree

from .exceptions import XMLParseError


def parse_xml(xml_content: str) -> etree._Element:
    """Parse XML content into an element tree.

    Args:
        xml_content: String containing XML content

    Returns:
        Parsed XML element tree

    Raises:
        XMLParseError: If XML cannot be parsed
    """
    try:
        # Use lxml's lenient parser to handle malformed XML
        parser = etree.XMLParser(recover=True)
        root = etree.fromstring(xml_content.encode("utf-8"), parser=parser)
        return root
    except Exception as e:
        raise XMLParseError(f"Failed to parse XML: {e}") from e
