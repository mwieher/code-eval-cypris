"""XML Attribute Extraction Package.

This package provides functionality to extract doc-number values from patent XML
documents with priority-based ordering.
"""

from .exceptions import ExtractionError, InvalidDocumentError, XMLParseError
from .extractor import extract_doc_numbers

__version__ = "0.1.0"
__all__ = ["extract_doc_numbers", "ExtractionError", "XMLParseError", "InvalidDocumentError"]
