# LinkedIn API Setup Guide

**Purpose:** Set up LinkedIn posting capability for the `post-to-linkedin` skill

**Estimated Time:** 30-60 minutes (varies by option)

**Target:** Silver Tier hackathon submission or production use

---

## Three Implementation Options

You have **three choices** for LinkedIn integration. Choose based on your situation:

| Option | Setup Time | Reliability | Best For | Hackathon Viable |
|--------|-----------|-------------|----------|------------------|
| **Option 1: Official API** | 60 min | High | Production | ⚠️ Requires company page |
| **Option 2: Unofficial API** | 20 min | Medium | Hackathon/testing | ✅ Yes |
| **Option 3: Browser Automation** | 30 min | Medium | Silver Tier | ✅ Yes (recommended) |

**Recommendation for Hackathon:** Start with **Option 3 (Browser Automation)** - it's the fastest path to a working demo without needing API approval or company pages.

---

## Option 1: LinkedIn Official API (Production-Ready)

### Prerequisites

- LinkedIn account (personal or company)
- **LinkedIn Company Page** (required for posting)
- LinkedIn Developer Account
- Verified app (may require LinkedIn review)

### Step 1: Create LinkedIn Developer App

1. **Go to LinkedIn Developers**
   - Visit: https://www.linkedin.com/developers/
   - Click "Create app"

2. **Fill App Information**
   - **App name:** "Autonomous AI Employee" (or your project name)
   - **LinkedIn Page:** Select your company page
   - **Privacy policy URL:** (required - can be GitHub repo README)
   - **App logo:** Upload any 300x300 image
   - **Legal agreement:** Check and submit

3. **Request Permissions**
   - Go to "Products" tab
   - Request "Share on LinkedIn" product
   - **Note:** May require LinkedIn approval (1-7 days)

### Step 2: Get API Credentials

1. **Auth Tab**
   - Copy "Client ID"
   - Copy "Client Secret"
   - Add redirect URL: `http://localhost:8000/callback`

2. **Store Credentials Securely**
   ```bash
   # Create .env file (already in .gitignore)
   touch .env
   ```

   Add to `.env`:
   ```
   LINKEDIN_CLIENT_ID=your_client_id_here
   LINKEDIN_CLIENT_SECRET=your_client_secret_here
   LINKEDIN_REDIRECT_URI=http://localhost:8000/callback
   ```

### Step 3: Install LinkedIn SDK

```bash
pip install python-linkedin-v2
```

### Step 4: Implement OAuth Flow

Create `scripts/linkedin_oauth.py`:

```python
#!/usr/bin/env python3
"""
LinkedIn OAuth 2.0 Flow
First-time setup to get access token
"""

import os
from pathlib import Path
from linkedin_v2 import LinkedInAuth

def get_linkedin_token():
    """
    Run once to get access token via OAuth 2.0
    Opens browser for user authorization
    """
    # Load credentials
    client_id = os.getenv('LINKEDIN_CLIENT_ID')
    client_secret = os.getenv('LINKEDIN_CLIENT_SECRET')
    redirect_uri = os.getenv('LINKEDIN_REDIRECT_URI')

    # Initialize OAuth
    auth = LinkedInAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri
    )

    # Get authorization URL
    auth_url = auth.get_authorization_url(
        scope=['w_member_social', 'r_liteprofile']
    )

    print("=" * 60)
    print("LinkedIn OAuth Authorization")
    print("=" * 60)
    print("\n1. Open this URL in your browser:")
    print(f"\n{auth_url}\n")
    print("2. Authorize the app")
    print("3. Copy the 'code' parameter from the redirect URL")
    print("=" * 60)

    # Get auth code from user
    auth_code = input("\nPaste the authorization code here: ").strip()

    # Exchange code for access token
    access_token = auth.get_access_token(auth_code)

    # Save token securely
    token_file = Path('Logs/linkedin_token.txt')
    token_file.parent.mkdir(exist_ok=True)
    token_file.write_text(access_token)
    token_file.chmod(0o600)  # Read/write for owner only

    print("\n✓ Access token saved to:", token_file)
    print("✓ LinkedIn API is now configured!")

    return access_token

if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()  # Load .env file
    get_linkedin_token()
```

