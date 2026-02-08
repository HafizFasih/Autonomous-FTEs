#!/usr/bin/env python3
"""
LinkedIn Watcher

Monitors LinkedIn for new notifications, messages, and connection requests.
Uses Playwright for browser automation since LinkedIn doesn't have a public API.
Creates action files in /Needs_Action folder.

Usage:
    python linkedin_watcher.py
    python linkedin_watcher.py --check-interval 300
    python linkedin_watcher.py --headless

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


class LinkedInWatcher:
    """Monitor LinkedIn for notifications and messages using browser automation."""

    def __init__(
        self,
        vault_path: str,
        check_interval: int = 300,
        headless: bool = True,
        dry_run: bool = False
    ):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.check_interval = check_interval
        self.headless = headless
        self.dry_run = dry_run

        # LinkedIn credentials from .env
        self.email = os.getenv('LINKEDIN_EMAIL', '')
        self.password = os.getenv('LINKEDIN_PASSWORD', '')
        self.session_path = os.getenv('LINKEDIN_SESSION_PATH', './linkedin_session')
        self.cookies_path = os.getenv('LINKEDIN_COOKIES_PATH', './linkedin_cookies.json')

        if not self.email or not self.password:
            print("Error: LINKEDIN_EMAIL and LINKEDIN_PASSWORD must be set in .env")
            sys.exit(1)

        # Track processed IDs
        self.processed_ids: Set[str] = set()
        self.processed_ids_file = self.vault_path / 'Logs' / 'linkedin_processed_ids.json'

        # Browser instances
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None

        # Setup
        self._setup_logging()
        self._load_processed_ids()
        self._ensure_directories()

    def _setup_logging(self) -> None:
        log_dir = self.vault_path / 'Logs'
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / 'linkedin_watcher.log'

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger('LinkedInWatcher')

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
                    self.logger.info(f"Loaded {len(self.processed_ids)} processed IDs")
            except Exception as e:
                self.logger.warning(f"Could not load processed IDs: {e}")

    def _save_processed_ids(self) -> None:
        try:
            self.processed_ids_file.parent.mkdir(exist_ok=True)
            with open(self.processed_ids_file, 'w') as f:
                json.dump({
                    'processed_ids': list(self.processed_ids),
                    'last_updated': datetime.now().isoformat(),
                    'count': len(self.processed_ids)
                }, f, indent=2)
        except Exception as e:
            self.logger.error(f"Could not save processed IDs: {e}")

    def _save_cookies(self) -> None:
        """Save cookies for future sessions."""
        if self.page:
            try:
                cookies = self.page.context.cookies()
                with open(self.cookies_path, 'w') as f:
                    json.dump(cookies, f, indent=2)
                self.logger.info("Cookies saved")
            except Exception as e:
                self.logger.error(f"Could not save cookies: {e}")

    def _load_cookies(self) -> bool:
        """Load cookies from previous session."""
        if Path(self.cookies_path).exists():
            try:
                with open(self.cookies_path, 'r') as f:
                    cookies = json.load(f)
                self.page.context.add_cookies(cookies)
                self.logger.info("Cookies loaded")
                return True
            except Exception as e:
                self.logger.warning(f"Could not load cookies: {e}")
        return False

    def connect(self) -> bool:
        """Launch browser and login to LinkedIn."""
        try:
            self.logger.info("Launching browser...")
            self.playwright = sync_playwright().start()

            self.browser = self.playwright.chromium.launch(
                headless=self.headless,
                args=['--disable-blink-features=AutomationControlled']
            )

            context = self.browser.new_context(
                viewport={'width': 1280, 'height': 800},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )

            self.page = context.new_page()

            # Try to use existing cookies
            if self._load_cookies():
                self.page.goto('https://www.linkedin.com/feed/', timeout=90000)
                time.sleep(5)

                # Check if logged in
                if 'feed' in self.page.url and 'login' not in self.page.url:
                    self.logger.info("Logged in via cookies")
                    return True

            # Manual login required
            self.logger.info("Logging in to LinkedIn...")
            self.page.goto('https://www.linkedin.com/login', timeout=90000)
            time.sleep(3)

            # Fill credentials
            self.page.fill('input#username', self.email)
            self.page.fill('input#password', self.password)
            self.page.click('button[type="submit"]')

            time.sleep(5)

            # Check for security challenges
            if 'checkpoint' in self.page.url or 'challenge' in self.page.url:
                self.logger.warning("Security challenge detected!")
                self.logger.warning("Please complete the challenge manually in the browser")
                if not self.headless:
                    input("Press Enter after completing the challenge...")
                else:
                    self.logger.error("Cannot complete challenge in headless mode. Run with --no-headless")
                    return False

            # Verify login success
            if 'feed' in self.page.url or 'mynetwork' in self.page.url:
                self.logger.info(f"Logged in as {self.email}")
                self._save_cookies()
                return True
            else:
                self.logger.error(f"Login may have failed. Current URL: {self.page.url}")
                return False

        except Exception as e:
            self.logger.error(f"Connection error: {e}")
            return False

    def disconnect(self) -> None:
        """Close browser."""
        try:
            if self.page:
                self._save_cookies()
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
        except:
            pass
        self.browser = None
        self.page = None
        self.playwright = None

    def check_notifications(self) -> List[Dict[str, Any]]:
        """Check LinkedIn notifications."""
        notifications = []
        try:
            self.logger.info("Checking notifications...")
            self.page.goto('https://www.linkedin.com/notifications/', timeout=60000)
            time.sleep(5)

            # Get notification items
            notif_elements = self.page.query_selector_all('div.nt-card')

            for elem in notif_elements[:15]:  # Limit to 15
                try:
                    # Extract notification text
                    text_elem = elem.query_selector('.nt-card__text')
                    text = text_elem.inner_text() if text_elem else ''

                    # Extract time
                    time_elem = elem.query_selector('.nt-card__time')
                    notif_time = time_elem.inner_text() if time_elem else ''

                    # Generate ID from content
                    notif_id = f"notif_{hash(text[:100])}"

                    if notif_id in self.processed_ids:
                        continue

                    if text:
                        notifications.append({
                            'id': notif_id,
                            'type': 'notification',
                            'text': text.strip(),
                            'time': notif_time.strip(),
                            'url': self.page.url
                        })
                except Exception as e:
                    self.logger.debug(f"Error parsing notification: {e}")
                    continue

            self.logger.info(f"Found {len(notifications)} new notifications")

        except Exception as e:
            self.logger.error(f"Error checking notifications: {e}")

        return notifications

    def check_messages(self) -> List[Dict[str, Any]]:
        """Check LinkedIn messages."""
        messages = []
        try:
            self.logger.info("Checking messages...")
            self.page.goto('https://www.linkedin.com/messaging/', timeout=60000)
            time.sleep(5)

            # Get conversation items
            conv_elements = self.page.query_selector_all('li.msg-conversation-listitem')

            for elem in conv_elements[:10]:  # Limit to 10
                try:
                    # Check for unread indicator
                    unread = elem.query_selector('.msg-conversation-card__unread-count')
                    if not unread:
                        continue

                    # Extract sender name
                    name_elem = elem.query_selector('.msg-conversation-card__participant-names')
                    sender = name_elem.inner_text() if name_elem else 'Unknown'

                    # Extract preview
                    preview_elem = elem.query_selector('.msg-conversation-card__message-snippet')
                    preview = preview_elem.inner_text() if preview_elem else ''

                    # Extract time
                    time_elem = elem.query_selector('.msg-conversation-card__time-stamp')
                    msg_time = time_elem.inner_text() if time_elem else ''

                    # Generate ID
                    msg_id = f"msg_{hash(sender + preview[:50])}"

                    if msg_id in self.processed_ids:
                        continue

                    messages.append({
                        'id': msg_id,
                        'type': 'message',
                        'sender': sender.strip(),
                        'preview': preview.strip(),
                        'time': msg_time.strip(),
                        'text': f"Message from {sender}: {preview}"
                    })
                except Exception as e:
                    self.logger.debug(f"Error parsing message: {e}")
                    continue

            self.logger.info(f"Found {len(messages)} unread messages")

        except Exception as e:
            self.logger.error(f"Error checking messages: {e}")

        return messages

    def check_connection_requests(self) -> List[Dict[str, Any]]:
        """Check pending connection requests."""
        requests = []
        try:
            self.logger.info("Checking connection requests...")
            self.page.goto('https://www.linkedin.com/mynetwork/invitation-manager/', timeout=60000)
            time.sleep(5)

            # Get invitation cards
            invite_elements = self.page.query_selector_all('li.invitation-card')

            for elem in invite_elements[:10]:
                try:
                    # Extract name
                    name_elem = elem.query_selector('.invitation-card__title')
                    name = name_elem.inner_text() if name_elem else 'Unknown'

                    # Extract subtitle (title/company)
                    subtitle_elem = elem.query_selector('.invitation-card__subtitle')
                    subtitle = subtitle_elem.inner_text() if subtitle_elem else ''

                    # Generate ID
                    req_id = f"conn_{hash(name)}"

                    if req_id in self.processed_ids:
                        continue

                    requests.append({
                        'id': req_id,
                        'type': 'connection_request',
                        'name': name.strip(),
                        'subtitle': subtitle.strip(),
                        'text': f"Connection request from {name} - {subtitle}"
                    })
                except Exception as e:
                    self.logger.debug(f"Error parsing connection request: {e}")
                    continue

            self.logger.info(f"Found {len(requests)} pending connection requests")

        except Exception as e:
            self.logger.error(f"Error checking connection requests: {e}")

        return requests

    def create_action_file(self, item: Dict[str, Any]) -> Optional[Path]:
        """Create action file for LinkedIn item."""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            item_type = item.get('type', 'item').upper()

            # Safe filename
            text_preview = item.get('text', item.get('sender', 'unknown'))[:30]
            safe_text = "".join(c for c in text_preview if c.isalnum() or c in ' -_').strip()
            safe_text = safe_text.replace(' ', '_') or 'item'

            filename = f"LINKEDIN_{item_type}_{timestamp}_{safe_text}.md"
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
        item_type = item.get('type', 'item')

        if item_type == 'message':
            content = f"""---
