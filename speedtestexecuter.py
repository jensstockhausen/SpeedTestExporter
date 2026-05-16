#!/usr/bin/env python3
"""
Speedtest Executer Module
"""
import subprocess
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def run_speedtest(interface: str = "en0") -> str:
    """
    Run speedtest CLI application and save output to file.
    
    Args:
        interface: Network interface to test (default: en0)
        
    Returns:
        Path to the output file
    """
    logger.info("Starting speedtest on interface: %s", interface)
    
    # Create speedtestraw directory if it doesn't exist
    output_dir = "speedtestraw"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate output filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"speedtest_{timestamp}.json")
    
    # Run speedtest command
    cmd = ["speedtest", "--accept-gdpr", "-p", "no", "-f", "json-pretty", "-I", interface]
    logger.info("Running command: %s", ' '.join(cmd))
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        logger.debug("Speedtest stdout (%d bytes): %.200s", len(result.stdout), result.stdout)

        # Write stdout to file
        with open(output_file, "w") as f:
            f.write(result.stdout)
        
        logger.info("Speedtest results saved to: %s", output_file)
        return output_file
        
    except subprocess.CalledProcessError as e:
        logger.error("Error running speedtest: %s", e, exc_info=True)
        if e.stderr:
            logger.error("Error output: %s", e.stderr)
        raise
    except Exception as e:
        logger.error("Unexpected error: %s", e, exc_info=True)
        raise
