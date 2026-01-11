#!/usr/bin/env python3
"""
Email Sender Script

Simple script to send emails via Gmail API.
Used by approval workflow to send approved email responses.

Usage:
    python send_email.py --to recipient@example.com --subject "Hello" --body "Message"
    python send_email.py --approval-file APPROVAL_EMAIL_xxx.md

Author: Autonomous FTE System
Date: 2026-01-11
"""

import sys
import os
import argparse
import base64
import logging
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

# Gmail API imports
try:
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("Error: Gmail API libraries not installed.")
    print("Install with: uv pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    sys.exit(1)


class EmailSender:
    """Send emails via Gmail API."""

    def __init__(self, token_path: str = 'token.json'):
        """
        Initialize Email Sender.

        Args:
            token_path: Path to Gmail API token file
        """
        self.token_path = Path(token_path)
        self.service = None

        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('EmailSender')

    def authenticate(self) -> None:
        """Authenticate with Gmail API."""
        if not self.token_path.exists():
            self.logger.error(f"Token file not found: {self.token_path}")
            self.logger.error("Run gmail_watcher.py first to authenticate")
            sys.exit(1)

        try:
            creds = Credentials.from_authorized_user_file(
                str(self.token_path),
                ['https://www.googleapis.com/auth/gmail.send']
            )

            self.service = build('gmail', 'v1', credentials=creds)
            self.logger.info("Gmail API authenticated successfully")

        except Exception as e:
            self.logger.error(f"Authentication failed: {e}")
            sys.exit(1)

    def create_message(
        self,
        to: str,
        subject: str,
        body: str,
        from_email: Optional[str] = None
    ) -> dict:
        """
        Create email message.

        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body (plain text)
            from_email: Sender email (optional, uses authenticated account)

        Returns:
            Message dict ready to send
        """
        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject
        if from_email:
            message['from'] = from_email

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        return {'raw': raw}

    def send_message(self, message: dict) -> bool:
        """
        Send email message.

        Args:
            message: Message dict from create_message()

        Returns:
            True if sent successfully, False otherwise
        """
        try:
            sent_message = self.service.users().messages().send(
                userId='me',
                body=message
            ).execute()

            self.logger.info(f"Email sent successfully (Message ID: {sent_message['id']})")
            return True

        except HttpError as e:
            self.logger.error(f"Failed to send email: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return False

    def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        from_email: Optional[str] = None
    ) -> bool:
        """
        Send email (convenience method).

        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body
            from_email: Sender email (optional)

        Returns:
            True if sent successfully
        """
        self.authenticate()
        message = self.create_message(to, subject, body, from_email)
        return self.send_message(message)

    def send_from_approval_file(self, approval_file_path: str) -> bool:
        """
        Send email from approval file.

        Args:
            approval_file_path: Path to APPROVAL_EMAIL_*.md file

        Returns:
            True if sent successfully
        """
        import yaml
        import re

        file_path = Path(approval_file_path)

        if not file_path.exists():
            self.logger.error(f"Approval file not found: {file_path}")
            return False

        try:
            # Read file
            content = file_path.read_text(encoding='utf-8')

            # Extract YAML frontmatter
            frontmatter_pattern = r'^---\s*\n(.*?)\n---\s*\n'
            match = re.search(frontmatter_pattern, content, re.DOTALL)

            if not match:
                self.logger.error("No YAML frontmatter found in approval file")
                return False

            metadata = yaml.safe_load(match.group(1))

            # Extract email body
            body_pattern = r'## Email Body\s*\n```\s*\n(.*?)\n```'
            body_match = re.search(body_pattern, content, re.DOTALL)

            if not body_match:
                self.logger.error("No email body found in approval file")
                return False

            body = body_match.group(1).strip()

            # Send email
            to = metadata.get('to')
            subject = metadata.get('subject')

            if not to or not subject:
                self.logger.error("Missing 'to' or 'subject' in approval file")
                return False

            self.logger.info(f"Sending email to: {to}")
            self.logger.info(f"Subject: {subject}")

            return self.send_email(to, subject, body)

        except Exception as e:
            self.logger.error(f"Error processing approval file: {e}")
            return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Send email via Gmail API')

    # Option 1: Direct parameters
    parser.add_argument('--to', help='Recipient email address')
    parser.add_argument('--subject', help='Email subject')
    parser.add_argument('--body', help='Email body')
    parser.add_argument('--from', dest='from_email', help='Sender email (optional)')

    # Option 2: From approval file
    parser.add_argument('--approval-file', help='Path to APPROVAL_EMAIL_*.md file')

    # Configuration
    parser.add_argument(
        '--token',
        default='token.json',
        help='Path to Gmail API token file (default: token.json)'
    )

    args = parser.parse_args()

    sender = EmailSender(token_path=args.token)

    # Send from approval file
    if args.approval_file:
        success = sender.send_from_approval_file(args.approval_file)
        sys.exit(0 if success else 1)

    # Send with direct parameters
    if not args.to or not args.subject or not args.body:
        parser.error("Either --approval-file OR (--to, --subject, --body) are required")

    success = sender.send_email(
        to=args.to,
        subject=args.subject,
        body=args.body,
        from_email=args.from_email
    )

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
