#!/usr/bin/env python3
"""
Speed Exporter Script
"""
import os
import logging
from datetime import datetime
from speedtestexecuter import run_speedtest
from dotenv import load_dotenv
from extractmetrics import process_all_json_files


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
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Get interfaces from environment variable
    interfaces_str = os.getenv('INTERFACES', 'en0')
    interfaces = [iface.strip() for iface in interfaces_str.split(',')]
    
    logging.info(f"Testing interfaces: {interfaces}")
    
    try:
        # Delete all files in speedtestraw
        if os.path.exists("speedtestraw"):
            for f in os.listdir("speedtestraw"):
                os.remove(os.path.join("speedtestraw", f))

        # Run speedtest for each interface
        for interface in interfaces:
            logging.info(f"Running speedtest for interface: {interface}")
            run_speedtest(interface)
        
        logging.info("Speed exporter completed successfully")

        # Delete all files in speedtestmetrics
        if os.path.exists("speedtestmetrics"):
            for f in os.listdir("speedtestmetrics"):
                os.remove(os.path.join("speedtestmetrics", f))

        # Process all JSON files to generate metrics
        process_all_json_files()
        logging.info("Metrics extraction completed successfully")

    except Exception as e:
        logging.error(f"Speed exporter failed: {e}")
        raise


if __name__ == "__main__":
    main()