### Step 5: Update linkedin_api_helper.py

Replace the `_initialize_api` method in `scripts/linkedin_api_helper.py`:

```python
def _initialize_api(self):
    """Initialize LinkedIn API (Official)"""
    from linkedin_v2 import LinkedInAPI

    # Load access token
    token_file = Path('Logs/linkedin_token.txt')
    if not token_file.exists():
        raise FileNotFoundError(
            "LinkedIn token not found. Run: python scripts/linkedin_oauth.py"
        )

    access_token = token_file.read_text().strip()

    # Initialize API
    self.api = LinkedInAPI(access_token=access_token)
    self.api_initialized = True
    logger.info("LinkedIn Official API initialized")
```

Replace the `publish_post` method:

```python
def publish_post(self, content: str, metadata: Optional[Dict] = None) -> Dict:
    """Publish post via Official LinkedIn API"""

    self.validate_post_content(content)

    if self.dry_run:
        # ... existing dry-run code ...
        pass

    # Actual posting
    try:
        response = self.api.submit_share(
            comment=content,
            visibility='PUBLIC'
        )

        post_id = response.get('id', '')
        post_url = f"https://www.linkedin.com/feed/update/urn:li:share:{post_id}"

        return {
            'status': 'success',
            'post_url': post_url,
            'post_id': post_id,
            'timestamp': datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"LinkedIn posting failed: {e}")
        return {
            'status': 'error',
            'error': str(e)
        }
```

### Step 6: First-Time Authorization

```bash
# Run OAuth flow (opens browser)
python scripts/linkedin_oauth.py

# Test posting (dry-run)
python scripts/linkedin_api_helper.py \
  --approval-file "Vault/Approved/APPROVAL_LINKEDIN_test.md" \
  --dry-run

# Actual posting
python scripts/linkedin_api_helper.py \
  --approval-file "Vault/Approved/APPROVAL_LINKEDIN_test.md"
```

---

## Option 2: Unofficial LinkedIn API (Hackathon-Friendly)

### Prerequisites

- LinkedIn personal account
- LinkedIn credentials (email + password)

### Step 1: Install Unofficial Library

```bash
pip install linkedin-api
```

### Step 2: Store Credentials

Add to `.env`:
```
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_linkedin_password
```

### Step 3: Update linkedin_api_helper.py

Replace `_initialize_api`:

```python
def _initialize_api(self):
    """Initialize LinkedIn API (Unofficial)"""
    from linkedin_api import Linkedin

    # Load credentials
    email = os.getenv('LINKEDIN_EMAIL')
    password = os.getenv('LINKEDIN_PASSWORD')

    if not email or not password:
        raise ValueError("LinkedIn credentials not found in .env")

    # Session-based auth
    self.api = Linkedin(email, password)
    self.api_initialized = True
    logger.info("LinkedIn Unofficial API initialized")
```

Replace `publish_post`:

```python
def publish_post(self, content: str, metadata: Optional[Dict] = None) -> Dict:
    """Publish post via Unofficial LinkedIn API"""

    self.validate_post_content(content)

    if self.dry_run:
        # ... existing dry-run code ...
        pass

    # Actual posting
    try:
        response = self.api.submit_share(
            text=content,
            visibility='PUBLIC'
        )

        # Note: Unofficial API might not return direct post URL
        return {
            'status': 'success',
            'post_url': 'https://www.linkedin.com/feed/',
            'timestamp': datetime.now().isoformat(),
            'note': 'Check LinkedIn feed to see post'
        }

    except Exception as e:
        logger.error(f"LinkedIn posting failed: {e}")
        return {
            'status': 'error',
            'error': str(e)
        }
```

### Step 4: Test

