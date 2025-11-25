"""
Shared dependencies for API endpoints.
"""

import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def get_logger():
    """
    Dependency to get logger instance.
    """
    return logger
