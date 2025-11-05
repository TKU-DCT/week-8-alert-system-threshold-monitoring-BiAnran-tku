# import psutil
# from datetime import datetime
# import sqlite3
# import os
# import time
# import subprocess
# import platform

# DB_NAME = "log.db"

# # Define threshold values
# CPU_THRESHOLD = 80.0
# MEM_THRESHOLD = 85.0
# DISK_THRESHOLD = 90.0

# def get_system_info():
#     # TODO: Collect system info (timestamp, cpu, memory, disk, ping)
#     pass

# def ping_host(host):
#     # TODO: Ping 8.8.8.8 and return ("UP", ms) or ("DOWN", -1)
#     pass

# def parse_ping_time(output):
#     # TODO: Extract ping response time from command output
#     pass

# def insert_log(data):
#     # TODO: Insert log data into SQLite (reuse Week 7 function)
#     pass

# def check_alerts(cpu, memory, disk):
#     # TODO: Print alert messages if any value exceeds its threshold
#     pass

# if __name__ == "__main__":
#     # TODO: Initialize and log 5 records (every 10 seconds)
#     # For each record, call check_alerts()
#     pass

import psutil
from datetime import datetime
import sqlite3
import os
import time
import subprocess
import platform
import re

# --- Bonus: Import for color and sound ---
import colorama
from colorama import Fore, Style
try:
    import winsound
    SOUND_AVAILABLE = True
except ImportError:
    SOUND_AVAILABLE = False # winsound is only available on Windows

# Initialize colorama
colorama.init()

DB_NAME = "log.db"

# Define threshold values
CPU_THRESHOLD = 80.0
MEM_THRESHOLD = 85.0
DISK_THRESHOLD = 90.0

# --- Bonus: Define colors for different alert types ---
ALERT_COLORS = {
    'CPU': Fore.YELLOW,
    'Memory': Fore.MAGENTA,
    'Disk': Fore.RED
}

# --- SET TO True TO USE FAKE HIGH-USAGE DATA FOR TESTING ---
# --- SET TO False TO USE REAL SYSTEM DATA ---
USE_SIMULATED_DATA = True

def setup_database():
    """Create both system_logs and alerts_log tables if they don't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS system_logs (
        timestamp TEXT,
        cpu_percent REAL,
        memory_percent REAL,
        disk_percent REAL,
        ping_status TEXT,
        ping_time REAL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS alerts_log (
        timestamp TEXT,
        alert_type TEXT,
        current_value REAL,
        threshold_value REAL
    )
    ''')
    
    conn.commit()
    conn.close()

def get_system_info():
    """Collect system info (timestamp, cpu, memory, disk, ping)."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    memory_percent = memory.percent
    disk = psutil.disk_usage('/')
    disk_percent = (disk.used / disk.total) * 100
    ping_status, ping_time = ping_host("8.8.8.8")
    
    return (timestamp, cpu_percent, memory_percent, disk_percent, ping_status, ping_time)

# --- NEW FUNCTION FOR SIMULATION ---
def get_simulated_system_info():
    """
    Returns fake system data that is guaranteed to trigger all alerts.
    Use this for testing the alert functionality.
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # These values are set above the thresholds to force alerts
    cpu_percent = 95.5  # > 80
    memory_percent = 90.2 # > 85
    disk_percent = 95.1  # > 90
    ping_status, ping_time = ("UP", 23.1)
    
    return (timestamp, cpu_percent, memory_percent, disk_percent, ping_status, ping_time)

def ping_host(host):
    """Ping a host and return ("UP", ms) or ("DOWN", -1)."""
    try:
        command = ["ping", "-n", "1", host] if platform.system().lower() == "windows" else ["ping", "-c", "1", host]
        output = subprocess.check_output(command, universal_newlines=True, stderr=subprocess.STDOUT)
        ping_time = parse_ping_time(output)
        return ("UP", ping_time) if ping_time > 0 else ("DOWN", -1)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ("DOWN", -1)

def parse_ping_time(output):
    """Extract ping response time from command output."""
    try:
        pattern = r"Time[=<](\d+)ms" if platform.system().lower() == "windows" else r"time[=<](\d+\.?\d*)"
        match = re.search(pattern, output)
        return float(match.group(1)) if match else -1
    except Exception:
        return -1

def insert_log(data):
    """Insert system log data into SQLite."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO system_logs VALUES (?, ?, ?, ?, ?, ?)', data)
    conn.commit()
    conn.close()

def insert_alert_log(alert_data):
    """Insert a single alert into the alerts_log table."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO alerts_log VALUES (?, ?, ?, ?)', alert_data)
    conn.commit()
    conn.close()

def play_alert_sound():
    """Plays a beep sound if the winsound library is available (Windows)."""
    if SOUND_AVAILABLE:
        try:
            winsound.Beep(1000, 500)
        except RuntimeError:
            pass

def check_alerts(cpu, memory, disk):
    """
    Checks thresholds and returns a list of triggered alerts.
    Each alert is a dictionary with its details.
    """
    alerts = []
    if cpu > CPU_THRESHOLD:
        alerts.append({
            "type": "CPU",
            "value": cpu,
            "threshold": CPU_THRESHOLD
        })
    if memory > MEM_THRESHOLD:
        alerts.append({
            "type": "Memory",
            "value": memory,
            "threshold": MEM_THRESHOLD
        })
    if disk > DISK_THRESHOLD:
        alerts.append({
            "type": "Disk",
            "value": disk,
            "threshold": DISK_THRESHOLD
        })
    return alerts

if __name__ == "__main__":
    setup_database()
    
    mode = "SIMULATION" if USE_SIMULATED_DATA else "LIVE"
    print(f"Starting system monitor in {mode} mode...")
    print(f"Thresholds -> CPU: {CPU_THRESHOLD}%, Memory: {MEM_THRESHOLD}%, Disk: {DISK_THRESHOLD}%")
    print("-" * 50)

    for i in range(5):
        # --- CHOOSE WHICH DATA SOURCE TO USE ---
        if USE_SIMULATED_DATA:
            system_info = get_simulated_system_info()
        else:
            system_info = get_system_info()
        
        insert_log(system_info)
        
        print(f"Logged: {system_info}", end=" ")
        
        triggered_alerts = check_alerts(system_info[1], system_info[2], system_info[3])
        
        if triggered_alerts:
            play_alert_sound()
            
            for alert in triggered_alerts:
                alert_log_entry = (
                    system_info[0],
                    alert['type'],
                    alert['value'],
                    alert['threshold']
                )
                insert_alert_log(alert_log_entry)
                
                color = ALERT_COLORS.get(alert['type'], Fore.WHITE)
                alert_message = f"⚠️ ALERT: High {alert['type']} usage! ({alert['value']}%)"
                print(f"{color}{alert_message}{Style.RESET_ALL}", end=" ")
        
        print()
        
        if i < 4:
            time.sleep(10)