```bash
# Load environment variables
export $(cat .env | xargs)  # Linux/Mac
# OR manually set in Windows Command Prompt

# Test (dry-run)
python scripts/linkedin_api_helper.py \
  --approval-file "Vault/Approved/APPROVAL_LINKEDIN_test.md" \
  --dry-run

# Actual posting
python scripts/linkedin_api_helper.py \
  --approval-file "Vault/Approved/APPROVAL_LINKEDIN_test.md"
```

### ⚠️ Security Warning

- Unofficial API uses username/password (not OAuth)
- LinkedIn may flag unusual activity
- Use only for testing/hackathon
- Migrate to Official API for production

---

## Option 3: Browser Automation (Recommended for Hackathon)

### Prerequisites

- LinkedIn personal account
- Playwright or Selenium

### Step 1: Install Playwright

```bash
pip install playwright
playwright install chromium
```

### Step 2: First-Time Login (Create Session)

```bash
# Run Playwright in non-headless mode (one time)
python scripts/linkedin_browser_auth.py
```

Create `scripts/linkedin_browser_auth.py`:

```python
#!/usr/bin/env python3
"""
LinkedIn Browser Authentication
Run once to create persistent session
"""

from playwright.sync_api import sync_playwright
from pathlib import Path

def create_linkedin_session():
    """
    Opens LinkedIn in browser for manual login
    Creates persistent session for future automation
    """
    session_dir = Path('linkedin_session')

    with sync_playwright() as p:
        print("=" * 60)
        print("LinkedIn Browser Login")
        print("=" * 60)
        print("\n1. Browser will open to LinkedIn login page")
        print("2. Log in with your credentials")
        print("3. Close browser when done")
        print("\nNOTE: Session will be saved for future automated use")
        print("=" * 60)
        input("\nPress Enter to continue...")

        # Launch browser with persistent context (saves cookies)
        browser = p.chromium.launch_persistent_context(
            user_data_dir=str(session_dir),
            headless=False,  # Visible browser
            viewport={'width': 1280, 'height': 720}
        )

        page = browser.new_page()
        page.goto('https://www.linkedin.com/login')

        print("\n✓ Browser opened - please log in")
        print("✓ After logging in, close the browser window")

        # Wait for user to manually log in and close
        try:
            page.wait_for_timeout(600000)  # 10 minutes max
        except:
            pass

        browser.close()

    if session_dir.exists():
        print("\n✓ LinkedIn session saved to:", session_dir)
        print("✓ Future automation will use this session")
    else:
        print("\n✗ Session not created - please try again")

if __name__ == '__main__':
    create_linkedin_session()
```

Run once:
```bash
python scripts/linkedin_browser_auth.py
# Log in manually, then close browser
```

### Step 3: Update linkedin_api_helper.py

Replace `_initialize_api`:

```python
def _initialize_api(self):
    """Initialize LinkedIn via Browser Automation"""
    from playwright.sync_api import sync_playwright

    session_dir = Path('linkedin_session')

    if not session_dir.exists():
        raise FileNotFoundError(
            "LinkedIn session not found. Run: python scripts/linkedin_browser_auth.py"
        )

    # Initialize Playwright
    self.playwright = sync_playwright().start()
    self.browser = self.playwright.chromium.launch_persistent_context(
        user_data_dir=str(session_dir),
        headless=True,  # Run in background
        viewport={'width': 1280, 'height': 720}
    )
    self.page = self.browser.new_page()

    # Navigate to LinkedIn
    self.page.goto('https://www.linkedin.com/feed/')

    # Check if logged in (look for profile link)
    try:
        self.page.wait_for_selector('[data-control-name="identity_profile_photo"]', timeout=5000)
        self.api_initialized = True
        logger.info("LinkedIn browser automation initialized")
    except:
        logger.error("Not logged in - run: python scripts/linkedin_browser_auth.py")
        self.api_initialized = False
        raise RuntimeError("LinkedIn authentication failed")
```

Replace `publish_post`:

