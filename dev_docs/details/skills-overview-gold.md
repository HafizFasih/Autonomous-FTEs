# Agent Skills Overview: Gold Tier

**Document Version:** 1.0
**Last Updated:** 2026-01-11
**Project:** Autonomous FTE - Personal AI Employee

---

## Gold Tier Overview

**New Skills Required:** 5 (Total: 10 skills)
**Build Time:** 40-56 hours
**Key Additions:** Xero accounting, multi-platform social (Facebook/Instagram/Twitter), weekly CEO briefing, system monitoring

### Prerequisites

**From Silver Tier:**
- ✅ 5 operational skills (process-tasks, process-emails, post-to-linkedin, create-plan, handle-approval)
- ✅ 2+ Watcher scripts running
- ✅ Email MCP server operational
- ✅ Approval workflow tested

**New Requirements:**
- Xero account with API access
- Facebook Business Account + Instagram
- Twitter Developer Account
- Enhanced vault structure (see below)

### Enhanced Vault Structure

```
AI_Employee_Vault/
├── [Existing Silver folders...]
├── Accounting/              # NEW
│   ├── Current_Month.md
│   ├── Transactions/
│   ├── Invoices/
│   └── Expenses/
├── Briefings/               # NEW
│   └── archives/
├── Social_Media/
│   ├── LinkedIn/            # From Silver
│   ├── Facebook/            # NEW
│   ├── Instagram/           # NEW
│   └── Twitter/             # NEW
└── Logs/
    ├── system/              # NEW
    ├── actions/             # NEW
    └── financial/           # NEW
```

---

## Gold Tier Skills Summary

| # | Skill | Files | Priority | Time |
|---|-------|-------|----------|------|
| 6 | manage-accounting | 9 | Critical | 12-16h |
| 7 | post-to-social-media | 9 | High | 6-8h |
| 8 | post-to-twitter | 6 | High | 4-6h |
| 9 | generate-ceo-briefing | 8 | Critical | 8-12h |
| 10 | monitor-system | 9 | Critical | 10-14h |

---

## Skill #6: manage-accounting

**Purpose:** Xero integration for invoicing, expense categorization, financial tracking

**Structure:**
```
manage-accounting/
├── SKILL.md
├── reference/
│   ├── xero-categories.md
│   ├── expense-rules.md
│   ├── invoice-templates.md
│   ├── reconciliation-guide.md
│   └── tax-categories.md
└── scripts/
    ├── xero_sync.py
    ├── categorize_expense.py
    └── generate_invoice.py
```

**Metadata:**
```yaml
---
name: manage-accounting
description: Integrate with Xero accounting system to sync transactions, categorize
  expenses, track revenue, generate invoices, and maintain financial records. Use
  when syncing bank transactions, categorizing expenses, creating invoices, checking
  financial status, or when user mentions "accounting", "xero", "expenses", "revenue".
user-invocable: true
allowed-tools: [Read, Write, Edit, Bash, Glob]
---
```

**Key Functions:**
- Sync Xero transactions → /Accounting/Current_Month.md
- Auto-categorize expenses (80%+ accuracy target)
- Generate invoices via Xero MCP
- Bank reconciliation
- Update Dashboard with financial summary

**Dependencies:** Xero MCP Server, Business_Goals.md with financial targets

---

## Skill #7: post-to-social-media

**Purpose:** Facebook & Instagram automation with engagement tracking

**Structure:**
```
post-to-social-media/
├── SKILL.md
├── reference/
│   ├── facebook-guidelines.md
│   ├── instagram-guidelines.md
│   ├── content-calendar.md
│   ├── hashtag-library.md
│   └── engagement-rules.md
└── scripts/
    ├── facebook_api_helper.py
    ├── instagram_api_helper.py
    └── image_optimizer.py
```

**Metadata:**
```yaml
---
name: post-to-social-media
description: Manage Facebook and Instagram business presence. Create and schedule
  posts, generate content for both platforms, track engagement. Use when posting to
  Facebook or Instagram, or when user mentions "facebook", "instagram", "social media".
user-invocable: true
allowed-tools: [Read, Write, Edit, Bash, Glob]
context: fork
---
```

**Key Functions:**
- Create platform-optimized posts (FB: 40-80 words, IG: visual focus)
- Auto-apply platform-specific hashtags
- Request approval → publish via Facebook/Instagram API
- Track engagement metrics
- Follow content calendar

**Dependencies:** Facebook Business Account, Instagram Business linked to FB

---

## Skill #8: post-to-twitter

**Purpose:** Twitter/X posting with thread support and engagement tracking

**Structure:**
```
post-to-twitter/
├── SKILL.md
├── reference/
│   ├── twitter-guidelines.md
│   ├── thread-templates.md
│   ├── hashtag-strategy.md
│   └── engagement-tactics.md
└── scripts/
    └── twitter_api_helper.py
```

**Metadata:**
```yaml
---
name: post-to-twitter
description: Manage Twitter/X presence. Create tweets and threads, schedule content,
  track engagement. Use when posting to Twitter, creating threads, or when user
  mentions "twitter", "tweet", "x post", "thread".
user-invocable: true
allowed-tools: [Read, Write, Edit, Bash, Glob]
context: fork
---
```

**Key Functions:**
- Single tweets (280 char limit, optimal 71-100)
- Multi-tweet threads with templates
- 1-2 hashtags max (unlike Instagram)
- Request approval → publish via Twitter API v2
- Track engagement and mentions

**Dependencies:** Twitter Developer Account with API v2 access

---

## Skill #9: generate-ceo-briefing

