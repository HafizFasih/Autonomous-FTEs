#!/usr/bin/env python3
"""
Gmail Watcher (IMAP Version)

Monitors Gmail inbox for new emails using IMAP and creates EMAIL_*.md files in /Needs_Action folder.
Uses credentials from .env file.

Usage:
    python gmail_watcher.py
    python gmail_watcher.py --check-interval 60
    python gmail_watcher.py --dry-run

Author: Autonomous FTE System
"""

import os
import sys
import time
import logging
import json
import imaplib
import email
from email.message import Message
from email.header import decode_header
from pathlib import Path
from datetime import datetime
from typing import Set, List, Dict, Any, Optional

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed. Using system environment variables.")


class GmailWatcher:
    """Monitor Gmail for new emails using IMAP and create action files."""

    def __init__(
        self,
        vault_path: str,
        check_interval: int = 60,
        dry_run: bool = False
    ):
        """
        Initialize Gmail Watcher.

        Args:
            vault_path: Path to Obsidian vault root
            check_interval: Seconds between checks (default: 60)
            dry_run: If True, don't create files, just log what would happen
        """
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.check_interval = check_interval
        self.dry_run = dry_run

        # IMAP settings from .env
        self.imap_server = os.getenv('EMAIL_IMAP_SERVER', 'imap.gmail.com')
        self.imap_port = int(os.getenv('EMAIL_IMAP_PORT', '993'))
        self.username = os.getenv('EMAIL_USERNAME', '')
        self.password = os.getenv('EMAIL_PASSWORD', '')

        if not self.username or not self.password:
            print("Error: EMAIL_USERNAME and EMAIL_PASSWORD must be set in .env file")
            sys.exit(1)

        # Track processed message IDs to avoid duplicates
        self.processed_ids: Set[str] = set()
        self.processed_ids_file = self.vault_path / 'Logs' / 'gmail_processed_ids.json'

        # IMAP connection
        self.mail = None

        # Setup logging
        self._setup_logging()

        # Load previously processed IDs
        self._load_processed_ids()

        # Ensure directories exist
        self._ensure_directories()

    def _setup_logging(self) -> None:
        """Configure logging."""
        log_dir = self.vault_path / 'Logs'
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / 'gmail_watcher.log'

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )

        self.logger = logging.getLogger('GmailWatcher')

    def _ensure_directories(self) -> None:
        """Ensure required directories exist."""
        self.needs_action.mkdir(parents=True, exist_ok=True)
        (self.vault_path / 'Logs').mkdir(exist_ok=True)

    def _load_processed_ids(self) -> None:
        """Load previously processed message IDs from file."""
        if self.processed_ids_file.exists():
            try:
                with open(self.processed_ids_file, 'r') as f:
                    data = json.load(f)
                    self.processed_ids = set(data.get('processed_ids', []))
                    self.logger.info(f"Loaded {len(self.processed_ids)} previously processed message IDs")
            except Exception as e:
                self.logger.warning(f"Could not load processed IDs: {e}")
                self.processed_ids = set()

    def _save_processed_ids(self) -> None:
        """Save processed message IDs to file."""
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

    def connect(self) -> bool:
        """Connect to Gmail IMAP server."""
        try:
            self.logger.info(f"Connecting to {self.imap_server}:{self.imap_port}...")
            self.mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            self.mail.login(self.username, self.password)
            self.logger.info(f"Connected as {self.username}")
            return True
        except imaplib.IMAP4.error as e:
            self.logger.error(f"IMAP authentication failed: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Connection error: {e}")
            return False

    def disconnect(self) -> None:
        """Disconnect from IMAP server."""
        if self.mail:
            try:
                self.mail.logout()
            except:
                pass
            self.mail = None

    def _decode_header_value(self, value: str) -> str:
        """Decode email header value."""
        if not value:
            return ""
        decoded_parts = decode_header(value)
        result = []
        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                result.append(part.decode(encoding or 'utf-8', errors='ignore'))
            else:
                result.append(part)
        return ''.join(result)

    def _extract_body(self, msg: Message) -> str:
        """Extract email body from message."""
        body = ""

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if content_type == "text/plain" and "attachment" not in content_disposition:
                    try:
                        payload = part.get_payload(decode=True)
                        if payload:
                            charset = part.get_content_charset() or 'utf-8'
                            body = payload.decode(charset, errors='ignore')
                            break
                    except:
                        pass
        else:
            try:
                payload = msg.get_payload(decode=True)
                if payload:
                    charset = msg.get_content_charset() or 'utf-8'
                    body = payload.decode(charset, errors='ignore')
            except:
                pass

        # Truncate very long bodies
        if len(body) > 5000:
            body = body[:5000] + "\n\n[... truncated ...]"

        return body.strip()

    def _parse_sender(self, from_header: str) -> tuple:
        """Parse sender name and email from From header."""
        import re

        from_header = self._decode_header_value(from_header)

        # Match "Name <email>" format
        match = re.match(r'(.+?)\s*<(.+?)>', from_header)
        if match:
            name = match.group(1).strip().strip('"')
            email_addr = match.group(2).strip()
            return name, email_addr

        # If no name, just email
        if '@' in from_header:
            return from_header, from_header

        return 'Unknown', from_header

    def _determine_priority(self, subject: str, body: str) -> str:
        """Determine email priority based on content."""
        urgent_keywords = [
            'urgent', 'asap', 'immediate', 'emergency', 'critical',
            'time-sensitive', 'deadline today', 'action required'
        ]

        text = f"{subject} {body}".lower()

        if any(kw in text for kw in urgent_keywords):
            return 'high'

        return 'normal'

    def check_for_updates(self) -> List[Dict[str, Any]]:
        """Check Gmail for new unread emails."""
        try:
            # Select inbox
            self.mail.select('INBOX')

            # Search for unread emails
            status, messages = self.mail.search(None, 'UNSEEN')

            if status != 'OK':
                self.logger.error("Failed to search emails")
                return []

            email_ids = messages[0].split()
            new_emails = []

            for email_id in email_ids[-20:]:  # Process max 20 at a time
                msg_id = email_id.decode()

                if msg_id in self.processed_ids:
                    continue

                # Fetch email
                status, msg_data = self.mail.fetch(email_id, '(RFC822)')

                if status != 'OK':
                    continue

                # Parse email
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)

                # Extract details
                subject = self._decode_header_value(msg.get('Subject', 'No Subject'))
                from_header = msg.get('From', 'Unknown')
                sender_name, sender_email = self._parse_sender(from_header)
                date = msg.get('Date', '')
                body = self._extract_body(msg)
                message_id = msg.get('Message-ID', msg_id)

                new_emails.append({
                    'id': msg_id,
                    'message_id': message_id,
                    'from': from_header,
                    'sender_name': sender_name,
                    'sender_email': sender_email,
                    'subject': subject,
                    'date': date,
                    'body': body,
                    'snippet': body[:200] if body else ''
                })

            self.logger.info(f"Found {len(email_ids)} unread emails, {len(new_emails)} new")
            return new_emails

        except Exception as e:
            self.logger.error(f"Error checking for updates: {e}")
            # Try to reconnect
            self.disconnect()
            self.connect()
            return []

    def create_action_file(self, message: Dict[str, Any]) -> Optional[Path]:
        """Create an action file for the email in Needs_Action folder."""
        try:
            # Generate filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            safe_subject = "".join(c for c in message['subject'][:30] if c.isalnum() or c in ' -_').strip()
            safe_subject = safe_subject.replace(' ', '_') or 'no_subject'
            filename = f"EMAIL_{timestamp}_{safe_subject}.md"

            filepath = self.needs_action / filename

            # Determine priority
            priority = self._determine_priority(message['subject'], message['body'])

            # Build content
            content = self._build_email_content(message, priority)

            if not self.dry_run:
                filepath.write_text(content, encoding='utf-8')

            self.logger.info(f"Created email file: {filename} (Priority: {priority})")

            # Mark as processed
            self.processed_ids.add(message['id'])
            self._save_processed_ids()

            return filepath

        except Exception as e:
            self.logger.error(f"Error creating action file: {e}")
            return None

    def _build_email_content(self, message: Dict[str, Any], priority: str) -> str:
        """Build formatted email content for .md file."""
        content = f"""---
type: email
from: {message['sender_email']}
from_name: {message['sender_name']}
subject: {message['subject']}
received: {datetime.now().isoformat()}
priority: {priority}
message_id: {message['message_id']}
status: pending
---

## Email from {message['sender_name']}

**From:** {message['sender_name']} <{message['sender_email']}>
**Subject:** {message['subject']}
**Date:** {message['date']}

---

## Content

{message['body'] if message['body'] else message['snippet']}

---

## Suggested Actions

- [ ] Reply to sender
- [ ] Forward to relevant party
- [ ] Archive after processing
{'- [ ] FLAG AS URGENT - Handle immediately' if priority == 'high' else ''}

## Metadata

- **Message ID:** {message['message_id']}
- **Received:** {message['date']}
"""
        return content

    def run(self) -> None:
        """Run the watcher continuously."""
        self.logger.info(f"Starting Gmail Watcher (IMAP)")
        self.logger.info(f"  Server: {self.imap_server}:{self.imap_port}")
        self.logger.info(f"  User: {self.username}")
        self.logger.info(f"  Check interval: {self.check_interval}s")

        if self.dry_run:
            self.logger.info("DRY RUN MODE - No files will be created")

        # Connect
        if not self.connect():
            self.logger.error("Failed to connect. Exiting.")
            sys.exit(1)

        # Main monitoring loop
        iteration = 0
        while True:
            try:
                iteration += 1
                self.logger.info(f"--- Check #{iteration} ---")

                # Check for new messages
                new_messages = self.check_for_updates()

                if new_messages:
                    self.logger.info(f"Processing {len(new_messages)} new emails...")

                    for msg in new_messages:
                        # Create action file
                        filepath = self.create_action_file(msg)

                        if filepath:
                            self.logger.info(f"  + {filepath.name}")
                        else:
                            self.logger.warning(f"  - Could not process: {msg['subject'][:50]}")

                        time.sleep(0.5)
                else:
                    self.logger.info("No new emails")

                # Sleep until next check
                self.logger.info(f"Sleeping for {self.check_interval} seconds...")
                time.sleep(self.check_interval)

            except KeyboardInterrupt:
                self.logger.info("\nStopping Gmail Watcher (Ctrl+C received)")
                break
            except Exception as e:
                self.logger.error(f"Error in main loop: {e}")
                self.logger.info("Reconnecting...")
                self.disconnect()
                time.sleep(5)
                self.connect()

        self.disconnect()
        self.logger.info("Gmail Watcher stopped")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Gmail Watcher (IMAP) for Autonomous FTE')
    parser.add_argument(
        '--vault-path',
        default=os.getenv('VAULT_PATH', 'Vault'),
        help='Path to Obsidian vault (default: Vault directory or VAULT_PATH env var)'
    )
    parser.add_argument(
        '--check-interval',
        type=int,
        default=60,
        help='Seconds between Gmail checks (default: 60)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Dry run mode - log what would happen but don\'t create files'
    )

    args = parser.parse_args()

    # Create and run watcher
    watcher = GmailWatcher(
        vault_path=args.vault_path,
        check_interval=args.check_interval,
        dry_run=args.dry_run
    )

    watcher.run()


if __name__ == '__main__':
    main()
