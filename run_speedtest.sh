#!/bin/bash
#
# Speed Test Cron Script
# 
# This script runs the speed_exporter.py script and can be executed by cron.
#
# To add this to your crontab to run every 30 minutes:
# 1. Make this script executable: chmod +x run_speedtest.sh
# 2. Edit your crontab: crontab -e
# 3. Add the following line (adjust path as needed):
#
#    */30 * * * * /home/name/speedtest/run_speedtest.sh >> /Users/jens/Develop/speedtest/log/cron.log 2>&1
#
# Alternative: Run at specific minutes (0 and 30 of each hour):
#    0,30 * * * * /home/user/speedtest/run_speedtest.sh >> /Users/jens/Develop/speedtest/log/cron.log 2>&1
#
# Cron syntax explanation:
# */30 * * * * means: every 30 minutes
# │    │ │ │ │
# │    │ │ │ └─── day of week (0-7, Sunday=0 or 7)
# │    │ │ └───── month (1-12)
# │    │ └─────── day of month (1-31)
# │    └───────── hour (0-23)
# └────────────── minute (0-59)

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the script directory
cd "$SCRIPT_DIR"

# Activate virtual environment
source .venv/bin/activate

# Run the speed exporter
python3 speed_exporter.py

# Deactivate virtual environment
deactivate

# Exit with the status of the python script
exit $?
