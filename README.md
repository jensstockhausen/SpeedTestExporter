# Speed Test Exporter

A Python-based tool that automates network speed testing and exports metrics in Prometheus format for monitoring and analysis.

## Features

- **Automated Speed Testing**: Runs speedtest CLI on configured network interfaces
- **Prometheus Metrics**: Converts speedtest results to Prometheus-compatible format
- **Multi-Interface Support**: Test multiple network interfaces simultaneously
- **Comprehensive Logging**: Detailed logs for monitoring and debugging
- **Cron Integration**: Easy setup for scheduled automated testing
- **Environment Configuration**: Flexible configuration via `.env` file

## Project Structure

```
speedtest/
├── speed_exporter.py       # Main orchestration script
├── speedtestexecuter.py    # Speedtest execution module
├── extractmetrics.py       # Prometheus metrics conversion
├── run_speedtest.sh        # Bash script for cron execution
├── requirements.txt        # Python dependencies
├── .env                    # Environment configuration
├── .gitignore             # Git ignore rules
├── speedtestraw/          # Raw JSON speedtest results
├── speedtestmetrics/      # Prometheus metrics output
└── log/                   # Application logs
```

## Prerequisites

- Python 3.7 or higher
- [Speedtest CLI](https://www.speedtest.net/apps/cli) installed and available in PATH
- Network interface(s) to test (e.g., en0, en1)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/jensstockhausen/SpeedTestExporter.git
cd SpeedTestExporter
```

2. Create and activate virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure interfaces in `.env`:
```bash
# Edit .env file
INTERFACES=en0,en1
```

## Usage

### Manual Execution

Run the speed exporter manually:
```bash
python3 speed_exporter.py
```

Or using the bash script:
```bash
./run_speedtest.sh
```

### Automated Execution with Cron

1. Make the script executable (if not already):
```bash
chmod +x run_speedtest.sh
```

2. Edit your crontab:
```bash
crontab -e
```

3. Add one of the following lines (adjust paths as needed):

Run every 30 minutes:
```cron
*/30 * * * * /Users/jens/Develop/speedtest/run_speedtest.sh >> /Users/jens/Develop/speedtest/log/cron.log 2>&1
```

Run at :00 and :30 of each hour:
```cron
0,30 * * * * /Users/jens/Develop/speedtest/run_speedtest.sh >> /Users/jens/Develop/speedtest/log/cron.log 2>&1
```

## Configuration

### Environment Variables (.env)

- `INTERFACES`: Comma-separated list of network interfaces to test (default: `en0`)

Example:
```bash
INTERFACES=en0,en1,en2
```

## Output

### Raw JSON Results
Speedtest results are saved as JSON files in `speedtestraw/` with timestamps:
- Format: `speedtest_YYYYMMDD_HHMMSS.json`

### Prometheus Metrics
Converted metrics are saved in `speedtestmetrics/` as `.prom` files with the following metrics:

- `speedtest_download_bandwidth_bps` - Download bandwidth in bits per second
- `speedtest_upload_bandwidth_bps` - Upload bandwidth in bits per second
- `speedtest_ping_latency_ms` - Ping latency in milliseconds
- `speedtest_ping_jitter_ms` - Ping jitter in milliseconds
- `speedtest_packet_loss_percent` - Packet loss percentage
- `speedtest_download_bytes_total` - Total bytes downloaded
- `speedtest_upload_bytes_total` - Total bytes uploaded

Each metric includes labels: `isp`, `interface`, and `server`.

### Logs
Application logs are stored in `log/` directory:
- Format: `speedtest_YYYYMMDD_HHMMSS.log`
- Includes timestamps, log levels, and detailed messages

## Modules

### speed_exporter.py
Main orchestration script that:
- Loads configuration from `.env`
- Sets up logging
- Runs speedtest for each configured interface
- Processes results into Prometheus metrics

### speedtestexecuter.py
Handles speedtest CLI execution:
- Runs speedtest command with specified interface
- Captures JSON output
- Saves raw results to `speedtestraw/`

### extractmetrics.py
Converts speedtest JSON to Prometheus format:
- Parses JSON results
- Extracts key metrics
- Generates Prometheus-compatible output
- Can process single files or batch process directory

## Dependencies

- `python-dotenv==1.0.0` - Environment variable management

## Development

### Code Style
- Follows PEP 8 style guidelines
- Uses type hints where appropriate
- Includes docstrings for functions and classes

### Testing
Run a test execution:
```bash
source .venv/bin/activate
python3 speed_exporter.py
```

Check the output in:
- `speedtestraw/` for JSON results
- `speedtestmetrics/` for Prometheus metrics
- `log/` for execution logs

## Troubleshooting

### Speedtest CLI not found
Ensure speedtest CLI is installed:
```bash
# macOS
brew install speedtest-cli
```

### Permission denied
If running speedtest requires sudo, you may need to configure passwordless sudo for the speedtest command or run the script with appropriate permissions.

### Interface not found
List available network interfaces:
```bash
networksetup -listallhardwareports
# or
ifconfig
```

Update `.env` with valid interface names.

## License

MIT License - feel free to use and modify as needed.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
