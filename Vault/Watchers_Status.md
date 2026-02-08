# Watchers Status

Last updated: 2026-02-07

## Active Watchers

| Watcher | Status | Account | Check Interval | Log File |
|---------|--------|---------|----------------|----------|
| Filesystem | Running | Vault/Inbox/ | Instant | Logs/filesystem_watcher.log |
| Gmail | Running | aimoshahs@gmail.com | 60s | Logs/gmail_watcher.log |
| Twitter | Running | @stelalvna | 120s | Logs/twitter_watcher.log |
| LinkedIn | Running | umayaimanshah@gmail.com | 300s | Logs/linkedin_watcher.log |
| WhatsApp | Pending QR Scan | - | 60s | Logs/whatsapp_watcher.log |

## How to Start Watchers

```bash
# Navigate to project directory
cd "C:\Users\LENOVO X1 YOGA\Desktop\Autonomous-FTEs"

# Start Filesystem Watcher
python watchers/filesystem_watcher.py --vault-path Vault

# Start Gmail Watcher (uses .env credentials)
python watchers/gmail_watcher.py --vault-path Vault --check-interval 60

# Start Twitter Watcher (uses .env credentials)
python watchers/twitter_watcher.py --vault-path Vault --check-interval 120

# Start LinkedIn Watcher (visible browser for login)
python watchers/linkedin_watcher.py --vault-path Vault --check-interval 300 --no-headless

# Start WhatsApp Watcher (requires QR scan first time)
python watchers/whatsapp_watcher.py --vault-path Vault --check-interval 60
```

## What Each Watcher Does

### Filesystem Watcher
- Monitors `Vault/Inbox/` folder
- When you drop a file, it moves to `Vault/Needs_Action/`
- Creates a metadata `.md` file for processing

### Gmail Watcher
- Connects via IMAP using credentials in `.env`
- Checks for unread emails every 60 seconds
- Creates `EMAIL_*.md` files in `Needs_Action/`
- Tracks processed emails to avoid duplicates

### Twitter Watcher
- Connects via Twitter API using credentials in `.env`
- Monitors mentions of @stelalvna
- Creates `TWITTER_MENTION_*.md` files in `Needs_Action/`

### LinkedIn Watcher
- Uses Playwright browser automation
- Monitors notifications, messages, and connection requests
- Creates `LINKEDIN_*.md` files in `Needs_Action/`
- Saves cookies for future sessions

### WhatsApp Watcher
- Uses Playwright with WhatsApp Web
- Requires QR code scan on first run
- Monitors unread messages
- Creates `WHATSAPP_*.md` files in `Needs_Action/`

## Output Folders

- **Needs_Action/** - Items awaiting processing
- **Pending_Approval/** - Items needing human approval
- **Approved/** - Approved actions ready to execute
- **Rejected/** - Rejected actions
- **Done/** - Completed items
- **Logs/** - Watcher log files

## Processed Items Tracking

Each watcher tracks processed IDs to avoid duplicates:
- `Logs/gmail_processed_ids.json`
- `Logs/twitter_processed_ids.json`
- `Logs/linkedin_processed_ids.json`
- `Logs/whatsapp_processed_ids.json`

## Statistics (Current Session)

- **Emails processed:** 70+
- **Twitter mentions:** 20
- **LinkedIn items:** Monitoring
- **WhatsApp messages:** Pending QR scan
- **Files dropped:** 1 (test)

---

*This file is auto-generated. Open in Obsidian to view and track watcher activity.*
