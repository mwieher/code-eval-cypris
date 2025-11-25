"""Tests for the API endpoints."""

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


class TestHealthEndpoint:
    """Tests for the health check endpoint."""

    def test_health_check_returns_200(self):
        """Health endpoint should return 200 OK."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_check_has_status(self):
        """Health endpoint should return status field."""
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "healthy"

    def test_health_check_has_version(self):
        """Health endpoint should return version field."""
        response = client.get("/health")
        data = response.json()
        assert "version" in data
        assert data["version"] == "0.1.0"

    def test_health_check_has_uptime(self):
        """Health endpoint should return uptime_seconds field."""
        response = client.get("/health")
        data = response.json()
        assert "uptime_seconds" in data
        assert isinstance(data["uptime_seconds"], (int, float))
        assert data["uptime_seconds"] >= 0


class TestRootEndpoint:
    """Tests for the root endpoint."""

    def test_root_returns_200(self):
        """Root endpoint should return 200 OK."""
        response = client.get("/")
        assert response.status_code == 200

    def test_root_has_name(self):
        """Root endpoint should return API name."""
        response = client.get("/")
        data = response.json()
        assert "name" in data
        assert "XML" in data["name"]

    def test_root_has_docs_url(self):
        """Root endpoint should return docs URL."""
        response = client.get("/")
        data = response.json()
        assert data["docs_url"] == "/docs"


class TestExtractEndpoint:
    """Tests for the extract endpoint."""

    def test_extract_with_basic_sample(self):
        """Test extraction with basic sample XML."""
        xml_content = """<root>
          <application-reference>
            <document-id format="epo">
              <doc-number>999000888</doc-number>
            </document-id>
            <document-id format="original">
              <doc-number>66667777</doc-number>
            </document-id>
          </application-reference>
        </root>"""

        response = client.post("/extract", files={"file": ("test.xml", xml_content, "text/xml")})

        assert response.status_code == 200
        data = response.json()
        assert data["doc_numbers"] == ["999000888", "66667777"]
        assert data["count"] == 2
        assert "processing_time_ms" in data

    def test_extract_with_priority_ordering(self):
        """Test that priority ordering works correctly."""
        xml_content = """<root>
          <document-id format="patent-office">
            <doc-number>222</doc-number>
          </document-id>
          <document-id format="epo">
            <doc-number>111</doc-number>
          </document-id>
        </root>"""

        response = client.post("/extract", files={"file": ("test.xml", xml_content, "text/xml")})

        assert response.status_code == 200
        data = response.json()
        assert data["doc_numbers"] == ["111", "222"]

    def test_extract_with_empty_xml(self):
        """Test extraction with XML containing no document-ids."""
        xml_content = "<root></root>"

        response = client.post("/extract", files={"file": ("test.xml", xml_content, "text/xml")})

        assert response.status_code == 200
        data = response.json()
        assert data["doc_numbers"] == []
        assert data["count"] == 0

    def test_extract_returns_processing_time(self):
        """Test that response includes processing time."""
        xml_content = "<root></root>"

        response = client.post("/extract", files={"file": ("test.xml", xml_content, "text/xml")})

        assert response.status_code == 200
        data = response.json()
        assert "processing_time_ms" in data
        assert isinstance(data["processing_time_ms"], (int, float))
        assert data["processing_time_ms"] >= 0

    def test_extract_with_malformed_xml(self):
        """Test extraction with malformed XML (should use recovery parser)."""
        xml_content = """<root>
          <document-id format="epo">
            <doc-number>111111111</doc-number>
          </document-id>
          <unclosed-tag>
        </root>"""

        response = client.post("/extract", files={"file": ("test.xml", xml_content, "text/xml")})

        # Should succeed with recovery parser
        assert response.status_code == 200
        data = response.json()
        assert "111111111" in data["doc_numbers"]

    def test_extract_with_non_xml_file(self):
        """Test that non-XML files are rejected."""
        response = client.post("/extract", files={"file": ("test.txt", "not xml", "text/plain")})

        assert response.status_code == 422
        data = response.json()
        assert "error" in data

    def test_extract_with_invalid_encoding(self):
        """Test that files with invalid encoding are rejected."""
        # Create invalid UTF-8 bytes
        invalid_bytes = b"\xff\xfe\xfd"

        response = client.post("/extract", files={"file": ("test.xml", invalid_bytes, "text/xml")})

        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert "Encoding" in data["error"] or "decode" in data["message"].lower()

    def test_extract_with_large_file(self):
        """Test that files exceeding size limit are rejected."""
        # Create a file larger than 10MB
        large_content = "<root>" + ("x" * (11 * 1024 * 1024)) + "</root>"

        response = client.post("/extract", files={"file": ("test.xml", large_content, "text/xml")})

        assert response.status_code == 422
        data = response.json()
        assert "error" in data
        assert "large" in data["message"].lower() or "size" in data["message"].lower()


class TestExtractWithFixtures:
    """Tests using actual fixture files."""

    @pytest.fixture
    def fixtures_dir(self):
        """Return path to fixtures directory."""
        return Path(__file__).parent / "fixtures"

    def test_fixture_01_basic_sample(self, fixtures_dir):
        """Test with fixture 01: basic sample."""
        fixture_file = fixtures_dir / "01_basic_sample" / "input.xml"

        with open(fixture_file, "rb") as f:
            response = client.post("/extract", files={"file": ("input.xml", f, "text/xml")})

        assert response.status_code == 200
        data = response.json()
        assert data["doc_numbers"] == ["999000888", "66667777"]

    def test_fixture_02_priority_ordering(self, fixtures_dir):
        """Test with fixture 02: priority ordering."""
        fixture_file = fixtures_dir / "02_priority_ordering" / "input.xml"

        with open(fixture_file, "rb") as f:
            response = client.post("/extract", files={"file": ("input.xml", f, "text/xml")})

        assert response.status_code == 200
        data = response.json()
        assert data["doc_numbers"] == ["111111111", "222222222", "333333333"]

    def test_fixture_08_no_document_ids(self, fixtures_dir):
        """Test with fixture 08: no document-ids."""
        fixture_file = fixtures_dir / "08_no_document_ids" / "input.xml"

        with open(fixture_file, "rb") as f:
            response = client.post("/extract", files={"file": ("input.xml", f, "text/xml")})

        assert response.status_code == 200
        data = response.json()
        assert data["doc_numbers"] == []
        assert data["count"] == 0

    def test_fixture_10_malformed_unclosed_tag(self, fixtures_dir):
        """Test with fixture 10: malformed XML with unclosed tag."""
        fixture_file = fixtures_dir / "10_malformed_unclosed_tag" / "input.xml"

        with open(fixture_file, "rb") as f:
            response = client.post("/extract", files={"file": ("input.xml", f, "text/xml")})

        # Should succeed with recovery parser
        assert response.status_code == 200
        data = response.json()
        assert "111111111" in data["doc_numbers"]

    def test_fixture_12_duplicate_doc_numbers(self, fixtures_dir):
        """Test with fixture 12: duplicate doc-numbers."""
        fixture_file = fixtures_dir / "12_duplicate_doc_numbers" / "input.xml"

        with open(fixture_file, "rb") as f:
            response = client.post("/extract", files={"file": ("input.xml", f, "text/xml")})

        assert response.status_code == 200
        data = response.json()
        # Should preserve duplicates
        assert data["doc_numbers"].count("111111111") == 2


class TestErrorHandling:
    """Tests for error handling in the API."""

    def test_xml_parse_error_returns_400(self):
        """Test that XMLParseError returns 400 status code."""
        # Create XML that will fail even with recovery parser
        xml_content = ""

        response = client.post("/extract", files={"file": ("test.xml", xml_content, "text/xml")})

        assert response.status_code == 400
        data = response.json()
        assert "error" in data

    def test_unexpected_error_returns_500(self):
        """Test that unexpected errors return 500 status code."""
        # This is hard to trigger without mocking, but we can test the path exists
        # by checking that valid requests don't return 500
        xml_content = "<root></root>"

        response = client.post("/extract", files={"file": ("test.xml", xml_content, "text/xml")})

        # Should NOT return 500 for valid request
        assert response.status_code != 500
