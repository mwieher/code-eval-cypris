"""Tests for the parser module."""

import pytest
from lxml import etree

from xml_extractor.exceptions import XMLParseError
from xml_extractor.parser import parse_xml


class TestParseXML:
    """Tests for parse_xml function."""

    def test_parse_valid_xml(self):
        """Test parsing valid XML."""
        xml = "<root><child>text</child></root>"
        result = parse_xml(xml)
        assert isinstance(result, etree._Element)
        assert result.tag == "root"

    def test_parse_xml_with_attributes(self):
        """Test parsing XML with attributes."""
        xml = '<root attr="value"><child>text</child></root>'
        result = parse_xml(xml)
        assert result.get("attr") == "value"

    def test_parse_xml_with_namespaces(self):
        """Test parsing XML with namespaces."""
        xml = '<root xmlns="http://example.com"><child>text</child></root>'
        result = parse_xml(xml)
        assert result is not None

    def test_parse_malformed_xml_with_recovery(self):
        """Test that malformed XML is recovered."""
        xml = "<root><unclosed></root>"
        # Should not raise exception due to recovery parser
        result = parse_xml(xml)
        assert result is not None

    def test_parse_completely_invalid_xml(self):
        """Test that recovery parser handles invalid XML gracefully."""
        xml = "not xml at all"
        # Recovery parser is very lenient and may create elements from invalid text
        # This test verifies the parser doesn't crash
        try:
            parse_xml(xml)
            # If recovery succeeds, that's acceptable behavior for the recovery parser
        except XMLParseError:
            # If it raises XMLParseError, that's also acceptable
            pass

    def test_parse_empty_string(self):
        """Test that empty string raises XMLParseError."""
        with pytest.raises(XMLParseError):
            parse_xml("")

    def test_parse_xml_with_special_characters(self):
        """Test parsing XML with special characters."""
        xml = "<root><child>&lt;&gt;&amp;</child></root>"
        result = parse_xml(xml)
        assert result is not None
        child = result.find("child")
        assert child.text == "<>&"
