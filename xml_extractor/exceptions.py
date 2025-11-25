"""Custom exceptions for XML extraction."""


class ExtractionError(Exception):
    """Base exception for extraction-related errors."""

    pass


class XMLParseError(ExtractionError):
    """Raised when XML cannot be parsed."""

    pass


class InvalidDocumentError(ExtractionError):
    """Raised when document structure is unexpected."""

    pass
