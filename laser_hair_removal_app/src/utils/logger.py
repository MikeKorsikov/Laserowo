import logging
from pathlib import Path
from datetime import datetime
import os
from typing import Optional

class Logger:
    """Manages logging setup and operations for the application."""
    
    def __init__(self, log_dir: str = "data/logs", log_level: str = "INFO"):
        """Initialize logger with directory and log level."""
        self.log_dir = Path(log_dir)
        self.log_level = getattr(logging, log_level.upper(), logging.INFO)
        self._setup_logging()
    
    def _setup_logging(self) -> None:
        """Set up logging to file and console."""
        # Ensure log directory exists
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate log file name with timestamp
        log_filename = self.log_dir / f"app_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        # Configure logger
        logger = logging.getLogger('LaserApp')
        logger.setLevel(self.log_level)
        
        # File handler
        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(self.log_level)
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.log_level)
        console_formatter = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        # Prevent duplicate logging if already configured
        if not logger.handlers:
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)
        
        self.logger = logger
    
    def get_logger(self) -> logging.Logger:
        """Return the configured logger instance."""
        return self.logger
    
    def rotate_log(self) -> None:
        """Rotate log file by creating a new file with a timestamp."""
        self._setup_logging()
        self.logger.info("Log file rotated")

if __name__ == "__main__":
    logger = Logger(log_level="DEBUG")
    log = logger.get_logger()
    try:
        log.debug("This is a debug message")
        log.info("This is an info message")
        log.warning("This is a warning message")
        log.error("This is an error message")
        logger.rotate_log()
        log.info("Log rotated, new message")
    except Exception as e:
        log.error(f"Error in logger test: {e}")