#!/usr/bin/env python3
"""
Extract Metrics Module - Converts speedtest JSON to Prometheus metrics
"""
import json
import os
import logging
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)


def parse_speedtest_json(json_file: str) -> Dict[str, Any]:
    """
    Parse speedtest JSON file and extract relevant metrics.
    
    Args:
        json_file: Path to the JSON file
        
    Returns:
        Dictionary containing extracted metrics
    """
    logger.info("Parsing JSON file: %s", json_file)
    
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        metrics = {
            'download_bandwidth': data.get('download', {}).get('bandwidth', 0),
            'download_bytes': data.get('download', {}).get('bytes', 0),
            'upload_bandwidth': data.get('upload', {}).get('bandwidth', 0),
            'upload_bytes': data.get('upload', {}).get('bytes', 0),
            'ping_latency': data.get('ping', {}).get('latency', 0),
            'ping_jitter': data.get('ping', {}).get('jitter', 0),
            'packet_loss': data.get('packetLoss', 0),

            'isp': data.get('isp', 'unknown'),
            'interface': data.get('interface', {}).get('name', 'unknown'),
            'server_name': data.get('server', {}).get('name', 'unknown'),
            'server_location': data.get('server', {}).get('location', 'unknown'),
            
            'timestamp': data.get('timestamp', datetime.now().isoformat())
        }
        
        logger.info(
            "Extracted metrics: download=%s, upload=%s",
            metrics['download_bandwidth'], metrics['upload_bandwidth']
        )
        logger.debug(
            "Full metrics: ping_latency=%s, ping_jitter=%s, packet_loss=%s, isp=%s, interface=%s",
            metrics['ping_latency'], metrics['ping_jitter'], metrics['packet_loss'],
            metrics['isp'], metrics['interface']
        )
        return metrics
        
    except json.JSONDecodeError as e:
        logger.error("Error parsing JSON file %s: %s", json_file, e, exc_info=True)
        raise
    except Exception as e:
        logger.error("Unexpected error reading %s: %s", json_file, e, exc_info=True)
        raise


def convert_to_prometheus(metrics: Dict[str, Any], output_file: str):
    """
    Convert metrics to Prometheus format and write to file.
    
    Args:
        metrics: Dictionary containing metrics
        output_file: Path to output file
    """
    logger.info("Converting metrics to Prometheus format")
    
    # Create Prometheus metrics content
    prometheus_metrics = []
    
    # Download bandwidth (convert to bits per second if needed)
    prometheus_metrics.append(f"# HELP speedtest_download_bandwidth_bps Download bandwidth in bits per second")
    prometheus_metrics.append(f"# TYPE speedtest_download_bandwidth_bps gauge")
    prometheus_metrics.append(f'speedtest_download_bandwidth_bps{{isp="{metrics["isp"]}",interface="{metrics["interface"]}",server="{metrics["server_name"]}"}} {metrics["download_bandwidth"]}')
    
    # Upload bandwidth
    prometheus_metrics.append(f"# HELP speedtest_upload_bandwidth_bps Upload bandwidth in bits per second")
    prometheus_metrics.append(f"# TYPE speedtest_upload_bandwidth_bps gauge")
    prometheus_metrics.append(f'speedtest_upload_bandwidth_bps{{isp="{metrics["isp"]}",interface="{metrics["interface"]}",server="{metrics["server_name"]}"}} {metrics["upload_bandwidth"]}')
    
    # Ping latency
    prometheus_metrics.append(f"# HELP speedtest_ping_latency_ms Ping latency in milliseconds")
    prometheus_metrics.append(f"# TYPE speedtest_ping_latency_ms gauge")
    prometheus_metrics.append(f'speedtest_ping_latency_ms{{isp="{metrics["isp"]}",interface="{metrics["interface"]}",server="{metrics["server_name"]}"}} {metrics["ping_latency"]}')
    
    # Ping jitter
    prometheus_metrics.append(f"# HELP speedtest_ping_jitter_ms Ping jitter in milliseconds")
    prometheus_metrics.append(f"# TYPE speedtest_ping_jitter_ms gauge")
    prometheus_metrics.append(f'speedtest_ping_jitter_ms{{isp="{metrics["isp"]}",interface="{metrics["interface"]}",server="{metrics["server_name"]}"}} {metrics["ping_jitter"]}')
    
    # Packet loss
    prometheus_metrics.append(f"# HELP speedtest_packet_loss_percent Packet loss percentage")
    prometheus_metrics.append(f"# TYPE speedtest_packet_loss_percent gauge")
    prometheus_metrics.append(f'speedtest_packet_loss_percent{{isp="{metrics["isp"]}",interface="{metrics["interface"]}",server="{metrics["server_name"]}"}} {metrics["packet_loss"]}')
    
    # Download bytes
    prometheus_metrics.append(f"# HELP speedtest_download_bytes_total Total bytes downloaded")
    prometheus_metrics.append(f"# TYPE speedtest_download_bytes_total counter")
    prometheus_metrics.append(f'speedtest_download_bytes_total{{isp="{metrics["isp"]}",interface="{metrics["interface"]}",server="{metrics["server_name"]}"}} {metrics["download_bytes"]}')
    
    # Upload bytes
    prometheus_metrics.append(f"# HELP speedtest_upload_bytes_total Total bytes uploaded")
    prometheus_metrics.append(f"# TYPE speedtest_upload_bytes_total counter")
    prometheus_metrics.append(f'speedtest_upload_bytes_total{{isp="{metrics["isp"]}",interface="{metrics["interface"]}",server="{metrics["server_name"]}"}} {metrics["upload_bytes"]}')
    
    # Write to file
    try:
        with open(output_file, 'w') as f:
            f.write('\n'.join(prometheus_metrics))
            f.write('\n')
        
        logger.info("Prometheus metrics written to: %s", output_file)
        
    except Exception as e:
        logger.error("Error writing Prometheus metrics to %s: %s", output_file, e, exc_info=True)
        raise


def extract_metrics(json_file: str) -> str:
    """
    Extract metrics from speedtest JSON file and convert to Prometheus format.
    
    Args:
        json_file: Path to the speedtest JSON file
        
    Returns:
        Path to the output Prometheus metrics file
    """
    # Create speedtestmetrics directory if it doesn't exist
    output_dir = "speedtestmetrics"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate output filename based on input filename
    base_name = os.path.basename(json_file)
    output_name = base_name.replace('.json', '.prom')
    output_file = os.path.join(output_dir, output_name)
    
    # Parse JSON and extract metrics
    metrics = parse_speedtest_json(json_file)
    
    # Convert to Prometheus format
    convert_to_prometheus(metrics, output_file)
    
    return output_file


def process_all_json_files(input_dir: str = "speedtestraw") -> list:
    """
    Process all JSON files in the input directory.
    
    Args:
        input_dir: Directory containing speedtest JSON files
        
    Returns:
        List of output file paths
    """
    if not os.path.exists(input_dir):
        logger.warning("Input directory %s does not exist", input_dir)
        return []
    
    output_files = []
    json_files = [f for f in os.listdir(input_dir) if f.endswith('.json')]
    
    logger.info("Found %d JSON files to process", len(json_files))
    
    for json_file in json_files:
        full_path = os.path.join(input_dir, json_file)
        try:
            output_file = extract_metrics(full_path)
            output_files.append(output_file)
        except Exception as e:
            logger.error("Failed to process %s: %s", json_file, e)
            continue
    
    logger.info("Successfully processed %d files", len(output_files))
    return output_files


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    process_all_json_files()
