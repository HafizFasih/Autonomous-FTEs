import time
import logging
import os
from pathlib import Path

# Configuration
VAULT_PATH = os.getenv('VAULT_PATH', 'Vault')
CHECK_INTERVAL = 60

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Path(VAULT_PATH) / 'Logs' / 'orchestrator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('Orchestrator')

def check_needs_action():
    """Check /Needs_Action for new files to process."""
    needs_action_dir = Path(VAULT_PATH) / 'Needs_Action'
    if not needs_action_dir.exists():
        logger.warning(f"{needs_action_dir} does not exist.")
        return

    files = list(needs_action_dir.glob('*.md'))
    if files:
        logger.info(f"Found {len(files)} items in Needs_Action.")
        # Trigger Claude Logic here (Placeholder)
        # e.g. call_claude(files)
    else:
        logger.debug("No items in Needs_Action.")

def run():
    logger.info("Starting Orchestrator...")
    while True:
        try:
            check_needs_action()
        except Exception as e:
            logger.error(f"Error in Orchestrator loop: {e}")
        
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    run()
