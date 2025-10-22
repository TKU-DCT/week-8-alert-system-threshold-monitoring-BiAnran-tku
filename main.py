import psutil
from datetime import datetime
import sqlite3
import os
import time
import subprocess
import platform

DB_NAME = "log.db"

# Define threshold values
CPU_THRESHOLD = 80.0
MEM_THRESHOLD = 85.0
DISK_THRESHOLD = 90.0

def get_system_info():
    # TODO: Collect system info (timestamp, cpu, memory, disk, ping)
    pass

def ping_host(host):
    # TODO: Ping 8.8.8.8 and return ("UP", ms) or ("DOWN", -1)
    pass

def parse_ping_time(output):
    # TODO: Extract ping response time from command output
    pass

def insert_log(data):
    # TODO: Insert log data into SQLite (reuse Week 7 function)
    pass

def check_alerts(cpu, memory, disk):
    # TODO: Print alert messages if any value exceeds its threshold
    pass

if __name__ == "__main__":
    # TODO: Initialize and log 5 records (every 10 seconds)
    # For each record, call check_alerts()
    pass
