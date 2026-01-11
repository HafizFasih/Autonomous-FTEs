# type: ignore
import time
import shutil
import os
import argparse
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class DropFolderHandler(FileSystemEventHandler):
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.inbox = self.vault_path / 'Inbox'
        self.needs_action = self.vault_path / 'Needs_Action'
        
        # Ensure directories exist
        self.inbox.mkdir(exist_ok=True)
        self.needs_action.mkdir(exist_ok=True)
        
    def on_created(self, event):
        # Ignore directories
        if event.is_directory:
            return
            
        source = Path(event.src_path)
        
        # Only process files inside Inbox
        if self.inbox not in source.parents:
            return

        print(f"New file detected: {source.name}")
        
        # Define destination path
        dest = self.needs_action / f'FILE_{source.name}'
        
        # Brief pause to ensure file write is complete
        time.sleep(1)
        
        try:
            # Move the file
            shutil.move(str(source), str(dest))
            print(f"Moved to: {dest}")
            
            # Create Metadata file for Claude
            self.create_metadata(source, dest)
            
        except Exception as e:
            print(f"Error moving file: {e}")

    def create_metadata(self, source, dest):
        meta_path = dest.with_suffix('.md')
        content = f"""---
type: file_drop
original_name: {source.name}
status: pending
timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}
---
# New File Dropped
The user dropped a file named `{source.name}`.
Please analyze this file or the user's request associated with it.
"""
        meta_path.write_text(content)
        print(f"Created metadata: {meta_path.name}")

def main():
    parser = argparse.ArgumentParser(description='Filesystem Watcher for Autonomous FTE')
    parser.add_argument(
        '--vault-path',
        default=os.getenv('VAULT_PATH', 'Vault'),
        help='Path to Obsidian vault (default: Vault directory or VAULT_PATH env var)'
    )
    args = parser.parse_args()
    
    vault_path = Path(args.vault_path).resolve()
    print(f"Monitoring Vault at: {vault_path}")

    event_handler = DropFolderHandler(vault_path)
    observer = Observer()
    
    # Watch the Inbox folder specifically
    inbox_path = vault_path / 'Inbox'
    inbox_path.mkdir(exist_ok=True)
    
    observer.schedule(event_handler, path=str(inbox_path), recursive=False)
    
    print(f"Watcher running on {inbox_path}...")
    print("Press Ctrl+C to stop.")
    
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
