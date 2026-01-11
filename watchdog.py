# watchdog.py - Monitor and restart critical processes

import subprocess
import time
import os
from pathlib import Path
import logging

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('Watchdog')

PROCESSES = {
    'orchestrator': 'python orchestrator.py',
    'gmail_watcher': 'python watchers/gmail_watcher.py',
    'file_watcher': 'python watchers/filesystem_watcher.py'
}

def is_process_running(pid_file):
    if not pid_file.exists():
        return False
    try:
        pid = int(pid_file.read_text().strip())
        # Check if process exists (Windows specific check could be added if needed, 
        # but os.kill(pid, 0) works on Unix/Mac. Windows might need psutil or tasklist)
        try:
            os.kill(pid, 0)
        except OSError:
            return False
        return True
    except (ValueError, ProcessLookupError):
        return False

def check_and_restart():
    # Use system temp dir for pid files
    tmp_dir = Path(os.getenv('TEMP', '/tmp'))
    
    for name, cmd in PROCESSES.items():
        pid_file = tmp_dir / f'{name}.pid'
        
        if not is_process_running(pid_file):
            logger.warning(f'{name} not running, restarting...')
            # Use shell=True for simple command string execution, but ideally list is safer
            proc = subprocess.Popen(cmd.split(), shell=True) 
            pid_file.write_text(str(proc.pid))
            logger.info(f'{name} started with PID {proc.pid}')

if __name__ == "__main__":
    logger.info("Starting Watchdog...")
    while True:
        check_and_restart()
        time.sleep(60)
