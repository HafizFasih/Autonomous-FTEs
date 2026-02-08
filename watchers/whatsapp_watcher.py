#!/usr/bin/env python3
"""
WhatsApp Watcher

Monitors WhatsApp Web for new messages and creates action files in /Needs_Action folder.
Uses Playwright for browser automation with WhatsApp Web.

First run requires scanning QR code to link WhatsApp.

Usage:
    python whatsapp_watcher.py
    python whatsapp_watcher.py --check-interval 60
    python whatsapp_watcher.py --no-headless

Author: Autonomous FTE System
"""

import os
import sys
import time
import logging
import json
from pathlib import Path
from datetime import datetime
from typing import Set, List, Dict, Any, Optional

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed.")

# Playwright for browser automation
try:
    from playwright.sync_api import sync_playwright, Browser, Page
except ImportError:
    print("Error: playwright not installed.")
    print("Install with: pip install playwright && playwright install chromium")
    sys.exit(1)


class WhatsAppWatcher:
    """Monitor WhatsApp Web for new messages using browser automation."""

    def __init__(
        self,
        vault_path: str,
        check_interval: int = 60,
        headless: bool = False,  # WhatsApp Web works better with visible browser
        dry_run: bool = False
    ):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.check_interval = check_interval
        self.headless = headless
        self.dry_run = dry_run

        # Session path from .env
        self.session_path = os.getenv('WHATSAPP_SESSION_PATH', './whatsapp_session')

        # Track processed messages
        self.processed_ids: Set[str] = set()
        self.processed_ids_file = self.vault_path / 'Logs' / 'whatsapp_processed_ids.json'

        # Browser instances
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.is_logged_in = False

        # Setup
        self._setup_logging()
        self._load_processed_ids()
        self._ensure_directories()

    def _setup_logging(self) -> None:
        log_dir = self.vault_path / 'Logs'
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / 'whatsapp_watcher.log'

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger('WhatsAppWatcher')

    def _ensure_directories(self) -> None:
        self.needs_action.mkdir(parents=True, exist_ok=True)
        (self.vault_path / 'Logs').mkdir(exist_ok=True)
        Path(self.session_path).mkdir(exist_ok=True)

    def _load_processed_ids(self) -> None:
        if self.processed_ids_file.exists():
            try:
                with open(self.processed_ids_file, 'r') as f:
                    data = json.load(f)
                    self.processed_ids = set(data.get('processed_ids', []))
                    self.logger.info(f"Loaded {len(self.processed_ids)} processed message IDs")
            except Exception as e:
                self.logger.warning(f"Could not load processed IDs: {e}")

    def _save_processed_ids(self) -> None:
        try:
            self.processed_ids_file.parent.mkdir(exist_ok=True)
            with open(self.processed_ids_file, 'w') as f:
                json.dump({
                    'processed_ids': list(self.processed_ids)[-1000:],  # Keep last 1000
                    'last_updated': datetime.now().isoformat(),
                    'count': len(self.processed_ids)
                }, f, indent=2)
        except Exception as e:
            self.logger.error(f"Could not save processed IDs: {e}")

    def connect(self) -> bool:
        """Launch browser and connect to WhatsApp Web."""
        try:
            self.logger.info("Launching browser...")
            self.playwright = sync_playwright().start()

            # Use persistent context to maintain WhatsApp session
            self.browser = self.playwright.chromium.launch_persistent_context(
                user_data_dir=self.session_path,
                headless=self.headless,
                viewport={'width': 1280, 'height': 900},
                args=['--disable-blink-features=AutomationControlled']
            )

            self.page = self.browser.pages[0] if self.browser.pages else self.browser.new_page()

            self.logger.info("Opening WhatsApp Web...")
            self.page.goto('https://web.whatsapp.com', timeout=120000)

            # Wait for either QR code or main chat interface
            self.logger.info("Waiting for WhatsApp to load...")

            # Check if already logged in or need QR scan
            max_wait = 120  # 2 minutes for QR scan
            waited = 0

            while waited < max_wait:
                # Check if main chat interface is loaded (logged in)
                chat_list = self.page.query_selector('div[aria-label="Chat list"]')
                side_panel = self.page.query_selector('#pane-side')

                if chat_list or side_panel:
                    self.logger.info("WhatsApp Web loaded - already logged in!")
                    self.is_logged_in = True
                    return True

                # Check if QR code is displayed
                qr_code = self.page.query_selector('canvas[aria-label="Scan this QR code to link a device!"]')
                qr_code_alt = self.page.query_selector('div[data-testid="qrcode"]')

                if qr_code or qr_code_alt:
                    self.logger.info("=" * 50)
                    self.logger.info("QR CODE DISPLAYED - Please scan with your phone!")
                    self.logger.info("Open WhatsApp on your phone > Settings > Linked Devices > Link a Device")
                    self.logger.info("=" * 50)

                    # Reset wait time for QR scanning
                    waited = 0
                    max_wait = 180  # 3 minutes for QR scan

                    # Wait for user to scan
                    while waited < max_wait:
                        time.sleep(5)
                        waited += 5

                        # Check if logged in now
                        chat_list = self.page.query_selector('div[aria-label="Chat list"]')
                        side_panel = self.page.query_selector('#pane-side')

                        if chat_list or side_panel:
                            self.logger.info("QR code scanned - logged in successfully!")
                            self.is_logged_in = True
                            return True

                        self.logger.info(f"Waiting for QR scan... ({waited}s / {max_wait}s)")

                    self.logger.error("Timeout waiting for QR scan")
                    return False

                time.sleep(2)
                waited += 2
                self.logger.info(f"Loading WhatsApp... ({waited}s)")

            self.logger.error("Timeout waiting for WhatsApp to load")
            return False

        except Exception as e:
            self.logger.error(f"Connection error: {e}")
            return False

    def disconnect(self) -> None:
        """Close browser."""
        try:
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
        except:
            pass
        self.browser = None
        self.page = None
        self.playwright = None

    def check_unread_messages(self) -> List[Dict[str, Any]]:
        """Check for unread messages in WhatsApp."""
        messages = []
        try:
            self.logger.info("Checking for unread messages...")

            # Find all chat items with unread indicators
            # WhatsApp uses a span with aria-label containing unread count
            unread_chats = self.page.query_selector_all('span[aria-label*="unread message"]')

            # Alternative selector for unread badges
            if not unread_chats:
                unread_chats = self.page.query_selector_all('div[class*="unread"]')

            self.logger.info(f"Found {len(unread_chats)} chats with unread messages")

            for badge in unread_chats[:10]:  # Limit to 10 chats
                try:
                    # Navigate up to find the chat container
                    chat_container = badge.evaluate_handle('''
                        el => {
                            let parent = el;
                            for (let i = 0; i < 10; i++) {
                                parent = parent.parentElement;
                                if (parent && parent.getAttribute('role') === 'listitem') {
                                    return parent;
                                }
                            }
                            return null;
                        }
                    ''')

                    if not chat_container:
                        continue

                    # Extract chat name
                    name_elem = chat_container.as_element().query_selector('span[title]')
                    chat_name = name_elem.get_attribute('title') if name_elem else 'Unknown'

                    # Extract last message preview
                    preview_elem = chat_container.as_element().query_selector('span[class*="message-text"]')
                    if not preview_elem:
                        preview_elem = chat_container.as_element().query_selector('div[class*="_21S-L"]')
                    preview = preview_elem.inner_text() if preview_elem else ''

                    # Extract time
                    time_elem = chat_container.as_element().query_selector('div[class*="time"]')
                    msg_time = time_elem.inner_text() if time_elem else ''

                    # Extract unread count
                    unread_count = '1'
                    count_match = badge.get_attribute('aria-label')
                    if count_match:
                        import re
                        numbers = re.findall(r'\d+', count_match)
                        if numbers:
                            unread_count = numbers[0]

                    # Generate unique ID
                    msg_id = f"wa_{hash(chat_name + preview[:30] + msg_time)}"

                    if msg_id in self.processed_ids:
                        continue

                    messages.append({
                        'id': msg_id,
                        'type': 'whatsapp_message',
                        'chat_name': chat_name.strip(),
                        'preview': preview.strip()[:200],
                        'time': msg_time.strip(),
                        'unread_count': unread_count,
                        'text': f"Message from {chat_name}: {preview[:100]}"
                    })

                except Exception as e:
                    self.logger.debug(f"Error parsing chat: {e}")
                    continue

            # Alternative method: look for chats with green badges
            if not messages:
                self.logger.info("Trying alternative method to find unread...")
                chat_items = self.page.query_selector_all('div[role="listitem"]')

                for item in chat_items[:20]:
                    try:
                        # Look for unread indicator (green circle with number)
                        unread_badge = item.query_selector('span[class*="unread"]')
                        if not unread_badge:
                            unread_badge = item.query_selector('span[aria-label*="unread"]')

                        if not unread_badge:
                            continue

                        # Get chat name
                        name_elem = item.query_selector('span[title]')
                        chat_name = name_elem.get_attribute('title') if name_elem else 'Unknown'

                        # Get preview text
                        spans = item.query_selector_all('span')
                        preview = ''
                        for span in spans:
                            text = span.inner_text()
                            if len(text) > 10 and text != chat_name:
                                preview = text
                                break

                        msg_id = f"wa_{hash(chat_name)}"

                        if msg_id in self.processed_ids:
                            continue

                        messages.append({
                            'id': msg_id,
                            'type': 'whatsapp_message',
                            'chat_name': chat_name.strip(),
                            'preview': preview.strip()[:200],
                            'time': '',
                            'unread_count': '1+',
                            'text': f"Unread message from {chat_name}"
                        })

                    except:
                        continue

            self.logger.info(f"Found {len(messages)} new unread conversations")

        except Exception as e:
            self.logger.error(f"Error checking messages: {e}")

        return messages

    def create_action_file(self, item: Dict[str, Any]) -> Optional[Path]:
        """Create action file for WhatsApp message."""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

            # Safe filename from chat name
            safe_name = "".join(c for c in item['chat_name'][:25] if c.isalnum() or c in ' -_').strip()
            safe_name = safe_name.replace(' ', '_') or 'chat'

            filename = f"WHATSAPP_{timestamp}_{safe_name}.md"
            filepath = self.needs_action / filename

            content = self._build_content(item)

            if not self.dry_run:
                filepath.write_text(content, encoding='utf-8')

            self.logger.info(f"Created: {filename}")

            self.processed_ids.add(item['id'])
            self._save_processed_ids()

            return filepath

        except Exception as e:
            self.logger.error(f"Error creating action file: {e}")
            return None

    def _build_content(self, item: Dict[str, Any]) -> str:
        """Build markdown content for action file."""
        content = f"""---
type: whatsapp_message
from: {item['chat_name']}
unread_count: {item['unread_count']}
received: {datetime.now().isoformat()}
status: pending
---

## WhatsApp Message from {item['chat_name']}

**From:** {item['chat_name']}
**Time:** {item.get('time', 'Unknown')}
**Unread:** {item['unread_count']} message(s)

---

## Preview

{item.get('preview', 'No preview available')}

---

## Suggested Actions

- [ ] Open WhatsApp and read full message
- [ ] Reply to sender
- [ ] Mark as handled

## Notes

- Open WhatsApp Web to view full conversation
- This is a preview only - full message content requires manual review

"""
        return content

    def run(self) -> None:
        """Run the watcher continuously."""
        self.logger.info("Starting WhatsApp Watcher")
        self.logger.info(f"  Session path: {self.session_path}")
        self.logger.info(f"  Check interval: {self.check_interval}s")
        self.logger.info(f"  Headless: {self.headless}")

        if self.dry_run:
            self.logger.info("DRY RUN MODE")

        if not self.connect():
            self.logger.error("Failed to connect. Exiting.")
            sys.exit(1)

        iteration = 0
        while True:
            try:
                iteration += 1
                self.logger.info(f"--- Check #{iteration} ---")

                # Refresh page periodically to ensure connection
                if iteration % 10 == 0:
                    self.logger.info("Refreshing connection...")
                    self.page.reload(timeout=60000)
                    time.sleep(5)

                # Check for unread messages
                messages = self.check_unread_messages()

                if messages:
                    self.logger.info(f"Processing {len(messages)} conversations...")
                    for msg in messages:
                        filepath = self.create_action_file(msg)
                        if filepath:
                            self.logger.info(f"  + {filepath.name}")
                        time.sleep(0.5)
                else:
                    self.logger.info("No new unread messages")

                self.logger.info(f"Sleeping for {self.check_interval} seconds...")
                time.sleep(self.check_interval)

            except KeyboardInterrupt:
                self.logger.info("\nStopping WhatsApp Watcher")
                break
            except Exception as e:
                self.logger.error(f"Error: {e}")
                self.logger.info("Attempting to recover...")
                time.sleep(10)
                try:
                    self.page.reload(timeout=60000)
                except:
                    self.logger.error("Recovery failed, reconnecting...")
                    self.disconnect()
                    time.sleep(5)
                    if not self.connect():
                        self.logger.error("Reconnection failed. Exiting.")
                        break

        self.disconnect()
        self.logger.info("WhatsApp Watcher stopped")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='WhatsApp Watcher for Autonomous FTE')
    parser.add_argument('--vault-path', default=os.getenv('VAULT_PATH', 'Vault'))
    parser.add_argument('--check-interval', type=int, default=60, help='Seconds between checks (default: 60)')
    parser.add_argument('--headless', action='store_true', help='Run in headless mode (not recommended for WhatsApp)')
    parser.add_argument('--no-headless', action='store_true', default=True, help='Run with visible browser (default)')
    parser.add_argument('--dry-run', action='store_true')

    args = parser.parse_args()

    # WhatsApp Web works better with visible browser
    headless = args.headless and not args.no_headless

    watcher = WhatsAppWatcher(
        vault_path=args.vault_path,
        check_interval=args.check_interval,
        headless=headless,
        dry_run=args.dry_run
    )
    watcher.run()


if __name__ == '__main__':
    main()