type: linkedin_message
sender: {item.get('sender', 'Unknown')}
received: {datetime.now().isoformat()}
status: pending
---

## LinkedIn Message from {item.get('sender', 'Unknown')}

**From:** {item.get('sender', 'Unknown')}
**Time:** {item.get('time', 'Unknown')}

---

## Preview

{item.get('preview', 'No preview available')}

---

## Suggested Actions

- [ ] Read full message on LinkedIn
- [ ] Reply to sender
- [ ] Archive after processing

"""
        elif item_type == 'connection_request':
            content = f"""---
type: linkedin_connection_request
from: {item.get('name', 'Unknown')}
received: {datetime.now().isoformat()}
status: pending
---

## LinkedIn Connection Request

**From:** {item.get('name', 'Unknown')}
**Title:** {item.get('subtitle', 'Unknown')}

---

## Suggested Actions

- [ ] Review profile
- [ ] Accept connection
- [ ] Ignore request
- [ ] Send message with acceptance

"""
        else:  # notification
            content = f"""---
type: linkedin_notification
received: {datetime.now().isoformat()}
status: pending
---

## LinkedIn Notification

**Time:** {item.get('time', 'Unknown')}

---

## Content

{item.get('text', 'No content')}

---

## Suggested Actions

- [ ] Review on LinkedIn
- [ ] Take appropriate action
- [ ] Archive after processing

