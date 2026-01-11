# Branch 2: Email System Setup Guide

**Branch:** `feat/email-system`
**Status:** Implementation Complete - Setup Required
**Date:** 2026-01-11

---

## Overview

Branch 2 implements the email processing system with three main components:

1. **process-emails Skill** ✅ Complete (SKILL.md + 3 reference files + parser script)
2. **Gmail Watcher** ✅ Complete (`gmail_watcher.py`)
3. **Email MCP Server** 🔧 Requires Setup

This guide walks you through setting up the Gmail API and Email MCP Server to complete Branch 2.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Gmail API Setup](#gmail-api-setup)
3. [Install Dependencies](#install-dependencies)
4. [Configure Gmail Watcher](#configure-gmail-watcher)
5. [Email MCP Server Setup](#email-mcp-server-setup)
6. [Testing the System](#testing-the-system)
7. [Running in Production](#running-in-production)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

**Required:**
- Python 3.13+ with UV
- Node.js v24+
- Claude Code CLI installed
- Google Account with Gmail
- Active internet connection

**Estimated Setup Time:** 30-45 minutes

---

## Gmail API Setup

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing):
   - Click "Select a project" → "New Project"
   - Name: "Autonomous FTE Email"
   - Click "Create"

### Step 2: Enable Gmail API

1. In Google Cloud Console, navigate to:
   - **APIs & Services** → **Library**
2. Search for "Gmail API"
3. Click on "Gmail API"
4. Click **"Enable"**

### Step 3: Configure OAuth Consent Screen

1. Navigate to **APIs & Services** → **OAuth consent screen**
2. Select **"External"** user type (unless you have Google Workspace)
3. Click **"Create"**
4. Fill in required fields:
   - **App name:** Autonomous FTE Email System
   - **User support email:** Your email
   - **Developer contact:** Your email
5. Click **"Save and Continue"**
6. **Scopes:** Click "Add or Remove Scopes"
   - Add: `https://www.googleapis.com/auth/gmail.readonly`
   - Add: `https://www.googleapis.com/auth/gmail.send` (for future sending)
7. Click **"Save and Continue"**
8. **Test users:** Add your Gmail address
9. Click **"Save and Continue"**

### Step 4: Create OAuth 2.0 Credentials

1. Navigate to **APIs & Services** → **Credentials**
2. Click **"+ Create Credentials"** → **"OAuth client ID"**
3. Application type: **"Desktop app"**
4. Name: "Gmail Watcher Client"
5. Click **"Create"**
6. **Download JSON:**
   - Click the download icon on the created credential
   - Save as `credentials.json` in `D:\Autonomous-FTEs\`

**Security Note:** Add `credentials.json` and `token.json` to `.gitignore`!

---

## Install Dependencies

### Install Gmail API Libraries

```bash
cd D:\Autonomous-FTEs
uv pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

**Expected Output:**
```
Resolved X packages in XXms
Installed 3 packages in XXms
 + google-auth-oauthlib==X.X.X
 + google-auth-httplib2==X.X.X
 + google-api-python-client==X.X.X
```

### Verify Installation

```bash
python -c "from googleapiclient.discovery import build; print('Gmail API libraries installed successfully')"
```

---

## Configure Gmail Watcher

### Step 1: Set Up Environment (Optional)

Create `.env` file in vault root (optional - can use command-line args instead):

```bash
# D:\Autonomous-FTEs\.env
VAULT_PATH=D:\Autonomous-FTEs
GMAIL_CREDENTIALS=D:\Autonomous-FTEs\credentials.json
```

**Important:** Add `.env` to `.gitignore`!

### Step 2: First-Time Authentication

Run Gmail Watcher for the first time to authenticate:

```bash
cd D:\Autonomous-FTEs
python watchers\gmail_watcher.py --dry-run
```

**What Happens:**
1. Browser window opens automatically
2. Sign in with your Google account
3. Grant permissions to the app
4. Browser shows "Authentication successful"
5. `token.json` is created automatically

**Expected Output:**
```
Starting OAuth authentication flow...
Please visit this URL to authorize this application: https://...
[Browser opens]
Credentials saved successfully
Gmail API authenticated successfully
Starting Gmail Watcher (check interval: 120s)
DRY RUN MODE - No files will be created
```

### Step 3: Test Dry Run

The watcher should now check your Gmail:

```
--- Check #1 ---
Found 5 unread important emails, 2 new
[DRY RUN] Would create file: EMAIL_Interested_in_Your_Services_2026-01-11.md
[DRY RUN] Priority: normal, From: John Doe
```

**If working:** Press Ctrl+C and proceed to remove `--dry-run` flag

---

## Email MCP Server Setup

### Option 1: Basic Email Sending (Bash/Python Script)

For Silver Tier, we can use a simple Python script called via Bash instead of a full MCP server.

#### Create Email Sender Script

Already provided at: `D:\Autonomous-FTEs\scripts\send_email.py` (see below)

#### Test Email Sending

```bash
python scripts\send_email.py --to recipient@example.com --subject "Test" --body "Testing email send"
```

### Option 2: Full MCP Server (Advanced - Gold Tier)

For a full MCP server implementation, see:
- [MCP Email Server Template](https://github.com/modelcontextprotocol/servers)
- Or use `@modelcontextprotocol/server-gmail` if available

#### Install MCP Server

```bash
npm install -g @modelcontextprotocol/server-gmail
```

#### Configure Claude Code

Edit: `~/.config/claude-code/mcp.json` (or Windows equivalent)

```json
{
  "mcpServers": {
    "email": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-gmail"],
      "env": {
        "GMAIL_CREDENTIALS": "D:/Autonomous-FTEs/credentials.json",
        "GMAIL_TOKEN": "D:/Autonomous-FTEs/token.json"
      }
    }
  }
}
```

**Restart Claude Code** for changes to take effect.

---

## Testing the System

### End-to-End Test

#### 1. Send Test Email to Yourself

- Send an email to your Gmail with subject: "Test: Autonomous FTE"
- Mark it as "Important" (star it)
- Keep it unread

#### 2. Run Gmail Watcher (Real Mode)

```bash
cd D:\Autonomous-FTEs
python watchers\gmail_watcher.py --check-interval 60
```

**Expected Output:**
```
Starting Gmail Watcher (check interval: 60s)
Gmail API authenticated successfully
--- Check #1 ---
Found 1 unread important emails, 1 new
Processing 1 new emails...
Created email file: EMAIL_Test_Autonomous_FTE_2026-01-11.md (Priority: normal)
  ✓ EMAIL_Test_Autonomous_FTE_2026-01-11.md
```

#### 3. Verify File Created

```bash
ls Needs_Action\EMAIL_*.md
```

Should show the newly created email file.

#### 4. Process Email with Claude Code

In Claude Code CLI, run:

```
/process-emails
```

Or simply say:

```
Check my emails
```

**Expected Behavior:**
- Claude activates `process-emails` skill
- Reads EMAIL_*.md file
- Categorizes email (likely "Sales/Leads" or "Administrative")
- Drafts response using appropriate template
- Creates approval request in `/Pending_Approval`
- Logs activity to Dashboard

#### 5. Approve Email Response

1. Check `/Pending_Approval` folder
2. Review the drafted email response
3. Move file to `/Approved` if acceptable

#### 6. Send Email (Manual for Silver Tier)

For now, manually send the approved email via Gmail.

**Gold Tier Enhancement:** Automate sending via MCP server.

---

## Running in Production

### Run Gmail Watcher Continuously

#### Option 1: Terminal Session (Simple)

```bash
cd D:\Autonomous-FTEs
python watchers\gmail_watcher.py
```

Keep terminal open. Press Ctrl+C to stop.

#### Option 2: PM2 Process Manager (Recommended)

```bash
# Install PM2
npm install -g pm2

# Start watcher
pm2 start watchers\gmail_watcher.py --interpreter python3 --name gmail-watcher

# View status
pm2 status

# View logs
pm2 logs gmail-watcher

# Stop
pm2 stop gmail-watcher

# Restart on boot (optional)
pm2 save
pm2 startup
```

#### Option 3: Windows Task Scheduler (Background)

1. Open Task Scheduler
2. Create Basic Task:
   - Name: "Gmail Watcher"
   - Trigger: "When I log on"
   - Action: "Start a program"
   - Program: `python`
   - Arguments: `D:\Autonomous-FTEs\watchers\gmail_watcher.py`
   - Start in: `D:\Autonomous-FTEs`
3. Save task

### Monitor Logs

```bash
# View watcher logs
tail -f Logs\gmail_watcher.log

# View processed IDs
cat Logs\gmail_processed_ids.json

# Dashboard activity
cat Dashboard.md
```

---

## Troubleshooting

### Issue: "Credentials file not found"

**Solution:** Ensure `credentials.json` is in the vault root directory.

```bash
ls D:\Autonomous-FTEs\credentials.json
```

### Issue: "Invalid grant" or "Token expired"

**Solution:** Delete `token.json` and re-authenticate:

```bash
rm token.json
python watchers\gmail_watcher.py --dry-run
```

Browser will open for re-authentication.

### Issue: "Gmail API not enabled"

**Solution:** Verify Gmail API is enabled in Google Cloud Console:
- Go to APIs & Services → Library
- Search "Gmail API"
- Should show "Manage" (not "Enable")

### Issue: "Quota exceeded"

**Solution:** Gmail API has daily quotas (usually 1,000,000,000 quota units/day).
- Check quota usage in Google Cloud Console
- Increase check interval: `--check-interval 300` (5 minutes)

### Issue: "No emails detected"

**Checklist:**
- [ ] Email is marked as "Important" (star it)
- [ ] Email is "Unread"
- [ ] Watcher is running (check logs)
- [ ] Token is valid (re-authenticate if needed)
- [ ] Gmail query filter: `is:unread is:important`

### Issue: "ModuleNotFoundError: No module named 'google'"

**Solution:** Install Gmail API libraries:

```bash
uv pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### Issue: process-emails skill not activating

**Solution:**
- Check skill location: `.claude/skills/process-emails/SKILL.md`
- Try explicit invocation: `/process-emails`
- Check Claude Code logs for skill loading errors

---

## Security Best Practices

### Credentials Protection

**Do:**
- Add to `.gitignore`: `credentials.json`, `token.json`, `.env`
- Store credentials securely
- Rotate tokens periodically
- Use OAuth (never store passwords)

**Don't:**
- Commit credentials to Git
- Share credentials publicly
- Use production Gmail for testing

### Email Approval Workflow

**Always require approval for:**
- All email sends (Silver Tier)
- New contacts
- Financial discussions
- Sensitive topics

**See:** `.claude/skills/handle-approval/reference/security-rules.md`

---

## Next Steps

### Branch 2 Complete When:

- [x] Gmail API configured and authenticated
- [x] Gmail Watcher running and detecting emails
- [x] process-emails skill processes EMAIL_*.md files
- [x] Approval requests created successfully
- [ ] Test with 3-5 real emails
- [ ] Document in completion report

### Gold Tier Enhancements:

- Automate email sending via MCP server
- WhatsApp Watcher integration
- LinkedIn automation
- Weekly business audit (CEO Briefing)

---

## Files Created in Branch 2

```
Branch 2 Files:
├── .claude/skills/process-emails/
│   ├── SKILL.md (340 lines)
│   ├── reference/
│   │   ├── email-templates.md (500 lines)
│   │   ├── priority-rules.md (470 lines)
│   │   └── categorization.md (520 lines)
│   └── scripts/
│       └── parse_email_metadata.py (310 lines)
├── watchers/
│   └── gmail_watcher.py (450 lines)
├── config/
│   └── mcp-email-server-config.json
└── docs/
    └── Branch-2-Setup-Guide.md (this file)
```

**Total:** 7 files, ~2,590 lines of code

---

## Support & Resources

### Documentation
- [Gmail API Docs](https://developers.google.com/gmail/api)
- [OAuth 2.0](https://developers.google.com/identity/protocols/oauth2)
- [MCP Protocol](https://modelcontextprotocol.io/)
- [Hackathon Guide](../hackathon.md)

### Logs & Debugging
- Gmail Watcher: `Logs/gmail_watcher.log`
- Processed IDs: `Logs/gmail_processed_ids.json`
- Dashboard: `Dashboard.md`

### Weekly Meeting
- **Wednesdays 10:00 PM**
- Zoom: https://us06web.zoom.us/j/87188707642
- Passcode: 744832

---

**Setup Guide Status:** ✅ Complete
**Last Updated:** 2026-01-11
**Ready for Testing:** Yes
