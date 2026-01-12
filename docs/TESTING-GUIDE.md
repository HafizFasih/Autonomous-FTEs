# Testing Guide: Autonomous FTE System

**System:** Autonomous FTE - Personal AI Employee (Gold Tier)
**Version:** 1.0
**Last Updated:** January 12, 2026
**Purpose:** Comprehensive testing procedures for validation and verification

---

## Overview

This guide provides systematic testing procedures to verify all components of the Autonomous FTE system are functioning correctly. Use this guide for:
- Initial system validation after setup
- Post-update verification
- Troubleshooting specific components
- Pre-submission testing for hackathon

**Testing Philosophy:**
- Test end-to-end workflows, not just individual components
- Test error scenarios, not just happy paths
- Verify automation, not just manual triggers
- Document all test results

---

## Table of Contents

1. [Pre-Test Setup](#pre-test-setup)
2. [Unit Tests (Component-Level)](#unit-tests-component-level)
3. [Integration Tests (Skill-Level)](#integration-tests-skill-level)
4. [End-to-End Tests (System-Level)](#end-to-end-tests-system-level)
5. [Chaos Engineering Tests](#chaos-engineering-tests)
6. [Performance Tests](#performance-tests)
7. [Security Tests](#security-tests)
8. [7-Day Burn-In Test](#7-day-burn-in-test)
9. [Test Results Template](#test-results-template)

---

## Pre-Test Setup

### Testing Environment Preparation

**1. Create Test Data**
```bash
# Create test folder in vault
mkdir -p Vault/Testing/
mkdir -p Vault/Testing/test_inputs/
mkdir -p Vault/Testing/test_outputs/
```

**2. Enable Test Mode (Optional)**
```bash
# Set environment variable to prevent real actions during testing
export DRY_RUN=true
```

**3. Backup Current State**
```bash
# Backup vault before testing
tar -czf vault_backup_pre_test.tar.gz AI_Employee_Vault/
```

**4. Test Accounts Setup**
- Gmail: Use test label or separate test account
- Social media: Use test pages/accounts (recommended)
- Xero: Use demo company (not production)

**5. Document Baseline**
```bash
# Capture baseline health score
python3 .claude/skills/monitor-system/scripts/health_monitor.py > baseline_health.txt
```

---

## Unit Tests (Component-Level)

### Test 1: Watcher Process Verification

**Purpose:** Verify each Watcher process starts, runs, and monitors correctly

#### 1.1 Gmail Watcher

**Test Steps:**
```bash
# Start watcher
python3 watchers/gmail_watcher.py &
WATCHER_PID=$!

# Wait 10 seconds
sleep 10

# Verify process running
ps -p $WATCHER_PID

# Verify PID file created
cat /tmp/gmail_watcher.pid

# Verify heartbeat file exists and is recent
ls -la /tmp/gmail_watcher_heartbeat
```

**Expected Results:**
- ✅ Process starts successfully
- ✅ PID file created with correct PID
- ✅ Heartbeat file exists and updates every 5 minutes
- ✅ Process continues running (check after 5 minutes)

**Pass Criteria:** All 4 checks pass

---

#### 1.2 WhatsApp Watcher

**Test Steps:**
```bash
python3 watchers/whatsapp_watcher.py &
# Verify similar to Gmail watcher
```

**Expected Results:**
- ✅ Process starts and runs
- ✅ PID and heartbeat files created
- ✅ Monitors WhatsApp Web (if configured)

**Pass Criteria:** Process stable for >10 minutes

---

#### 1.3 Other Watchers

**Repeat for:**
- LinkedIn Watcher
- Finance Watcher
- Filesystem Watcher

**Overall Pass Criteria:** All 5 Watchers running simultaneously without conflicts

---

### Test 2: MCP Server Connectivity

**Purpose:** Verify all MCP servers are accessible and responding

#### 2.1 Email MCP

**Test Steps:**
```bash
# List available MCP servers
claude-code mcp list | grep email

# Test email MCP functionality (dry run)
claude-code "test email mcp connection"
```

**Expected Results:**
- ✅ Email MCP appears in server list
- ✅ Server responds to health check
- ✅ Can authenticate with Gmail

**Pass Criteria:** Server responds within 5 seconds

---

#### 2.2 Xero MCP

**Test Steps:**
```bash
claude-code mcp list | grep xero
claude-code "test xero connection"
```

**Expected Results:**
- ✅ Xero MCP appears in list
- ✅ Server responds
- ✅ Can authenticate with Xero
- ✅ Can fetch recent transactions

**Pass Criteria:** Returns sample data

---

#### 2.3 Social Media MCP

**Test Steps:**
```bash
claude-code mcp list | grep social
claude-code "test social media mcp"
```

**Expected Results:**
- ✅ Social media MCP appears
- ✅ Facebook API reachable
- ✅ Instagram API reachable
- ✅ Twitter API reachable
- ✅ LinkedIn API reachable

**Pass Criteria:** All 4 platforms respond

---

### Test 3: Health Monitor

**Purpose:** Verify health monitoring calculates scores correctly

**Test Steps:**
```bash
# Run health monitor
python3 .claude/skills/monitor-system/scripts/health_monitor.py

# Check output
cat Vault/System_Status.md

# Verify score calculation
grep "health_score" Vault/Logs/system/health_checks.json | tail -1
```

**Expected Results:**
- ✅ Health check completes without errors
- ✅ Score is between 0-100
- ✅ Component scores add up to total
- ✅ System_Status.md updated
- ✅ JSON log entry created

**Test Scenarios:**

**Scenario A: All Healthy**
- All processes running
- Expected score: 95-100

**Scenario B: One Watcher Down**
- Kill one watcher: `kill $(cat /tmp/gmail_watcher.pid)`
- Expected score: ~88 (100 - 6 - 6 for related impacts)

**Scenario C: MCP Server Down**
- Stop an MCP server
- Expected score: ~75 (100 - 25)

**Pass Criteria:** Score accurately reflects system state

---

### Test 4: Error Handler

**Purpose:** Verify error detection and classification

**Test Steps:**
```bash
# Create synthetic error in log
echo '{
  "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%S)'Z",
  "log_type": "system",
  "event_type": "process_crash",
  "severity": "HIGH",
  "error_code": "PROC_CRASH",
  "component": "test_watcher"
}' >> Vault/Logs/system/$(date +%Y-%m-%d).json

# Run error handler
python3 .claude/skills/monitor-system/scripts/error_handler.py
```

**Expected Results:**
- ✅ Error detected in logs
- ✅ Error classified correctly (HIGH severity)
- ✅ Recovery procedure attempted
- ✅ Recovery logged

**Pass Criteria:** Error handler processes without crashing

---

### Test 5: Watchdog Manager

**Purpose:** Verify process restart functionality

**Test Steps:**
```bash
# Start a watcher
python3 watchers/gmail_watcher.py &
WATCHER_PID=$(cat /tmp/gmail_watcher.pid)

# Kill the process
kill $WATCHER_PID

# Wait 30 seconds
sleep 30

# Run watchdog
python3 .claude/skills/monitor-system/scripts/watchdog_manager.py

# Verify process restarted
ps aux | grep gmail_watcher
```

**Expected Results:**
- ✅ Watchdog detects crashed process
- ✅ Process restart attempted
- ✅ New PID file created
- ✅ Process running after restart
- ✅ Incident logged

**Pass Criteria:** Process restarted within 2 minutes

---

### Test 6: Log Aggregator

**Purpose:** Verify log rotation and compression

**Test Steps:**
```bash
# Create old log files for testing
touch -t 202501010000 Vault/Logs/actions/2025-01-01.json

# Run log aggregator
python3 .claude/skills/monitor-system/scripts/log_aggregator.py

# Verify compression
ls -la Vault/Logs/actions/ | grep ".gz"

# Verify statistics generated
cat Vault/Logs/log_stats.md
```

**Expected Results:**
- ✅ Old logs compressed
- ✅ New daily logs created
- ✅ Statistics report generated
- ✅ Retention policies enforced

**Pass Criteria:** Old files compressed, stats accurate

---

## Integration Tests (Skill-Level)

### Test 7: handle-approval Skill

**Purpose:** Verify approval workflow end-to-end

**Test Steps:**
```bash
# Create test approval request
cat > Vault/Pending_Approval/TEST_approval.md <<'EOF'
---
type: test_approval
action: test_action
---

This is a test approval request.
Move to /Approved/ to approve.
EOF

# Trigger approval handling
claude-code "check pending approvals"

# Move to approved
mv Vault/Pending_Approval/TEST_approval.md Vault/Approved/

# Verify handling
claude-code "process approved items"
```

**Expected Results:**
- ✅ Approval request detected
- ✅ Approval file moved correctly
- ✅ Action executed (or logged in dry-run)
- ✅ File moved to /Done/

**Pass Criteria:** Workflow completes without errors

---

### Test 8: process-emails Skill

**Purpose:** Verify email processing end-to-end

**Test Steps:**
```bash
# Send test email to yourself with urgent keyword
# Subject: "URGENT: Test Email"
# Body: "This is a test. Please reply with status."

# Wait for watcher to detect (max 10 minutes)

# Verify email file created
ls -la Vault/Needs_Action/ | grep EMAIL

# Trigger processing
claude-code "process emails"

# Verify response draft created or approval requested
ls -la Vault/Pending_Approval/ | grep EMAIL
```

**Expected Results:**
- ✅ Email detected by watcher
- ✅ File created in Needs_Action
- ✅ Claude processes email
- ✅ Response draft created
- ✅ Approval requested (if applicable)

**Pass Criteria:** Email processed within 15 minutes of receipt

---

### Test 9: post-to-linkedin Skill

**Purpose:** Verify LinkedIn posting workflow

**Test Steps:**
```bash
# Trigger LinkedIn post creation
claude-code "create linkedin post about AI automation"

# Verify approval request created
ls -la Vault/Pending_Approval/ | grep LINKEDIN

# Approve post
mv Vault/Pending_Approval/POST_LINKEDIN_*.md Vault/Approved/

# Verify post published
# (Check LinkedIn manually or via API)
```

**Expected Results:**
- ✅ Post content generated
- ✅ Approval request created
- ✅ Post published after approval
- ✅ Engagement metrics tracked

**Pass Criteria:** Post appears on LinkedIn within 5 minutes of approval

---

### Test 10: manage-accounting Skill

**Purpose:** Verify Xero integration

**Test Steps:**
```bash
# Trigger transaction sync
claude-code "sync xero transactions"

# Verify transactions synced
cat Vault/Accounting/Current_Month.md

# Check categorization
grep "category" Vault/Accounting/Current_Month.md
```

**Expected Results:**
- ✅ Transactions synced from Xero
- ✅ Current_Month.md updated
- ✅ Expenses categorized (>80% accuracy)
- ✅ Revenue tracked
- ✅ Dashboard updated

**Pass Criteria:** All recent transactions appear in vault

---

### Test 11: post-to-social-media Skill

**Purpose:** Verify Facebook & Instagram posting

**Test Steps:**
```bash
# Trigger social media post
claude-code "create social media post about business update"

# Verify approval requests for both platforms
ls -la Vault/Pending_Approval/ | grep -E "FACEBOOK|INSTAGRAM"

# Approve both
mv Vault/Pending_Approval/POST_FACEBOOK_*.md Vault/Approved/
mv Vault/Pending_Approval/POST_INSTAGRAM_*.md Vault/Approved/

# Verify posts published
# (Check Facebook Page and Instagram manually)
```

**Expected Results:**
- ✅ Content optimized for each platform
- ✅ Facebook: 40-80 words
- ✅ Instagram: High-res image + caption
- ✅ Both posts published
- ✅ Engagement tracked

**Pass Criteria:** Both posts live within 5 minutes

---

### Test 12: post-to-twitter Skill

**Purpose:** Verify Twitter posting

**Test Steps:**
```bash
# Trigger tweet creation
claude-code "create twitter post about AI insights"

# Verify approval request
ls -la Vault/Pending_Approval/ | grep TWITTER

# Approve and publish
mv Vault/Pending_Approval/POST_TWITTER_*.md Vault/Approved/
```

**Expected Results:**
- ✅ Tweet within 280 characters
- ✅ 1-2 hashtags max
- ✅ Published after approval
- ✅ Engagement tracked

**Pass Criteria:** Tweet appears within 5 minutes

---

### Test 13: generate-ceo-briefing Skill

**Purpose:** Verify weekly business audit

**Test Steps:**
```bash
# Manually trigger briefing (don't wait for Sunday)
claude-code "generate weekly briefing"

# Verify briefing created
ls -la Vault/Briefings/ | head -5

# Review briefing content
cat Vault/Briefings/[latest].md
```

**Expected Results:**
- ✅ Briefing file created
- ✅ Financial data included
- ✅ Operational metrics included
- ✅ Social media analytics included
- ✅ Proactive recommendations present
- ✅ Formatted correctly

**Pass Criteria:** Briefing contains all 5 analysis sections

---

### Test 14: monitor-system Skill

**Purpose:** Verify system monitoring integration

**Test Steps:**
```bash
# Check system status
claude-code "check system status"

# Verify response includes:
# - Current health score
# - Component status
# - Recent issues
```

**Expected Results:**
- ✅ Health score retrieved
- ✅ Component breakdown provided
- ✅ Issues summarized
- ✅ Recommendations given

**Pass Criteria:** Accurate status report generated

---

## End-to-End Tests (System-Level)

### Test 15: Complete Email Workflow

**Purpose:** Test entire email lifecycle

**Workflow:**
1. Send urgent email to yourself
2. Gmail Watcher detects email (<10 min)
3. Claude processes and drafts reply
4. Approval request created
5. User approves
6. Email sent via Email MCP
7. Action logged
8. Dashboard updated
9. Files moved to Done

**Test Steps:**
```bash
# 1. Send test email with "URGENT" in subject

# 2-3. Wait for detection and processing
watch -n 30 'ls -la Vault/Needs_Action/'

# 4-5. Approve when ready
ls -la Vault/Pending_Approval/
mv Vault/Pending_Approval/EMAIL_*.md Vault/Approved/

# 6-9. Verify completion
tail -f Vault/Logs/actions/$(date +%Y-%m-%d).json
```

**Expected Timeline:**
- Detection: <10 minutes
- Processing: <3 minutes
- Approval: Manual (user-dependent)
- Send: <1 minute
- **Total (excluding approval): <15 minutes**

**Pass Criteria:** Complete workflow without errors

---

### Test 16: Multi-Platform Social Media Day

**Purpose:** Test all 4 platforms posting in sequence

**Workflow:**
- 9:00 AM: LinkedIn post created → approved → published
- 10:00 AM: Facebook + Instagram posts → approved → published
- 11:00 AM: Twitter post → approved → published

**Test Steps:**
```bash
# Manually trigger all posts
claude-code "create all social media posts for today"

# Approve all
mv Vault/Pending_Approval/POST_*.md Vault/Approved/

# Verify all published
# Check each platform manually
```

**Expected Results:**
- ✅ 4 platform-optimized posts created
- ✅ All posts approved
- ✅ LinkedIn published
- ✅ Facebook published
- ✅ Instagram published
- ✅ Twitter published
- ✅ Engagement tracking initiated

**Pass Criteria:** All 4 posts live within 1 hour

---

### Test 17: Weekly Business Cycle

**Purpose:** Simulate full weekly business operations

**Test Steps:**

**Monday Morning:**
```bash
# Check CEO briefing generated Sunday night
cat Vault/Briefings/$(date +%Y-%m-%d)_Monday_Briefing.md
```

**Mid-Week:**
```bash
# Process test transactions
# Send test emails
# Create test tasks
```

**Sunday Evening:**
```bash
# Verify data collection over week
# Trigger briefing generation
claude-code "generate weekly briefing"
```

**Verification:**
```bash
# Briefing should include:
# - Financial data from Xero
# - Task completion from Done folder
# - Social metrics from all platforms
# - Proactive recommendations
```

**Pass Criteria:** Complete weekly cycle simulated successfully

---

## Chaos Engineering Tests

### Test 18: Process Crash Recovery

**Purpose:** Verify auto-recovery from process crashes

**Test Scenarios:**

**Scenario A: Single Process Crash**
```bash
# Kill Gmail Watcher
kill $(cat /tmp/gmail_watcher.pid)

# Wait for watchdog (runs every 5 min)
# Or manually trigger
python3 .claude/skills/monitor-system/scripts/watchdog_manager.py

# Verify restart
ps aux | grep gmail_watcher
```

**Expected:** Process restarted within 2 minutes

---

**Scenario B: Multiple Process Crashes**
```bash
# Kill all Watchers
pkill -f watcher

# Trigger recovery
python3 .claude/skills/monitor-system/scripts/watchdog_manager.py

# Verify all restarted
ps aux | grep watcher | wc -l  # Should be 5
```

**Expected:** All 5 processes restarted

---

**Scenario C: Crash Loop (Bad Config)**
```bash
# Introduce config error
mv watchers/config/gmail_config.json watchers/config/gmail_config.json.bak

# Start watcher (will crash)
python3 watchers/gmail_watcher.py &

# Watchdog attempts restart 3 times
# After 3 failures, should escalate

# Verify escalation
ls -la Vault/Needs_Action/ | grep ALERT
```

**Expected:** Alert created after 3 failed attempts

---

### Test 19: Network Outage

**Purpose:** Verify graceful degradation during network issues

**Test Steps:**
```bash
# Simulate network outage (disconnect WiFi or block traffic)

# Attempt operations
claude-code "sync xero transactions"  # Should queue
claude-code "post to linkedin"  # Should queue

# Verify queuing
cat Vault/Logs/system/operation_queue.json

# Restore network

# Verify queued operations process
# (After 5-10 minutes, operations should retry)
```

**Expected Results:**
- ✅ Operations queued during outage
- ✅ No crashes or errors
- ✅ Operations retry when network restored
- ✅ All queued operations complete

**Pass Criteria:** Zero data loss during outage

---

### Test 20: Disk Space Exhaustion

**Purpose:** Verify handling of low disk space

**Test Steps:**
```bash
# Check current disk usage
df -h

# Fill disk to <10% free (carefully!)
# Or mock low disk space in health monitor

# Trigger health check
python3 .claude/skills/monitor-system/scripts/health_monitor.py

# Verify cleanup triggered
python3 .claude/skills/monitor-system/scripts/log_aggregator.py

# Check space freed
df -h
```

**Expected Results:**
- ✅ Low disk space detected
- ✅ Cleanup automatically triggered
- ✅ Old logs compressed
- ✅ Space freed (>5%)
- ✅ Alert created if cleanup insufficient

**Pass Criteria:** Automatic cleanup frees adequate space

---

## Performance Tests

### Test 21: Load Testing - Email Volume

**Purpose:** Verify system handles high email volume

**Test Steps:**
```bash
# Send 50 test emails rapidly

# Monitor processing
watch -n 10 'ls Vault/Needs_Action/ | wc -l'

# Track processing rate
# Time how long to process all 50 emails
```

**Expected Results:**
- ✅ All 50 emails detected
- ✅ Processing starts within 10 minutes
- ✅ All emails processed within 2 hours
- ✅ No crashes or errors
- ✅ Average processing time: <3 min/email

**Pass Criteria:** 50 emails processed in <2 hours

---

### Test 22: Concurrent Operations

**Purpose:** Test system under concurrent load

**Test Steps:**
```bash
# Trigger multiple operations simultaneously
claude-code "sync xero transactions" &
claude-code "create linkedin post" &
claude-code "process emails" &
claude-code "check system status" &

# Monitor system load
top

# Verify all complete
wait
```

**Expected Results:**
- ✅ All operations start
- ✅ No resource exhaustion
- ✅ All operations complete successfully
- ✅ Response times acceptable (<5 min each)

**Pass Criteria:** 4 concurrent operations handled without issues

---

### Test 23: Long-Running Stability

**Purpose:** Verify system stability over extended period

**Test Steps:**
```bash
# Start all Watchers
# Let run for 24 hours

# Check health every hour
for i in {1..24}; do
  sleep 3600
  python3 .claude/skills/monitor-system/scripts/health_monitor.py
  echo "Hour $i: Health check complete"
done

# Review 24-hour health log
grep "health_score" Vault/Logs/system/health_checks.json | tail -24
```

**Expected Results:**
- ✅ All processes running after 24 hours
- ✅ Health score >85 throughout
- ✅ No memory leaks (check memory usage trend)
- ✅ No process crashes

**Pass Criteria:** 24 hours of stable operation

---

## Security Tests

### Test 24: Credential Security

**Purpose:** Verify no credentials exposed

**Test Steps:**
```bash
# Check for credentials in logs
grep -r "password\|secret\|token\|api_key" Vault/Logs/ | grep -v "REDACTED"

# Check for credentials in git
git log --all --full-history --source --grep="password\|secret\|token"

# Verify .env in .gitignore
cat .gitignore | grep .env
```

**Expected Results:**
- ✅ No plain-text credentials in logs
- ✅ Sensitive fields show [REDACTED]
- ✅ No credentials in git history
- ✅ .env file gitignored

**Pass Criteria:** Zero credential exposures

---

### Test 25: Approval Bypass Prevention

**Purpose:** Verify approval workflow can't be bypassed

**Test Scenarios:**

**Scenario A: Direct Action Without Approval**
```bash
# Attempt to send email without approval
# (Should fail or require approval)
```

**Scenario B: Approval File Tampering**
```bash
# Modify approval file (change amount, recipient, etc.)
# System should detect tampering and reject
```

**Expected:** All high-risk actions require approval, tampering detected

---

### Test 26: API Rate Limit Handling

**Purpose:** Verify graceful handling of rate limits

**Test Steps:**
```bash
# Trigger rapid API calls to intentionally hit rate limit
# (Use test account to avoid production impact)

for i in {1..100}; do
  claude-code "test api call" &
done

# Verify rate limit handling
grep "rate_limit" Vault/Logs/system/*.json
```

**Expected Results:**
- ✅ Rate limit detected
- ✅ Operations queued
- ✅ Retry scheduled appropriately
- ✅ No data loss

**Pass Criteria:** Rate limits handled without errors

---

## 7-Day Burn-In Test

### Comprehensive System Validation

**Purpose:** Validate system readiness for production

**Timeline:** 7 consecutive days

**Daily Checklist:**

```
DAY 1 - Initial Validation
[ ] All Watchers started
[ ] Health score: _____
[ ] Logs writing correctly
[ ] Dashboard updating

DAY 2 - Email Processing
[ ] Sent 5 test emails
[ ] All emails detected
[ ] Responses generated
[ ] Health score: _____

DAY 3 - Social Media
[ ] LinkedIn post published
[ ] Facebook post published
[ ] Instagram post published
[ ] Twitter post published
[ ] Health score: _____

DAY 4 - Accounting
[ ] Xero transactions synced
[ ] Expenses categorized
[ ] Dashboard updated
[ ] Health score: _____

DAY 5 - Error Recovery
[ ] Killed 1 process
[ ] Auto-recovery successful
[ ] No data loss
[ ] Health score: _____

DAY 6 - Full Load
[ ] 20 emails processed
[ ] 4 social posts published
[ ] Accounting synced
[ ] Health score: _____

DAY 7 - Final Validation
[ ] CEO briefing generated
[ ] All systems operational
[ ] Average health score: _____
[ ] Uptime: _____%
```

**Success Criteria:**
- ✅ 99%+ uptime over 7 days
- ✅ Average health score >90
- ✅ Zero data loss events
- ✅ <3 process crashes total
- ✅ All auto-recoveries successful
- ✅ CEO briefing generated successfully

**Overall Pass:** All criteria met

---

## Test Results Template

### Test Execution Record

```markdown
# Autonomous FTE Test Results

**Test Date:** ___________
**Tester:** ___________
**System Version:** Gold Tier 1.0

## Unit Tests

| Test | Pass/Fail | Notes |
|------|-----------|-------|
| 1.1 Gmail Watcher | ☐ Pass ☐ Fail | |
| 1.2 WhatsApp Watcher | ☐ Pass ☐ Fail | |
| 1.3 Other Watchers | ☐ Pass ☐ Fail | |
| 2.1 Email MCP | ☐ Pass ☐ Fail | |
| 2.2 Xero MCP | ☐ Pass ☐ Fail | |
| 2.3 Social Media MCP | ☐ Pass ☐ Fail | |
| 3. Health Monitor | ☐ Pass ☐ Fail | |
| 4. Error Handler | ☐ Pass ☐ Fail | |
| 5. Watchdog Manager | ☐ Pass ☐ Fail | |
| 6. Log Aggregator | ☐ Pass ☐ Fail | |

**Unit Tests Score:** ____/10

## Integration Tests

| Test | Pass/Fail | Notes |
|------|-----------|-------|
| 7. handle-approval | ☐ Pass ☐ Fail | |
| 8. process-emails | ☐ Pass ☐ Fail | |
| 9. post-to-linkedin | ☐ Pass ☐ Fail | |
| 10. manage-accounting | ☐ Pass ☐ Fail | |
| 11. post-to-social-media | ☐ Pass ☐ Fail | |
| 12. post-to-twitter | ☐ Pass ☐ Fail | |
| 13. generate-ceo-briefing | ☐ Pass ☐ Fail | |
| 14. monitor-system | ☐ Pass ☐ Fail | |

**Integration Tests Score:** ____/8

## End-to-End Tests

| Test | Pass/Fail | Duration | Notes |
|------|-----------|----------|-------|
| 15. Email Workflow | ☐ Pass ☐ Fail | ____ min | |
| 16. Multi-Platform Social | ☐ Pass ☐ Fail | ____ min | |
| 17. Weekly Business Cycle | ☐ Pass ☐ Fail | 7 days | |

**E2E Tests Score:** ____/3

## Chaos Engineering

| Test | Pass/Fail | Recovery Time | Notes |
|------|-----------|---------------|-------|
| 18. Process Crash | ☐ Pass ☐ Fail | ____ min | |
| 19. Network Outage | ☐ Pass ☐ Fail | ____ min | |
| 20. Disk Space | ☐ Pass ☐ Fail | ____ min | |

**Chaos Tests Score:** ____/3

## Performance Tests

| Test | Pass/Fail | Metric | Notes |
|------|-----------|--------|-------|
| 21. Email Volume | ☐ Pass ☐ Fail | ____ emails/hr | |
| 22. Concurrent Ops | ☐ Pass ☐ Fail | ____ ops | |
| 23. 24h Stability | ☐ Pass ☐ Fail | ____% uptime | |

**Performance Tests Score:** ____/3

## Security Tests

| Test | Pass/Fail | Notes |
|------|-----------|-------|
| 24. Credential Security | ☐ Pass ☐ Fail | |
| 25. Approval Bypass | ☐ Pass ☐ Fail | |
| 26. Rate Limit Handling | ☐ Pass ☐ Fail | |

**Security Tests Score:** ____/3

---

## Overall Results

**Total Tests:** 30
**Tests Passed:** ____
**Tests Failed:** ____
**Pass Rate:** ____%

**7-Day Burn-In:** ☐ Pass ☐ Fail
**Uptime:** ____%
**Avg Health Score:** ____

**Ready for Production:** ☐ Yes ☐ No

## Issues Found

1. _________________________________
2. _________________________________
3. _________________________________

## Recommendations

1. _________________________________
2. _________________________________
3. _________________________________

**Tester Signature:** _____________ **Date:** _____________
```

---

## Quick Test Commands

**Copy-paste these for rapid testing:**

```bash
# Complete health check
python3 .claude/skills/monitor-system/scripts/health_monitor.py && cat Vault/System_Status.md

# Test all Watchers
ps aux | grep watcher

# Test MCP servers
claude-code mcp list

# Trigger test email workflow
claude-code "process test email"

# Trigger test social post
claude-code "create test linkedin post"

# Check recent errors
grep -E "critical|high" Vault/Logs/system/*.json | tail -10

# Verify logging
tail -f Vault/Logs/actions/$(date +%Y-%m-%d).json

# Test watchdog
python3 .claude/skills/monitor-system/scripts/watchdog_manager.py

# Generate test briefing
claude-code "generate weekly briefing"
```

---

**Document Version:** 1.0
**Last Updated:** January 12, 2026
**Next Review:** February 12, 2026

*Test early, test often, test thoroughly. Quality is not an accident.*