"""
        return content

    def run(self) -> None:
        """Run the watcher continuously."""
        self.logger.info("Starting LinkedIn Watcher")
        self.logger.info(f"  Account: {self.email}")
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

                all_items = []

                # Check notifications
                notifications = self.check_notifications()
                all_items.extend(notifications)

                # Check messages
                messages = self.check_messages()
                all_items.extend(messages)

                # Check connection requests
                requests = self.check_connection_requests()
                all_items.extend(requests)

                if all_items:
                    self.logger.info(f"Processing {len(all_items)} items...")
                    for item in all_items:
                        filepath = self.create_action_file(item)
                        if filepath:
                            self.logger.info(f"  + {filepath.name}")
                        time.sleep(0.5)
                else:
                    self.logger.info("No new items")

                self.logger.info(f"Sleeping for {self.check_interval} seconds...")
                time.sleep(self.check_interval)

            except KeyboardInterrupt:
                self.logger.info("\nStopping LinkedIn Watcher")
                break
            except Exception as e:
                self.logger.error(f"Error: {e}")
                self.logger.info("Attempting to reconnect...")
                self.disconnect()
                time.sleep(30)
                self.connect()

        self.disconnect()
        self.logger.info("LinkedIn Watcher stopped")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='LinkedIn Watcher for Autonomous FTE')
    parser.add_argument('--vault-path', default=os.getenv('VAULT_PATH', 'Vault'))
    parser.add_argument('--check-interval', type=int, default=300, help='Seconds between checks (default: 300)')
    parser.add_argument('--headless', action='store_true', default=True, help='Run browser in headless mode')
    parser.add_argument('--no-headless', action='store_true', help='Run browser with visible window')
    parser.add_argument('--dry-run', action='store_true')

    args = parser.parse_args()

    headless = not args.no_headless

    watcher = LinkedInWatcher(
        vault_path=args.vault_path,
        check_interval=args.check_interval,
        headless=headless,
        dry_run=args.dry_run
    )
    watcher.run()


if __name__ == '__main__':
    main()
