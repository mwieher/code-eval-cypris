"""Tests for the extractor module."""

from xml_extractor.extractor import extract_doc_numbers, get_priority


class TestGetPriority:
    """Tests for get_priority function."""

    def test_epo_has_highest_priority(self):
        """EPO format should have priority 0."""
        assert get_priority("epo") == 0

    def test_patent_office_has_second_priority(self):
        """Patent-office format should have priority 1."""
        assert get_priority("patent-office") == 1

    def test_unknown_format_has_lower_priority(self):
        """Unknown formats should have priority 2."""
        assert get_priority("unknown") == 2

    def test_none_has_lowest_priority(self):
        """None format should have priority 3."""
        assert get_priority(None) == 3


class TestExtractDocNumbers:
    """Tests for extract_doc_numbers function."""

    def test_sample_xml_from_challenge(self):
        """Test with the exact sample from the challenge."""
        xml = """<root>
          <application-reference ucid="US-XXXXXXXX-A" is-representative="NO">
            <document-id mxw-id="ABCD99999999" load-source="docdb" format="epo">
              <country>US</country>
              <doc-number>999000888</doc-number>
              <kind>A</kind>
              <date>20051213</date>
              <lang>EN</lang>
            </document-id>
            <document-id mxw-id="ABCD88888888" load-source="patent-office" format="original">
              <country>US</country>
              <doc-number>66667777</doc-number>
              <lang>EN</lang>
            </document-id>
          </application-reference>
        </root>"""

        result = extract_doc_numbers(xml)
        assert result == ["999000888", "66667777"]

    def test_priority_ordering(self):
        """Test that epo comes before patent-office."""
        xml = """<root>
          <document-id format="patent-office">
            <doc-number>222</doc-number>
          </document-id>
          <document-id format="epo">
            <doc-number>111</doc-number>
          </document-id>
        </root>"""

        result = extract_doc_numbers(xml)
        assert result == ["111", "222"]

    def test_empty_xml(self):
        """Test with XML containing no document-id elements."""
        xml = "<root></root>"
        result = extract_doc_numbers(xml)
        assert result == []

    def test_whitespace_trimming(self):
        """Test that whitespace is trimmed from doc-numbers."""
        xml = """<root>
          <document-id format="epo">
            <doc-number>  123456  </doc-number>
          </document-id>
        </root>"""

        result = extract_doc_numbers(xml)
        assert result == ["123456"]

    def test_missing_doc_number_element(self):
        """Test that document-id without doc-number is skipped."""
        xml = """<root>
          <document-id format="epo">
            <country>US</country>
          </document-id>
          <document-id format="epo">
            <doc-number>123456</doc-number>
          </document-id>
        </root>"""

        result = extract_doc_numbers(xml)
        assert result == ["123456"]

    def test_empty_doc_number(self):
        """Test that empty doc-number elements are filtered out."""
        xml = """<root>
          <document-id format="epo">
            <doc-number></doc-number>
          </document-id>
          <document-id format="epo">
            <doc-number>123456</doc-number>
          </document-id>
        </root>"""

        result = extract_doc_numbers(xml)
        assert result == ["123456"]
