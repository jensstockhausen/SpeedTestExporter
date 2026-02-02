#!/usr/bin/env python3
"""
Speedtest Executer Module
"""
import subprocess
import os
import logging
from datetime import datetime


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
    cmd = ["speedtest", "--accept-gdpr", "-p", "no", "-f", "json-pretty", "-I", interface]
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
