#!/usr/bin/env python3
"""
Speed Exporter Script
"""
import os
import logging
from logging.handlers import RotatingFileHandler
from speedtestexecuter import run_speedtest
from dotenv import load_dotenv
from extractmetrics import process_all_json_files

logger = logging.getLogger(__name__)


def setup_logging():
    """Configure logging to file (with rotation) and console.

    Log level is controlled by the LOG_LEVEL environment variable (default: INFO).
    """
    log_dir = "log"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "speedtest.log")

    log_level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_name, logging.INFO)

    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Rotating file: 5 MB per file, keep 5 backups
    file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=5)
    file_handler.setFormatter(logging.Formatter(log_format))

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(log_format))

    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    logger.info("Logging initialized. Log file: %s (level=%s)", log_file, log_level_name)


def main():
    """Main function for speed exporter."""
    setup_logging()
    logger.info("Speed exporter starting...")
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Get interfaces from environment variable
    interfaces_str = os.getenv('INTERFACES', 'en0')
    interfaces = [iface.strip() for iface in interfaces_str.split(',')]
    
    logger.info("Testing interfaces: %s", interfaces)
    
    try:
        # Delete all files in speedtestraw
        if os.path.exists("speedtestraw"):
            for f in os.listdir("speedtestraw"):
                os.remove(os.path.join("speedtestraw", f))

        # Run speedtest for each interface
        for interface in interfaces:
            logger.info("Running speedtest for interface: %s", interface)
            run_speedtest(interface)
        
        logger.info("Speed exporter completed successfully")

        # Delete all files in speedtestmetrics
        if os.path.exists("speedtestmetrics"):
            for f in os.listdir("speedtestmetrics"):
                os.remove(os.path.join("speedtestmetrics", f))

        # Process all JSON files to generate metrics
        process_all_json_files()
        logger.info("Metrics extraction completed successfully")

    except Exception as e:
        logger.error("Speed exporter failed: %s", e, exc_info=True)
        raise


if __name__ == "__main__":
    main()
