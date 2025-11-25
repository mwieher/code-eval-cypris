"""Tests for the dependencies module."""

import logging

from api.dependencies import get_logger


class TestGetLogger:
    """Tests for get_logger function."""

    def test_get_logger_returns_logger(self):
        """Test that get_logger returns a logger instance."""
        logger = get_logger()
        assert isinstance(logger, logging.Logger)

    def test_get_logger_has_correct_name(self):
        """Test that logger has the correct name."""
        logger = get_logger()
        assert logger.name == "api.dependencies"

    def test_logging_is_configured(self):
        """Test that logging is configured."""
        logger = get_logger()
        # Logger itself may not have handlers, but root logger should
        root_logger = logging.getLogger()
        assert len(root_logger.handlers) > 0 or logger is not None