```python
def publish_post(self, content: str, metadata: Optional[Dict] = None) -> Dict:
    """Publish post via Browser Automation"""

    self.validate_post_content(content)

    if self.dry_run:
        # ... existing dry-run code ...
        pass

    # Actual posting via browser
    try:
        # Navigate to feed if not already there
        if 'linkedin.com/feed' not in self.page.url:
            self.page.goto('https://www.linkedin.com/feed/')

        # Click "Start a post"
        self.page.click('button[aria-label="Start a post"]')
        self.page.wait_for_selector('.ql-editor', timeout=5000)

        # Type content
        self.page.fill('.ql-editor', content)

        # Wait a moment for UI to update
        self.page.wait_for_timeout(1000)

        # Click "Post" button
        self.page.click('button[aria-label="Post"]')

        # Wait for success confirmation
        try:
            self.page.wait_for_selector('text=Post successful', timeout=10000)
        except:
            # Some LinkedIn versions don't show this exact text
            self.page.wait_for_timeout(3000)

        # Can't get direct post URL easily with automation
        return {
            'status': 'success',
            'post_url': 'https://www.linkedin.com/feed/',
            'timestamp': datetime.now().isoformat(),
            'note': 'Post published - check LinkedIn feed to confirm'
        }

    except Exception as e:
        logger.error(f"LinkedIn browser posting failed: {e}")

        # Take screenshot for debugging
        screenshot_path = Path('Logs/linkedin_error.png')
        self.page.screenshot(path=str(screenshot_path))

        return {
            'status': 'error',
            'error': str(e),
            'screenshot': str(screenshot_path)
        }
```

### Step 4: Test

```bash
# Test (dry-run)
python scripts/linkedin_api_helper.py \
  --approval-file "Vault/Approved/APPROVAL_LINKEDIN_test.md" \
  --dry-run

# Actual posting (browser runs in background)
python scripts/linkedin_api_helper.py \
  --approval-file "Vault/Approved/APPROVAL_LINKEDIN_test.md"
```

### Advantages of Browser Automation

- ✅ No API keys needed
- ✅ No LinkedIn Developer Account needed
- ✅ No company page required
- ✅ Works with personal LinkedIn accounts
- ✅ Fast setup (~30 minutes)
- ✅ Good for hackathon/demo

### Disadvantages

- ⚠️ Slower than API calls
- ⚠️ Fragile (breaks if LinkedIn UI changes)
- ⚠️ Requires session maintenance
- ⚠️ Not ideal for production at scale

---

## Security Best Practices (All Options)

### 1. Protect Credentials

```bash
# .env file should NEVER be committed
# Verify it's in .gitignore
grep ".env" .gitignore

# File permissions (Linux/Mac)
chmod 600 .env
chmod 700 linkedin_session/  # If using Option 3

# Windows: Right-click → Properties → Security → Advanced
```

### 2. Add to .gitignore

Ensure these lines are in `.gitignore`:

```
# LinkedIn credentials
.env
linkedin_session/
Logs/linkedin_token.txt
Logs/linkedin_error.png

# Python
__pycache__/
*.pyc
```

### 3. Rotate Credentials

- **Option 1 (Official API):** Regenerate tokens every 60-90 days
- **Option 2 (Unofficial):** Change password periodically
- **Option 3 (Browser):** Re-authenticate monthly

### 4. Rate Limiting

LinkedIn has posting limits:
- **Personal accounts:** ~10-20 posts per day
- **Company pages:** Higher limits

Don't exceed these limits or risk account restrictions.

---

## Testing Checklist

### Pre-Production Testing

- [ ] **Dry-run test passes**
  ```bash
  python scripts/linkedin_api_helper.py --dry-run --approval-file "path"
  ```

- [ ] **Parse approval file correctly**
  - Extracts post content
  - Validates platform = linkedin
  - Reads metadata

- [ ] **Character count validation**
  - Rejects posts > 3000 chars
  - Warns if > 10 hashtags

- [ ] **Authentication works**
  - API credentials valid (Option 1)
  - Login session active (Option 2, 3)
  - No error messages

- [ ] **Actual posting test**
  - Create test approval file
  - Move to /Approved
  - Run script (no dry-run)
  - Verify post appears on LinkedIn

