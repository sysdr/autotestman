#!/usr/bin/env python3
"""
Centralized Logging Configuration for UQAP Framework
This module should be imported by all test modules
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

class LoggerFactory:
    """
    Factory class for creating configured loggers across the framework.
    Implements the Singleton pattern for consistent logging configuration.
    """
    
    _instance: Optional['LoggerFactory'] = None
    _initialized: bool = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not LoggerFactory._initialized:
            self._setup_logging_infrastructure()
            LoggerFactory._initialized = True
    
    def _setup_logging_infrastructure(self) -> None:
        """Setup the base logging infrastructure"""
        # Create logs directory
        self.log_dir = Path("logs")
        self.log_dir.mkdir(exist_ok=True)
        
        # Generate session log filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.session_log = self.log_dir / f"session_{timestamp}.log"
        
        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
    
    def get_logger(self, name: str, level: int = logging.INFO) -> logging.Logger:
        """
        Get or create a configured logger for a specific module.
        
        Args:
            name: Logger name (typically __name__)
            level: Minimum log level for console output
        
        Returns:
            Configured logger instance
        """
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        
        # Clear existing handlers to avoid duplicates
        logger.handlers.clear()
        
        # Console Handler - User-facing output
        console = logging.StreamHandler(sys.stdout)
        console.setLevel(level)
        console_fmt = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%H:%M:%S'
        )
        console.setFormatter(console_fmt)
        
        # File Handler - Complete debug information
        file_handler = logging.FileHandler(self.session_log)
        file_handler.setLevel(logging.DEBUG)
        file_fmt = logging.Formatter(
            '%(asctime)s | %(name)-25s | %(levelname)-8s | %(funcName)-20s:%(lineno)-4d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_fmt)
        
        logger.addHandler(console)
        logger.addHandler(file_handler)
        
        return logger

# Convenience function for quick logger creation
def get_logger(name: str = __name__, level: int = logging.INFO) -> logging.Logger:
    """
    Quick access to configured logger.
    Usage: logger = get_logger(__name__)
    """
    factory = LoggerFactory()
    return factory.get_logger(name, level)
