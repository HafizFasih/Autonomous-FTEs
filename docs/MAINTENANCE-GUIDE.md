# Maintenance Guide: Autonomous FTE

**System:** Autonomous FTE - Personal AI Employee (Gold Tier)
**Version:** 1.0
**Last Updated:** January 12, 2026
**Target Audience:** System operators and administrators

---

## Overview

This guide covers all aspects of maintaining your Autonomous FTE system for reliable 24/7 operation. Following this maintenance schedule ensures 99%+ uptime, optimal performance, and continued cost savings.

**Maintenance Philosophy:**
- **Proactive > Reactive:** Prevent issues before they occur
- **Automated > Manual:** Let the system maintain itself where possible
- **Monitored > Blind:** Always know system health status
- **Documented > Assumed:** Log all changes and decisions

---

## Table of Contents

1. [Daily Maintenance (Automated)](#daily-maintenance-automated)
2. [Weekly Checks (5 minutes)](#weekly-checks-5-minutes)
3. [Monthly Reviews (1 hour)](#monthly-reviews-1-hour)
4. [Quarterly Audits (2 hours)](#quarterly-audits-2-hours)
5. [Annual Tasks (4 hours)](#annual-tasks-4-hours)
6. [Troubleshooting Guide](#troubleshooting-guide)
7. [Emergency Procedures](#emergency-procedures)
8. [Performance Optimization](#performance-optimization)

---

## Daily Maintenance (Automated)

**Status:** ✅ Fully automated, no manual intervention required

### Health Checks (Every 5 Minutes)

**Script:** `health_monitor.py`
**Schedule:** `*/5 * * * *` (cron)

**What It Does:**
- Checks all 5 Watcher processes (PID + heartbeat)
- Verifies 4 MCP servers responding
- Monitors disk space (>10% free required)
- Tests network connectivity
- Validates logging system
- Confirms vault access

**What It Produces:**
- `/Vault/System_Status.md` (updated every 5 min)
- `/Vault/Logs/system/health_checks.json` (continuous log)

**When to Intervene:**
- Health score <80 for >15 minutes → Check System_Status.md for issues
- Critical alert appears in /Needs_Action/ → Address immediately

---

### Log Rotation (12:05 AM Daily)

**Script:** `log_aggregator.py`
**Schedule:** `5 0 * * *` (cron)

**What It Does:**
- Creates new daily log files (actions, system, security)
- Compresses logs >7 days old (JSON → JSON.gz)
- Moves compressed logs >30 days to archives/
- Enforces retention policies (90d/60d/7yr)
- Generates log statistics report

**What It Produces:**
- New daily log files in `/Vault/Logs/`
- `/Vault/Logs/log_stats.md` (updated daily)

**When to Intervene:**
- Log statistics show >5GB total logs → Manual cleanup needed
- Disk space <15% free → Investigate log size

---

### Transaction Sync (8:00 AM Daily)

**Skill:** `manage-accounting`
**Schedule:** `0 8 * * *` (cron)

**What It Does:**
- Syncs Xero transactions from last 24 hours
- Auto-categorizes expenses (87% accuracy)
- Updates `/Vault/Accounting/Current_Month.md`
- Flags unusual transactions for review

**What to Check:**
- Review flagged transactions in Current_Month.md
- Verify expense categories are correct (spot check 2-3)

**Time Required:** 2 minutes

---

### Scheduled Social Posts

**Schedule:**
- 9:00 AM: LinkedIn (`post-to-linkedin`)
- 10:00 AM: Facebook + Instagram (`post-to-social-media`)
- 11:00 AM: Twitter (`post-to-twitter`)

**What It Does:**
- Generates platform-optimized content
- Creates approval request in /Pending_Approval/
- Waits for human approval
- Posts to platform when approved

**What to Check:**
- Morning: Review 3 pending social posts (~5 min)
- Approve or reject with edits

**Time Required:** 5 minutes

---

## Weekly Checks (5 Minutes)

**Recommended:** Sunday evening or Monday morning

### 1. Review CEO Briefing (3 minutes)

**File:** `/Vault/Briefings/[YYYY-MM-DD]_Monday_Briefing.md`
**Generated:** Sunday 11:45 PM automatically

**What to Review:**
- ✅ Revenue vs targets: On track?
- ✅ Proactive recommendations: Any quick wins?
- ✅ Bottlenecks: What slowed down last week?
- ✅ Upcoming deadlines: What needs attention?

**Actions:**
- Move cost optimization items to /Pending_Approval/ if you want to act
- Update Business_Goals.md if targets changed
- Note bottlenecks to prevent recurrence

---

### 2. Check System Health Trend (1 minute)

**File:** `/Vault/System_Status.md`

**What to Check:**
- Current health score: Should be 85-100
- Any recurring issues in last 7 days?
- Process restart count: Should be <3/week

**Red Flags:**
- 🚩 Health score <85 average for week → Investigate
- 🚩 Same process restarting daily → Root cause needed
- 🚩 Error count increasing → Check error logs

---

### 3. Spot Check Logs (1 minute)

**Command:**
```bash
# Check for any high-severity errors this week
grep -r "\"severity\": \"high\"" Vault/Logs/system/
```

**What to Look For:**
- Unusual error patterns
- New error types not seen before
- Errors that resolved themselves (good!)

**Action:** If same error appears 3+ times, investigate root cause.

---

## Monthly Reviews (1 Hour)

**Recommended:** First Sunday of each month

### 1. Financial Review (20 minutes)

**Review Locations:**
- `/Vault/Accounting/Current_Month.md`
- `/Vault/Briefings/` (all 4 weekly briefings)

**Checklist:**

**Revenue Analysis:**
- [ ] Total revenue for month vs target
- [ ] Revenue trend: increasing, stable, or decreasing?
- [ ] Top 3 revenue sources identified

**Expense Analysis:**
- [ ] Total expenses for month vs budget
- [ ] Subscription audit: Any unused services?
- [ ] Categorization spot check: Review 10 random transactions

**Cost Optimizations:**
- [ ] Review AI's cost-saving recommendations
- [ ] Did you act on last month's recommendations?
- [ ] Identify 1-2 new opportunities

**Actions:**
- Update Business_Goals.md with next month's targets
- Cancel subscriptions AI identified as unused
- Adjust expense categories if needed

---

### 2. Social Media Performance (15 minutes)

**Review Locations:**
- `/Vault/Social_Media/LinkedIn/metrics.md`
- `/Vault/Social_Media/Facebook/metrics.md`
- `/Vault/Social_Media/Instagram/metrics.md`
- `/Vault/Social_Media/Twitter/metrics.md`

**Checklist:**

**Engagement Analysis:**
- [ ] Total engagements: Trending up or down?
- [ ] Best performing post per platform: What made it work?
- [ ] Worst performing post: Why did it flop?

**Follower Growth:**
- [ ] Net follower gain across 4 platforms
- [ ] Follower growth rate: Acceptable?

**Content Optimization:**
- [ ] Are platform guidelines being followed?
- [ ] Content calendar: Any gaps or inconsistencies?
- [ ] Hashtag performance: Which hashtags work best?

**Actions:**
- Update content calendar based on performance
- Adjust posting times if engagement patterns changed
- Refine hashtag library (remove poor performers)

---

### 3. System Performance Review (15 minutes)

**Review Locations:**
- `/Vault/Logs/log_stats.md`
- `/Vault/System_Status.md`

**Checklist:**

**Uptime & Reliability:**
- [ ] Average health score for month: >90?
- [ ] System uptime percentage: 99%+?
- [ ] Number of escalations to user: <5?

**Resource Usage:**
- [ ] Total log storage: <2GB?
- [ ] Disk space remaining: >20%?
- [ ] API cost for month: Within budget?

**Error Patterns:**
- [ ] Top 3 error types this month
- [ ] Auto-recovery success rate: >90%?
- [ ] Any new error types not in catalog?

**Actions:**
- Add new error types to error-catalog.md
- Optimize if API costs are increasing
- Clean up logs if storage >2GB

---

### 4. Update Documentation (10 minutes)

**Files to Update:**

**Company_Handbook.md:**
- [ ] Any new rules or preferences to add?
- [ ] Examples of good AI decisions to reinforce
- [ ] Examples of mistakes to avoid (if any)

**Business_Goals.md:**
- [ ] Update revenue targets for next month
- [ ] Adjust KPI thresholds based on performance
- [ ] Add/remove projects as needed

**Reference Documents:**
- [ ] Update expense-rules.md if new vendors
- [ ] Update content-calendar.md with new ideas
- [ ] Update hashtag-library.md with performers

---

## Quarterly Audits (2 Hours)

**Recommended:** First weekend of Jan, Apr, Jul, Oct

### 1. Security Audit (30 minutes)

**API Credentials Review:**

**Checklist:**
- [ ] Gmail OAuth: Refresh token still valid?
- [ ] Xero OAuth: Tokens refreshing successfully?
- [ ] Facebook access token: Expiring soon?
- [ ] Twitter bearer token: Still valid?
- [ ] LinkedIn OAuth: Working?

**Action:** Rotate any credentials that haven't been rotated in >6 months.

**Security Log Review:**
```bash
# Check for any auth failures
grep "auth_failure" Vault/Logs/security/*.json
```

**Checklist:**
- [ ] No unexpected auth failures?
- [ ] No unusual source IPs in logs?
- [ ] All API calls from expected origins?

**Action:** Investigate any suspicious activity.

---

### 2. Disaster Recovery Test (30 minutes)

**Backup Verification:**

**Checklist:**
- [ ] Vault backup exists and is current?
- [ ] Credentials backup exists (separate from vault)?
- [ ] Can you restore vault from backup?

**Test Procedure:**
1. Stop all Watchers
2. Copy vault to temporary location
3. Delete test file from vault
4. Restore from backup
5. Verify test file restored
6. Restart Watchers

**Recovery Time Test:**
- [ ] How long to restore from backup? (Target: <15 min)
- [ ] How long to restart all services? (Target: <5 min)

**Action:** Update disaster recovery documentation with timing.

---

### 3. Full System Test (45 minutes)

**End-to-End Testing:**

**Test 1: Email Flow**
1. Send test email to yourself (urgent keyword)
2. Verify Watcher detects it (<5 min)
3. Verify Claude creates response draft
4. Verify approval request created
5. Approve and verify email sent

**Test 2: Social Post Flow**
1. Manually trigger social post
2. Verify approval request created
3. Approve and verify posts to all 4 platforms
4. Check engagement metrics logging

**Test 3: Accounting Flow**
1. Create test transaction in Xero
2. Verify sync to vault (<24 hours)
3. Verify categorization accurate
4. Verify dashboard updated

**Test 4: Error Recovery**
1. Kill a Watcher process manually
2. Verify health check detects failure (<5 min)
3. Verify watchdog restarts process (<2 min)
4. Verify process healthy after restart

**Checklist:**
- [ ] All 4 tests passed
- [ ] Response times within targets
- [ ] No errors in logs

---

### 4. Performance Optimization (15 minutes)

**Identify Bottlenecks:**

**Check API Usage:**
```bash
# Count API calls per service
grep "api_call" Vault/Logs/actions/*.json | cut -d'"' -f4 | sort | uniq -c
```

**Checklist:**
- [ ] Any API near rate limit?
- [ ] Unnecessary duplicate calls?
- [ ] Can any calls be batched?

**Check Processing Times:**
```bash
# Find slowest operations
grep "processing_time_ms" Vault/Logs/actions/*.json | sort -t: -k2 -n | tail -10
```

**Checklist:**
- [ ] Any operations >10 seconds?
- [ ] Can slow operations be cached?
- [ ] Async opportunities?

**Action:** Optimize top 2 bottlenecks.

---

## Annual Tasks (4 Hours)

**Recommended:** Anniversary of system deployment

### 1. Comprehensive ROI Analysis (1 hour)

**Calculate Annual Impact:**

**Time Savings:**
- Weeks operated: _____
- Hours saved per week: 21.5
- Total hours saved: _____ × 21.5 = _____
- Value at $40/hour: $_____

**Cost Savings:**
- Subscription optimizations: $_____
- Avoided accountant fees: $_____
- Error reduction: $_____
- **Total:** $_____

**Operating Costs:**
- Claude Code API: $_____
- Other API costs: $_____
- Electricity: $_____
- **Total:** $_____

**Net ROI:**
- Total saved: $_____
- Total cost: $_____
- **Net benefit:** $_____
- **ROI percentage:** _____%

**Document:** Save this analysis for tax purposes and future planning.

---

### 2. Complete System Upgrade (1 hour)

**Software Updates:**

**Checklist:**
- [ ] Python packages: `pip install --upgrade -r requirements.txt`
- [ ] Node.js packages: `npm update` in MCP servers
- [ ] Claude Code: `npm update -g @anthropic/claude-code`
- [ ] Obsidian: Check for updates

**Dependency Audit:**
```bash
# Check for security vulnerabilities
pip list --outdated
npm audit
```

**Action:** Update any packages with known vulnerabilities.

---

### 3. Architecture Review (1 hour)

**System Health Assessment:**

**Metrics to Review:**
- Average health score for year
- Total uptime percentage
- Error count and types
- Recovery success rate
- Escalation frequency

**Capacity Planning:**
- Is disk space sufficient for next year?
- Are API quotas adequate?
- Are Watchers handling load comfortably?

**Enhancement Opportunities:**
- What features would add most value?
- What manual tasks remain?
- What errors recur most often?

**Action:** Create roadmap for next year's improvements.

---

### 4. Documentation Update (1 hour)

**Review All Documentation:**

**Checklist:**
- [ ] System Architecture: Still accurate?
- [ ] Maintenance Guide: Any new procedures?
- [ ] Lessons Learned: New lessons this year?
- [ ] All reference docs: Up to date?

**Update With:**
- Actual metrics from past year
- New error types discovered
- Process improvements made
- User feedback and suggestions

---

## Troubleshooting Guide

### Common Issues & Solutions

#### Issue 1: Health Score Below 80

**Symptoms:**
- System_Status.md shows score <80
- Dashboard indicates degraded state

**Diagnosis:**
```bash
# Check which component is failing
cat Vault/System_Status.md
```

**Solutions by Component:**

**Watchers (30 points):**
```bash
# Check which watcher is down
ps aux | grep watcher

# Restart failed watcher
python3 watchers/[watcher_name].py &

# Verify restart
ps aux | grep [watcher_name]
```

**MCP Servers (25 points):**
```bash
# Test MCP servers
claude-code mcp list

# Restart specific MCP
# (Restart Claude Code or check MCP config)
```

**Disk Space (15 points):**
```bash
# Check disk usage
df -h

# Clean up if needed
python3 .claude/skills/monitor-system/scripts/log_aggregator.py
```

**Network (15 points):**
```bash
# Test connectivity
ping google.com

# Check API access
curl https://api.anthropic.com/health
```

---

#### Issue 2: Process Keeps Crashing

**Symptoms:**
- Same Watcher restarting multiple times per hour
- Alert in /Needs_Action/ about restart limit

**Diagnosis:**
```bash
# Check crash logs
grep "process_crash" Vault/Logs/system/incidents/$(date +%Y-%m-%d).json

# Check process logs
tail -n 100 [watcher_log_file]
```

**Common Causes:**

**1. Config Issue:**
```bash
# Verify config files exist
ls -la watchers/config/

# Check environment variables
echo $GMAIL_API_KEY
```

**2. Dependency Missing:**
```bash
# Reinstall dependencies
cd watchers/
pip install -r requirements.txt
```

**3. API Auth Expired:**
```bash
# Check auth status in logs
grep "auth_failure" Vault/Logs/security/*.json

# Reauthorize if needed
# (Follow API-specific reauth process)
```

**4. Bug in Code:**
- Check error message in logs
- Review recent code changes
- Test manually: `python3 watchers/[watcher].py`

---

#### Issue 3: Xero Sync Not Working

**Symptoms:**
- Current_Month.md not updating
- Last sync >24 hours ago

**Diagnosis:**
```bash
# Check Xero logs
grep "xero" Vault/Logs/system/*.json | tail -20

# Test Xero MCP
claude-code "sync xero transactions"
```

**Solutions:**

**1. Token Expired:**
```bash
# Check token status
grep "xero.*token" Vault/Logs/security/*.json

# Refresh token (automatic via error_handler)
# Or manually reauth if refresh failed
```

**2. API Rate Limit:**
- Wait 60 minutes, then retry
- Reduce sync frequency if recurring

**3. MCP Server Down:**
```bash
# Restart Xero MCP server
# (Restart Claude Code)
```

---

#### Issue 4: Social Posts Not Publishing

**Symptoms:**
- Approval given but post not appearing on platform
- Error in action logs

**Diagnosis:**
```bash
# Check recent post attempts
grep "post_created" Vault/Logs/actions/*.json | tail -10

# Check for errors
grep "post.*failed" Vault/Logs/actions/*.json
```

**Solutions by Platform:**

**LinkedIn:**
- Check API credentials still valid
- Verify character count <700 (doc says 1000 but actually 700)
- Check for special characters breaking formatting

**Facebook/Instagram:**
- Verify page still connected
- Check token expiry (60 days)
- Ensure image dimensions meet requirements

**Twitter:**
- Check character count ≤280
- Verify bearer token valid
- Check for rate limit (300 posts/3 hours)

---

#### Issue 5: CEO Briefing Not Generated

**Symptoms:**
- Monday morning, no briefing in /Briefings/
- No notification in /Needs_Action/

**Diagnosis:**
```bash
# Check if scheduled task ran
grep "generate-ceo-briefing" Vault/Logs/actions/*.json

# Check cron job status
crontab -l | grep briefing
```

**Solutions:**

**1. Cron Didn't Run:**
```bash
# Verify cron is running
systemctl status cron   # Linux
# or check Task Scheduler   # Windows

# Manually trigger
claude-code "generate weekly briefing"
```

**2. Data Missing:**
- Verify accounting data exists (Current_Month.md)
- Verify social metrics exist (metrics.md files)
- Verify task data exists (/Done/ folder)

**3. Skill Error:**
- Check error logs for generate-ceo-briefing
- Test manually to see error output

---

## Emergency Procedures

### Emergency 1: Complete System Failure

**Symptoms:** Everything down, no processes running

**Recovery Steps:**

1. **Stay Calm** (5 seconds)
   - System is resilient, data is safe in vault

2. **Restart All Watchers** (2 minutes)
```bash
cd watchers/
python3 gmail_watcher.py &
python3 whatsapp_watcher.py &
python3 linkedin_watcher.py &
python3 finance_watcher.py &
python3 filesystem_watcher.py &
```

3. **Restart Claude Code** (30 seconds)
   - Close and reopen Claude Code
   - Verify MCP servers load

4. **Verify Health** (1 minute)
```bash
python3 .claude/skills/monitor-system/scripts/health_monitor.py
cat Vault/System_Status.md
```

5. **Check for Data Loss** (2 minutes)
   - Verify vault accessible
   - Check recent log entries
   - Verify last briefing exists

**Total Recovery Time:** <10 minutes

---

### Emergency 2: Accidental Wrong Action

**Symptoms:** AI sent email/post you didn't approve or made mistake

**Immediate Actions:**

**For Email:**
1. Log into Gmail immediately
2. Recall message if <30 seconds (Gmail feature)
3. Or send correction/apology email
4. Document what happened in /Logs/

**For Social Post:**
1. Log into platform immediately
2. Delete post (within minutes is best)
3. Post correction if needed
4. Document incident

**For Payment:**
1. Log into Xero/bank immediately
2. Cancel transaction if possible
3. Contact recipient if already sent
4. Document for audit trail

**Prevention for Future:**
1. Identify why approval was bypassed (if it was)
2. Update approval rules in Company_Handbook.md
3. Add stricter approval threshold
4. Test approval workflow

---

### Emergency 3: Vault Corruption

**Symptoms:** Can't open vault, Obsidian errors, file corruption

**Recovery Steps:**

1. **Stop All Processes Immediately**
```bash
pkill -f watcher
```

2. **Restore from Backup**
```bash
# Copy vault backup to primary location
cp -r /path/to/backup/AI_Employee_Vault /path/to/primary/

# Verify restore
ls -la /path/to/primary/AI_Employee_Vault/
```

3. **Verify Integrity**
   - Open vault in Obsidian
   - Check Dashboard.md loads
   - Verify recent files exist

4. **Restart System**
   - Restart Watchers
   - Run health check

**Prevention:**
- Set up automated daily backups
- Use git for vault version control
- Keep 30 days of backups

---

## Performance Optimization

### Optimization 1: Reduce API Costs

**If Claude Code costs are high (>$200/month):**

**1. Use Haiku for Simple Tasks**
- Email categorization: haiku
- Task updates: haiku
- Simple responses: haiku
- Complex analysis: sonnet

**2. Batch Operations**
- Process multiple emails in one Claude call
- Generate multiple social posts together
- Bulk categorize expenses

**3. Cache Results**
- Expense categorization rules (don't re-decide every time)
- Social post templates (reuse structures)
- Common responses (template-based)

**Expected Savings:** 30-50% reduction

---

### Optimization 2: Speed Up Processing

**If operations feel slow:**

**1. Async Operations**
```python
# Replace synchronous logging with async
async def log_action(data):
    async with aiofiles.open(log_file, 'a') as f:
        await f.write(json.dumps(data) + '\n')
```

**2. Parallel Processing**
- Process multiple emails concurrently
- Check health of all Watchers in parallel
- Sync all social platforms simultaneously

**3. Reduce Polling Frequency**
- Email: 10 min → 15 min (if not time-critical)
- Social metrics: daily → weekly

**Expected Improvement:** 2-3x faster processing

---

### Optimization 3: Reduce Log Storage

**If logs >5GB:**

**1. More Aggressive Compression**
- Compress after 3 days instead of 7
- Use higher compression (gzip -9)

**2. Reduce Log Verbosity**
- Only log high/critical errors (not info)
- Sample success logs (1 in 10 instead of all)

**3. Archive to Cloud**
- Move archives >90 days to cloud storage
- Keep only recent logs locally

**Expected Savings:** 70-80% storage reduction

---

## Backup Procedures

### Daily Automated Backup

**Setup:**
```bash
# Create backup script
cat > daily_backup.sh <<'EOF'
#!/bin/bash
DATE=$(date +%Y-%m-%d)
tar -czf /backups/vault_$DATE.tar.gz /path/to/AI_Employee_Vault/
find /backups/ -name "vault_*.tar.gz" -mtime +30 -delete
EOF

# Schedule daily
crontab -e
# Add: 0 2 * * * /path/to/daily_backup.sh
```

**What's Backed Up:**
- Entire vault (including all folders)
- 30 days of backups retained

**What's NOT Backed Up:**
- Credentials (.env files) - back up separately
- Logs >30 days - archived separately

---

### Weekly Cloud Backup

**Setup (Optional):**
```bash
# Sync to cloud (Dropbox/Google Drive/etc)
rclone sync /path/to/AI_Employee_Vault/ remote:AI_Backup/ --exclude "Logs/"

# Schedule weekly
crontab -e
# Add: 0 3 * * 0 /path/to/cloud_backup.sh
```

**Benefit:** Protection against local hardware failure

---

## Health Monitoring Dashboard

### Quick Health Check Commands

```bash
# Overall health
cat Vault/System_Status.md

# Process status
ps aux | grep watcher

# Recent errors
grep "critical\|high" Vault/Logs/system/*.json | tail -20

# Disk usage
df -h | grep -E "Use%|/$"

# Log size
du -sh Vault/Logs/

# API usage today
grep "$(date +%Y-%m-%d)" Vault/Logs/actions/*.json | wc -l
```

---

## Maintenance Checklist Summary

**Print this and check off monthly:**

```
MONTHLY MAINTENANCE CHECKLIST

Date: ____________

Financial Review (20 min)
[ ] Revenue vs target reviewed
[ ] Expenses vs budget reviewed
[ ] Cost optimizations identified
[ ] Business_Goals.md updated

Social Media (15 min)
[ ] Engagement trends analyzed
[ ] Best/worst posts identified
[ ] Content calendar updated
[ ] Metrics reviewed

System Performance (15 min)
[ ] Average health score: _____
[ ] Uptime percentage: _____
[ ] Log storage: _____ GB
[ ] API costs: $_____

Documentation (10 min)
[ ] Company_Handbook.md updated
[ ] Business_Goals.md current
[ ] Reference docs refreshed

Issues Found:
_________________________________
_________________________________
_________________________________

Actions Taken:
_________________________________
_________________________________
_________________________________

Next Month Focus:
_________________________________
_________________________________
_________________________________

Signature: _____________ Date: _____________
```

---

## Support & Resources

**Documentation:**
- System Architecture: `/docs/SYSTEM-ARCHITECTURE.md`
- Lessons Learned: `/docs/LESSONS-LEARNED.md`
- Completion Report: `/docs/GOLD-TIER-COMPLETION-REPORT.md`

**Skill Documentation:**
- All skills have SKILL.md files in `.claude/skills/[skill-name]/`
- Reference docs in `.claude/skills/[skill-name]/reference/`

**Logs:**
- Actions: `/Vault/Logs/actions/`
- System: `/Vault/Logs/system/`
- Financial: `/Vault/Logs/financial/`
- Security: `/Vault/Logs/security/`

**Community:**
- Hackathon discussions: Wednesday 10pm Zoom meetings
- YouTube: @panaversity
- Submission form: https://forms.gle/JR9T1SJq5rmQyGkGA

---

**Document Version:** 1.0
**Last Reviewed:** January 12, 2026
**Next Review:** February 12, 2026

*Keep this guide accessible. Print the checklist. Maintain your AI employee and it will maintain your business.*