- [ ] **Dashboard logging**
  - Check Dashboard.md updated
  - Timestamp correct
  - Status logged

### Troubleshooting

**Issue:** "LinkedIn session not found"
- **Fix:** Run `python scripts/linkedin_browser_auth.py` (Option 3)

**Issue:** "Authentication failed"
- **Fix Option 1:** Re-run `python scripts/linkedin_oauth.py`
- **Fix Option 2:** Check .env credentials
- **Fix Option 3:** Delete `linkedin_session/` and re-login

**Issue:** "Post not appearing on LinkedIn"
- **Check 1:** Visit https://www.linkedin.com/feed/ directly
- **Check 2:** May take 1-2 minutes to appear
- **Check 3:** Check script output for error messages

**Issue:** "Character limit exceeded"
- **Fix:** Edit approval file content (keep under 3000 chars)

---

## Integration with post-to-linkedin Skill

Once LinkedIn API is configured, the skill workflow is:

```
1. User: "Create LinkedIn post about [topic]"
   ↓
2. post-to-linkedin skill activates
   ↓
3. Generates content, creates approval request
   ↓
4. Human approves → Moves to /Approved
   ↓
5. Orchestrator detects /Approved file
   ↓
6. Calls: python scripts/linkedin_api_helper.py --approval-file "path"
   ↓
7. linkedin_api_helper.py publishes via chosen method
   ↓
8. Post appears on LinkedIn ✓
   ↓
9. Dashboard.md updated with success log
```

---

## Option Comparison Matrix

| Feature | Option 1 (Official) | Option 2 (Unofficial) | Option 3 (Browser) |
|---------|--------------------|-----------------------|--------------------|
| **Setup Time** | 60 min | 20 min | 30 min |
| **Company Page Required** | ✅ Yes | ❌ No | ❌ No |
| **API Approval Needed** | ✅ Yes (1-7 days) | ❌ No | ❌ No |
| **Reliability** | High | Medium | Medium |
| **Speed** | Fast | Fast | Slow |
| **Production Ready** | ✅ Yes | ⚠️ Risky | ⚠️ No |
| **Hackathon Ready** | ⚠️ Maybe | ✅ Yes | ✅ Yes |
| **Cost** | Free (rate limits) | Free | Free |
| **Maintenance** | Low | Medium | High |

---

## Recommendation by Use Case

### For Hackathon Demo (This Weekend)
→ **Option 3: Browser Automation**
- Fastest to working demo
- No API approval wait
- Works with personal account

### For Silver Tier Submission
→ **Option 3: Browser Automation**
- Meets requirements
- Dry-run mode for demo
- Can show in video

### For Production Use (Post-Hackathon)
→ **Option 1: Official API**
- Most reliable
- Proper authentication
- Scalable
- LinkedIn approved

### For Quick Testing/Development
→ **Option 2: Unofficial API**
- Fast setup
- No company page
- Good for iteration

---

## Next Steps

### After LinkedIn Setup

1. **Test End-to-End**
   ```bash
   # In Claude Code:
   "Create a LinkedIn post about completing the Silver Tier hackathon"

   # Review approval file in /Pending_Approval
   # Move to /Approved
   # Check Dashboard for success log
   # Verify post on LinkedIn
   ```

2. **Create Demo Video**
   - Follow: `dev_docs/DEMO-VIDEO-SCRIPT.md`
   - Show LinkedIn post generation workflow
   - Highlight approval process

3. **Prepare Submission**
   - Update README with "LinkedIn ✅ Configured"
   - Include setup choice in documentation
   - Mention in hackathon submission form

---

## Support

**Issues?**
- Check Logs/linkedin_helper.log for errors
- Run with --json flag for detailed output
- Test with --dry-run first
- Take screenshots of errors

**Still stuck?**
- Review this guide carefully
- Check LinkedIn API status
- Try different browser (Option 3)
- Ask in Wednesday research meeting

---

*Good luck with your LinkedIn integration!* 🚀
