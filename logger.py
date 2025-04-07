# Singleton Pattern: Logger class provides a single logging instance across the application

import logging

def setup_logger():
    """
    Configures the logging system to write logs to a file with timestamps and levels.
    This helps with debugging and tracking issues.
    """
    logging.basicConfig(
        filename="app.log",             # Log file name
        level=logging.INFO,             # Log level: INFO and above
        format="%(asctime)s - %(levelname)s - %(message)s"  # Log message format
    )