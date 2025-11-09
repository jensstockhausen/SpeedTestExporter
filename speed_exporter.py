#!/usr/bin/env python3
"""
Speed Exporter Script
"""
import subprocess
import os
import logging
from datetime import datetime


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


def run_speedtest(interface: str = "en0") -> str:
    """
    Run speedtest CLI application and save output to file.
    
    Args:
        interface: Network interface to test (default: en0)
        
    Returns:
        Path to the output file
    """
    logging.info(f"Starting speedtest on interface: {interface}")
    
    # Create speedtestraw directory if it doesn't exist
    output_dir = "speedtestraw"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate output filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"speedtest_{timestamp}.json")
    
    # Run speedtest command
    cmd = ["speedtest", "-p", "no", "-f", "json-pretty", "-I", interface]
    logging.info(f"Running command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # Write stdout to file
        with open(output_file, "w") as f:
            f.write(result.stdout)
        
        logging.info(f"Speedtest results saved to: {output_file}")
        return output_file
        
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running speedtest: {e}")
        if e.stderr:
            logging.error(f"Error output: {e.stderr}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise


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
