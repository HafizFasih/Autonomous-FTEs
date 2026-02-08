#!/usr/bin/env python3
"""
Twitter Watcher

Monitors Twitter for mentions and DMs, creates action files in /Needs_Action folder.
Uses credentials from .env file.

Usage:
    python twitter_watcher.py
    python twitter_watcher.py --check-interval 120
    python twitter_watcher.py --dry-run

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

# Twitter API
try:
    import tweepy
except ImportError:
    print("Error: tweepy not installed.")
    print("Install with: pip install tweepy")
    sys.exit(1)


class TwitterWatcher:
    """Monitor Twitter for mentions and DMs, create action files."""

    def __init__(
        self,
        vault_path: str,
        check_interval: int = 120,
        dry_run: bool = False
    ):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.check_interval = check_interval
        self.dry_run = dry_run

        # Twitter credentials from .env
        self.api_key = os.getenv('TWITTER_API_KEY', '')
        self.api_secret = os.getenv('TWITTER_API_SECRET', '')
        self.access_token = os.getenv('TWITTER_ACCESS_TOKEN', '')
        self.access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET', '')
        self.bearer_token = os.getenv('TWITTER_BEARER_TOKEN', '')

        if not all([self.api_key, self.api_secret, self.access_token, self.access_token_secret]):
            print("Error: Twitter credentials must be set in .env file")
            sys.exit(1)

        # Track processed IDs
        self.processed_ids: Set[str] = set()
        self.processed_ids_file = self.vault_path / 'Logs' / 'twitter_processed_ids.json'

        # Twitter API client
        self.client = None
        self.api = None
        self.me = None

        # Setup
        self._setup_logging()
        self._load_processed_ids()
        self._ensure_directories()

    def _setup_logging(self) -> None:
        log_dir = self.vault_path / 'Logs'
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / 'twitter_watcher.log'

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger('TwitterWatcher')

    def _ensure_directories(self) -> None:
        self.needs_action.mkdir(parents=True, exist_ok=True)
        (self.vault_path / 'Logs').mkdir(exist_ok=True)

    def _load_processed_ids(self) -> None:
        if self.processed_ids_file.exists():
            try:
                with open(self.processed_ids_file, 'r') as f:
                    data = json.load(f)
                    self.processed_ids = set(data.get('processed_ids', []))
                    self.logger.info(f"Loaded {len(self.processed_ids)} processed tweet IDs")
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

    def connect(self) -> bool:
        """Connect to Twitter API."""
        try:
            self.logger.info("Connecting to Twitter API...")

            # Twitter API v2 client
            self.client = tweepy.Client(
                bearer_token=self.bearer_token,
                consumer_key=self.api_key,
                consumer_secret=self.api_secret,
                access_token=self.access_token,
                access_token_secret=self.access_token_secret,
                wait_on_rate_limit=True
            )

            # Also create v1.1 API for some features
            auth = tweepy.OAuth1UserHandler(
                self.api_key,
                self.api_secret,
                self.access_token,
                self.access_token_secret
            )
            self.api = tweepy.API(auth, wait_on_rate_limit=True)

            # Get authenticated user
            self.me = self.client.get_me()
            if self.me and self.me.data:
                self.logger.info(f"Connected as @{self.me.data.username}")
                return True
            else:
                self.logger.error("Could not get authenticated user")
                return False

        except tweepy.TweepyException as e:
            self.logger.error(f"Twitter API error: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Connection error: {e}")
            return False

    def check_mentions(self) -> List[Dict[str, Any]]:
        """Check for new mentions."""
        mentions = []
        try:
            # Get recent mentions
            response = self.client.get_users_mentions(
                id=self.me.data.id,
                max_results=20,
                tweet_fields=['created_at', 'author_id', 'conversation_id', 'text'],
                user_fields=['username', 'name'],
                expansions=['author_id']
            )

            if not response or not response.data:
                return []

            # Build user lookup
            users = {}
            if response.includes and 'users' in response.includes:
                for user in response.includes['users']:
                    users[user.id] = {'username': user.username, 'name': user.name}

            for tweet in response.data:
                tweet_id = str(tweet.id)
                if tweet_id in self.processed_ids:
                    continue

                author = users.get(tweet.author_id, {'username': 'unknown', 'name': 'Unknown'})

                mentions.append({
                    'id': tweet_id,
                    'type': 'mention',
                    'text': tweet.text,
                    'author_id': str(tweet.author_id),
                    'author_username': author['username'],
                    'author_name': author['name'],
                    'created_at': str(tweet.created_at) if tweet.created_at else '',
                    'conversation_id': str(tweet.conversation_id) if tweet.conversation_id else ''
                })

            self.logger.info(f"Found {len(mentions)} new mentions")

        except tweepy.TweepyException as e:
            self.logger.error(f"Error fetching mentions: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")

        return mentions

    def create_action_file(self, item: Dict[str, Any]) -> Optional[Path]:
        """Create action file for Twitter item."""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            item_type = item.get('type', 'tweet').upper()
            safe_text = "".join(c for c in item['text'][:30] if c.isalnum() or c in ' -_').strip()
            safe_text = safe_text.replace(' ', '_') or 'no_text'
            filename = f"TWITTER_{item_type}_{timestamp}_{safe_text}.md"

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
        item_type = item.get('type', 'tweet')

        content = f"""---
type: twitter_{item_type}
tweet_id: {item['id']}
author: @{item['author_username']}
author_name: {item['author_name']}
created_at: {item['created_at']}
received: {datetime.now().isoformat()}
status: pending
---

## Twitter {item_type.title()} from @{item['author_username']}

**From:** {item['author_name']} (@{item['author_username']})
**Date:** {item['created_at']}

---

## Content

{item['text']}

---

## Suggested Actions

- [ ] Reply to this {item_type}
- [ ] Like the tweet
- [ ] Retweet if relevant
- [ ] Archive after processing

## Metadata

- **Tweet ID:** {item['id']}
- **Conversation ID:** {item.get('conversation_id', 'N/A')}
"""
        return content

    def run(self) -> None:
        """Run the watcher continuously."""
        self.logger.info("Starting Twitter Watcher")
        self.logger.info(f"  Check interval: {self.check_interval}s")

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

                # Check mentions
                mentions = self.check_mentions()

                if mentions:
                    self.logger.info(f"Processing {len(mentions)} items...")
                    for item in mentions:
                        filepath = self.create_action_file(item)
                        if filepath:
                            self.logger.info(f"  + {filepath.name}")
                        time.sleep(0.5)
                else:
                    self.logger.info("No new mentions")

                self.logger.info(f"Sleeping for {self.check_interval} seconds...")
                time.sleep(self.check_interval)

            except KeyboardInterrupt:
                self.logger.info("\nStopping Twitter Watcher")
                break
            except Exception as e:
                self.logger.error(f"Error: {e}")
                time.sleep(30)

        self.logger.info("Twitter Watcher stopped")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Twitter Watcher for Autonomous FTE')
    parser.add_argument('--vault-path', default=os.getenv('VAULT_PATH', 'Vault'))
    parser.add_argument('--check-interval', type=int, default=120)
    parser.add_argument('--dry-run', action='store_true')

    args = parser.parse_args()

    watcher = TwitterWatcher(
        vault_path=args.vault_path,
        check_interval=args.check_interval,
        dry_run=args.dry_run
    )
    watcher.run()


if __name__ == '__main__':
    main()
