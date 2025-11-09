#!/usr/bin/env python3
"""
Speed Exporter Script
"""
import os
import logging
from datetime import datetime
from speedtestexecuter import run_speedtest


def setup_logging():
    """Configure logging to file and console."""
    # Create log directory if it doesn't exist
    log_dir = "log"
    os.makedirs(log_dir, exist_ok=True)
    
    # Generate log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"speedtest_{timestamp}.log")
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    logging.info(f"Logging initialized. Log file: {log_file}")


def main():
    """Main function for speed exporter."""
    setup_logging()
    logging.info("Speed exporter starting...")
    
    try:
        run_speedtest()
        logging.info("Speed exporter completed successfully")
    except Exception as e:
        logging.error(f"Speed exporter failed: {e}")
        raise


if __name__ == "__main__":
    main()
