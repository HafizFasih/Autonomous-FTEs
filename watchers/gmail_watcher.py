#!/usr/bin/env python3
"""
Gmail Watcher

Monitors Gmail inbox for new emails and creates EMAIL_*.md files in /Needs_Action folder.
Uses Gmail API to check for unread important emails at regular intervals.

Setup Required:
1. Enable Gmail API in Google Cloud Console
2. Download OAuth 2.0 credentials.json
3. Run authentication flow (first time only)
4. Configure .env file with paths

Usage:
    python gmail_watcher.py
    python gmail_watcher.py --check-interval 120
    python gmail_watcher.py --dry-run

Author: Autonomous FTE System
Date: 2026-01-11
"""

import os
import sys
import time
import logging
import json
from pathlib import Path
from datetime import datetime
from typing import Set, List, Dict, Any, Optional

# Gmail API imports (install: pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client)
try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("Error: Gmail API libraries not installed.")
    print("Install with: uv pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    sys.exit(1)


# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


class GmailWatcher:
    """Monitor Gmail for new emails and create action files."""

    def __init__(
        self,
        vault_path: str,
        credentials_path: str,
        token_path: str = 'token.json',
        check_interval: int = 120,
        dry_run: bool = False
    ):
        """
        Initialize Gmail Watcher.

        Args:
            vault_path: Path to Obsidian vault root
            credentials_path: Path to OAuth credentials.json
            token_path: Path to store authentication token
            check_interval: Seconds between checks (default: 120)
            dry_run: If True, don't create files, just log what would happen
        """
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.credentials_path = Path(credentials_path)
        self.token_path = Path(token_path)
        self.check_interval = check_interval
        self.dry_run = dry_run

        # Track processed message IDs to avoid duplicates
        self.processed_ids: Set[str] = set()
        self.processed_ids_file = self.vault_path / 'Logs' / 'gmail_processed_ids.json'

        # Gmail service (initialized in authenticate)
        self.service = None

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
            with open(self.processed_ids_file, 'w') as f:
                json.dump({
                    'processed_ids': list(self.processed_ids),
                    'last_updated': datetime.now().isoformat(),
                    'count': len(self.processed_ids)
                }, f, indent=2)
        except Exception as e:
            self.logger.error(f"Could not save processed IDs: {e}")

    def authenticate(self) -> None:
        """Authenticate with Gmail API using OAuth 2.0."""
        creds = None

        # Load existing token if available
        if self.token_path.exists():
            try:
                creds = Credentials.from_authorized_user_file(str(self.token_path), SCOPES)
            except Exception as e:
                self.logger.warning(f"Could not load token: {e}")

        # If no valid credentials, authenticate
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    self.logger.info("Refreshing expired credentials...")
                    creds.refresh(Request())
                except Exception as e:
                    self.logger.error(f"Could not refresh credentials: {e}")
                    creds = None

            if not creds:
                if not self.credentials_path.exists():
                    self.logger.error(f"Credentials file not found: {self.credentials_path}")
                    self.logger.error("Download credentials.json from Google Cloud Console")
                    sys.exit(1)

                self.logger.info("Starting OAuth authentication flow...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self.credentials_path), SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save credentials for next run
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())
            self.logger.info("Credentials saved successfully")

        # Build Gmail service
        self.service = build('gmail', 'v1', credentials=creds)
        self.logger.info("Gmail API authenticated successfully")

    def check_for_updates(self) -> List[Dict[str, Any]]:
        """
        Check Gmail for new unread important emails.

        Returns:
            List of new message metadata dictionaries
        """
        try:
            # Query for unread important emails
            query = 'is:unread is:important'

            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=20  # Process max 20 at a time
            ).execute()

            messages = results.get('messages', [])

            # Filter out already processed messages
            new_messages = [
                msg for msg in messages
                if msg['id'] not in self.processed_ids
            ]

            self.logger.info(f"Found {len(messages)} unread important emails, {len(new_messages)} new")

            return new_messages

        except HttpError as e:
            self.logger.error(f"Gmail API error: {e}")
            return []
        except Exception as e:
            self.logger.error(f"Error checking for updates: {e}")
            return []

    def get_message_details(self, message_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetch full message details from Gmail.

        Args:
            message_id: Gmail message ID

        Returns:
            Dictionary with message details or None if error
        """
        try:
            msg = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()

            # Extract headers
            headers = {
                h['name']: h['value']
                for h in msg['payload'].get('headers', [])
            }

            # Extract email body
            body = self._extract_body(msg['payload'])

            return {
                'id': message_id,
                'thread_id': msg.get('threadId', ''),
                'from': headers.get('From', 'Unknown'),
                'to': headers.get('To', ''),
                'subject': headers.get('Subject', 'No Subject'),
                'date': headers.get('Date', ''),
                'body': body,
                'snippet': msg.get('snippet', ''),
                'labels': msg.get('labelIds', [])
            }

        except HttpError as e:
            self.logger.error(f"Error fetching message {message_id}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error fetching message: {e}")
            return None

    def _extract_body(self, payload: Dict[str, Any]) -> str:
        """
        Extract email body from message payload.

        Args:
            payload: Gmail message payload

        Returns:
            Email body text
        """
        import base64

        # Check for simple body
        if 'body' in payload and payload['body'].get('size', 0) > 0:
            data = payload['body'].get('data', '')
            if data:
                return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')

        # Check for multipart message
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data', '')
                    if data:
                        return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')

                # Recursively check nested parts
                if 'parts' in part:
                    body = self._extract_body(part)
                    if body:
                        return body

        return ''

    def _parse_sender(self, from_header: str) -> tuple[str, str]:
        """
        Parse sender name and email from From header.

        Args:
            from_header: Email From header (e.g., "John Doe <john@example.com>")

        Returns:
            Tuple of (name, email)
        """
        import re

        # Match "Name <email>" format
        match = re.match(r'(.+?)\s*<(.+?)>', from_header)
        if match:
            name = match.group(1).strip().strip('"')
            email = match.group(2).strip()
            return name, email

        # If no name, just email
        if '@' in from_header:
            return from_header, from_header

        return 'Unknown', from_header

    def _determine_priority(self, subject: str, body: str, labels: List[str]) -> str:
        """
        Determine email priority based on content.

        Args:
            subject: Email subject
            body: Email body
            labels: Gmail labels

        Returns:
            Priority level: 'high', 'normal', or 'low'
        """
        urgent_keywords = [
            'urgent', 'asap', 'immediate', 'emergency', 'critical',
            'time-sensitive', 'deadline today', 'action required'
        ]

        text = f"{subject} {body}".lower()

        # Check for urgent keywords
        if any(kw in text for kw in urgent_keywords):
            return 'high'

        # Check Gmail labels
        if 'IMPORTANT' in labels:
            return 'normal'

        return 'normal'  # Default to normal for emails that pass initial filter

    def create_action_file(self, message: Dict[str, Any]) -> Optional[Path]:
        """
        Create EMAIL_*.md file in Needs_Action folder.

        Args:
            message: Message details dictionary

        Returns:
            Path to created file or None if error
        """
        try:
            # Parse sender
            sender_name, sender_email = self._parse_sender(message['from'])

            # Determine priority
            priority = self._determine_priority(
                message['subject'],
                message['body'],
                message['labels']
            )

            # Create safe filename
            timestamp = datetime.now().strftime('%Y-%m-%d')
            safe_subject = ''.join(c for c in message['subject'][:30] if c.isalnum() or c in (' ', '_')).strip()
            safe_subject = safe_subject.replace(' ', '_')
            filename = f"EMAIL_{safe_subject}_{timestamp}.md"

            filepath = self.needs_action / filename

            # Check if file already exists
            if filepath.exists():
                filename = f"EMAIL_{safe_subject}_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.md"
                filepath = self.needs_action / filename

            # Build email content
            content = self._build_email_content(
                message,
                sender_name,
                sender_email,
                priority
            )

            if self.dry_run:
                self.logger.info(f"[DRY RUN] Would create file: {filename}")
                self.logger.info(f"[DRY RUN] Priority: {priority}, From: {sender_name}")
                return filepath

            # Write file
            filepath.write_text(content, encoding='utf-8')

            self.logger.info(f"Created email file: {filename} (Priority: {priority})")

            # Mark as processed
            self.processed_ids.add(message['id'])
            self._save_processed_ids()

            return filepath

        except Exception as e:
            self.logger.error(f"Error creating action file: {e}")
            return None

    def _build_email_content(
        self,
        message: Dict[str, Any],
        sender_name: str,
        sender_email: str,
        priority: str
    ) -> str:
        """Build formatted email content for .md file."""
        content = f"""---
type: email
from: {sender_email}
from_name: {sender_name}
subject: {message['subject']}
received: {datetime.now().isoformat()}
priority: {priority}
message_id: {message['id']}
thread_id: {message['thread_id']}
status: pending
---

## Email Content

{message['body'] if message['body'] else message['snippet']}

## Suggested Actions

- [ ] Reply to sender
- [ ] Forward to relevant party
- [ ] Archive after processing
{'- [ ] FLAG AS URGENT - Handle immediately' if priority == 'high' else ''}

## Metadata

- **Labels:** {', '.join(message['labels'])}
- **Thread ID:** {message['thread_id']}
- **Received:** {message['date']}
"""
        return content

    def run(self) -> None:
        """Run the watcher continuously."""
        self.logger.info(f"Starting Gmail Watcher (check interval: {self.check_interval}s)")
        if self.dry_run:
            self.logger.info("DRY RUN MODE - No files will be created")

        # Authenticate
        self.authenticate()

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

                    for msg_info in new_messages:
                        # Fetch full message details
                        message = self.get_message_details(msg_info['id'])

                        if message:
                            # Create action file
                            filepath = self.create_action_file(message)

                            if filepath and not self.dry_run:
                                self.logger.info(f"  ✓ {filepath.name}")
                        else:
                            self.logger.warning(f"  ✗ Could not fetch message {msg_info['id']}")

                        # Small delay between messages
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
                self.logger.info("Continuing after error...")
                time.sleep(30)  # Wait before retrying

        self.logger.info("Gmail Watcher stopped")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Gmail Watcher for Autonomous FTE')
    parser.add_argument(
        '--vault-path',
        default=os.getenv('VAULT_PATH', 'Vault'),
        help='Path to Obsidian vault (default: Vault directory or VAULT_PATH env var)'
    )
    parser.add_argument(
        '--credentials',
        default=os.getenv('GMAIL_CREDENTIALS', 'credentials.json'),
        help='Path to Gmail API credentials.json (default: credentials.json or GMAIL_CREDENTIALS env var)'
    )
    parser.add_argument(
        '--token',
        default='token.json',
        help='Path to store authentication token (default: token.json)'
    )
    parser.add_argument(
        '--check-interval',
        type=int,
        default=120,
        help='Seconds between Gmail checks (default: 120)'
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
        credentials_path=args.credentials,
        token_path=args.token,
        check_interval=args.check_interval,
        dry_run=args.dry_run
    )

    watcher.run()


if __name__ == '__main__':
    main()