**Purpose:** Weekly autonomous business audit with proactive recommendations

**Structure:**
```
generate-ceo-briefing/
├── SKILL.md
├── reference/
│   ├── briefing-template.md
│   ├── analysis-framework.md
│   ├── kpi-definitions.md
│   └── recommendation-engine.md
└── scripts/
    ├── analyze_performance.py
    ├── detect_bottlenecks.py
    └── generate_insights.py
```

**Metadata:**
```yaml
---
name: generate-ceo-briefing
description: Autonomously audit business and financial performance weekly. Analyzes
  revenue, expenses, completed tasks, bottlenecks, and generates executive briefing
  with proactive suggestions. Use when generating weekly report, business audit, or
  when user mentions "briefing", "ceo report", "performance summary".
user-invocable: true
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
model: sonnet
---
```

**Analysis Components:**
1. **Financial:** Weekly revenue/expenses vs targets, cash flow, cost optimization
2. **Operational:** Task completion, bottlenecks, email response times
3. **Social Media:** Engagement across 4 platforms, follower growth
4. **Business Goals:** Progress vs targets, at-risk goals
5. **Proactive Recommendations:** Unused subscriptions, process improvements, growth opportunities

**Automation:** Runs Sunday 11:45 PM, creates Monday morning notification

**Dependencies:** All previous skills operational (needs financial + social + operational data)

---

## Skill #10: monitor-system

**Purpose:** System health monitoring, error recovery, comprehensive audit logging

**Structure:**
```
monitor-system/
├── SKILL.md
├── reference/
│   ├── error-catalog.md
│   ├── recovery-procedures.md
│   ├── health-check-matrix.md
│   └── audit-log-schema.md
└── scripts/
    ├── health_monitor.py       # Every 5 min
    ├── error_handler.py
    ├── log_aggregator.py
    └── watchdog_manager.py
```

**Metadata:**
```yaml
---
name: monitor-system
description: Monitor system health, detect errors, implement recovery procedures,
  restart failed processes, maintain audit logs. Use for system health checks, error
  recovery, process monitoring, or when user mentions "system status", "errors", "logs".
user-invocable: true
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
model: sonnet
---
```

**Key Functions:**
- **Health Monitoring:** Check Watchers/MCP servers every 5 min, calculate health score (0-100)
- **Error Recovery:** Auto-restart crashed processes, retry API failures, clean disk space
- **Graceful Degradation:** Queue operations when services down
- **Audit Logging:** JSON logs for all actions, daily rotation, weekly archive

**Recovery Procedures:**
- Process crash → Auto-restart (3 attempts → escalate)
- API auth failure → Token refresh or reauth request
- Disk space low → Archive logs, compress, clean temp
- Network outage → Queue operations, retry when restored

**Dependencies:** All other skills operational

---

## Build Order

**Sequential (must follow order):**

```
Phase 2: manage-accounting (12-16h)
    └─ Required by CEO briefing
        ↓
Phase 3a: post-to-social-media (6-8h)
Phase 3b: post-to-twitter (4-6h)
    └─ Can build in parallel
        ↓
Phase 4: generate-ceo-briefing (8-12h)
    └─ Needs financial + social data
        ↓
Phase 5: monitor-system (10-14h)
    └─ Build last (needs all skills operational)
```

---

## Dependencies Matrix

| Skill | Must Build First | External Deps |
|-------|------------------|---------------|
| manage-accounting | handle-approval | Xero account + MCP |
| post-to-social-media | handle-approval | FB Business + IG |
| post-to-twitter | handle-approval | Twitter Dev Account |
| generate-ceo-briefing | All above skills | None (internal data) |
| monitor-system | All other skills | None |

---

## Success Metrics

**Gold Tier Achieved (80+/100 points):**

- **Functionality (40pts):** All 10 skills operational, 85%+ auto-activation, all APIs working
- **Business Intelligence (30pts):** Weekly briefings auto-generating, accurate financial sync, relevant recommendations
- **Multi-Platform (20pts):** 4 platforms posting, content calendar followed, metrics tracked
- **Reliability (10pts):** 99%+ uptime, auto-recovery working, audit logs maintained

**ROI:** 21.5 hours/week saved, $200-500/month cost savings, 200-400% ROI

---

## Quick Start

### Week 1: Financial Foundation
1. Set up Xero account + API credentials
2. Install Xero MCP Server
3. Build manage-accounting skill
4. Test transaction sync + categorization

### Week 2: Social Expansion
1. Set up Facebook Business + Instagram
2. Apply for Twitter Developer Account
3. Build post-to-social-media + post-to-twitter
4. Test posting to all platforms

### Week 3: Business Intelligence
1. Ensure all data sources operational
2. Build generate-ceo-briefing skill
3. Run manual test briefing
4. Set up Sunday night automation

### Week 4: System Hardening
1. Build monitor-system skill
2. Test error recovery scenarios
3. Verify audit logging
4. Create Gold Tier documentation + demo video

---

## Resources

- [Hackathon Guide](../hackathon.md)
- [Bronze-Silver Overview](./skills-overview-bronze-silver.md)
- [Gold Branching Strategy](../branches/gold.md)
- [Xero MCP Server](https://github.com/XeroAPI/xero-mcp-server)
- [Submission Form](https://forms.gle/JR9T1SJq5rmQyGkGA)

**Research Meetings:** Wednesdays 10:00 PM | [Zoom Link](https://us06web.zoom.us/j/87188707642) | Passcode: 744832

---

**Document Status:** ✅ Complete
**Next Action:** Set up Xero account and begin `manage-accounting` skill

*Last Updated: 2026-01-11*
