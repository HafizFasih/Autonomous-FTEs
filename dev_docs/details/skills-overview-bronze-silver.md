# Agent Skills Overview: Bronze to Silver Tier

**Document Version:** 1.0
**Last Updated:** 2026-01-11
**Project:** Autonomous FTE - Personal AI Employee

---

## 📚 Table of Contents

1. [Agent Skills Fundamentals](#agent-skills-fundamentals)
2. [Bronze Tier Skills](#bronze-tier-skills)
3. [Silver Tier Skills](#silver-tier-skills)
4. [Complete Skill Structure](#complete-skill-structure)
5. [Build Order Recommendations](#build-order-recommendations)

---

## Agent Skills Fundamentals

### What Are Agent Skills?

**Agent Skills** are specialized markdown files that teach Claude Code how to perform specific tasks. They extend Claude's capabilities for your particular workflow by providing custom instructions, standards, or procedures.

### 3-Part Logical Structure

Every comprehensive Agent Skill consists of:

#### 1. **Metadata** (YAML Frontmatter)
```yaml
---
name: skill-name               # REQUIRED: Skill identifier
description: What it does...   # REQUIRED: Triggers auto-activation
user-invocable: true           # OPTIONAL: Show in slash menu (default: true)
allowed-tools: [Read, Write]   # OPTIONAL: Restrict tool access
model: haiku                   # OPTIONAL: Use specific model
context: fork                  # OPTIONAL: Run in isolated context
---
```

#### 2. **Body** (Markdown Instructions)
- Main instructions Claude follows when skill activates
- Step-by-step procedures
- Core logic and decision trees
- Links to reference files
- **Best Practice:** Keep under 500 lines

#### 3. **Reference/Supporting Files**
- **Documentation:** Guidelines, examples, schemas, templates
- **Scripts:** Python/Bash/Node.js helper utilities
- **Data Files:** JSON configs, CSV templates
- **Loaded on-demand** (progressive disclosure pattern)

### How Skills Get Activated

1. **Discovery:** Claude loads only `name` and `description` at startup
2. **Matching:** When your request matches description, Claude asks to use the skill
3. **Activation:** You confirm (or it auto-activates)
4. **Execution:** Full SKILL.md loads, Claude follows instructions

### Best Practices for Descriptions

**Answer TWO questions:**
1. **What does this skill do?** (List specific capabilities)
2. **When should Claude use it?** (Include trigger terms users would say)

**✅ Good Description:**
```yaml
description: Process emails from Gmail Watcher, categorize by priority,
  draft responses using templates, flag urgent items. Use when processing
  emails, checking inbox, or when user mentions "email", "inbox", "gmail".
```

**❌ Weak Description:**
```yaml
description: Helps with email
```

---

## Bronze Tier Skills

### Requirements Summary
- ✅ Obsidian vault with Dashboard.md and Company_Handbook.md
- ✅ Basic folder structure: /Inbox, /Needs_Action, /Done
- ✅ One working Watcher script (file system)
- ✅ Claude Code integration
- ✅ **All AI functionality as Agent Skills**

### Skill #1: process-tasks (Current Implementation)

**Status:** ✅ Complete (Bronze Tier)

**Location:** `.claude/skills/process-tasks/`

**Current Structure:**
```
process-tasks/
└── SKILL.md
```

**Metadata:**
```yaml
---
name: process-tasks
description: Process pending tasks, check Needs_Action folder, complete task
  requests, move finished work to Done folder, and update activity dashboard.
  Use when the user asks to "process tasks", "check pending tasks",
  "handle Needs_Action items", "what tasks are waiting", or "complete pending work".
---
```

**Body Includes:**
1. Check Needs_Action folder
2. Read task files
3. Follow Company_Handbook rules
4. Complete task requests
5. Move completed files to Done
6. Update Dashboard.md with activity log

**Performance:** 70-80% auto-activation success rate

**Enhancement for Silver Tier:**
```
process-tasks/
├── SKILL.md
└── reference/
    └── task-templates.md     # Add standardized task formats
```

---

## Silver Tier Skills

### Requirements Summary
- ✅ All Bronze requirements
- Two or more Watcher scripts (Gmail + WhatsApp/LinkedIn)
- Automatically Post on LinkedIn
- Claude reasoning loop that creates Plan.md files
- One working MCP server for external action (email sending)
- Human-in-the-loop approval workflow
- Basic scheduling via cron or Task Scheduler
- **All AI functionality as Agent Skills**

### Total Skills Needed: 5

| # | Skill Name | Status | 3-Part Structure | Priority |
|---|------------|--------|------------------|----------|
| 1 | process-tasks | ✅ Bronze | ⚠️ 2-part (enhance to 3) | Low |
| 2 | process-emails | 🔴 New | ✅ Yes | High |
| 3 | post-to-linkedin | 🔴 New | ✅ Yes | Medium |
| 4 | create-plan | 🔴 New | ⚠️ 2-part sufficient | High |
| 5 | handle-approval | 🔴 New | ✅ Yes | Critical |

---

### Skill #2: process-emails (Silver Tier)

**Purpose:** Handle emails detected by Gmail Watcher, categorize by priority, draft responses, flag urgent items.

**Dependencies:**
- Gmail Watcher (Python script)
- Email MCP Server (for sending)
- Company_Handbook.md (for response guidelines)

**Complete Structure:**
```
process-emails/
├── SKILL.md
├── reference/
│   ├── email-templates.md      # Response templates by category
│   ├── priority-rules.md       # Urgency classification criteria
│   └── categorization.md       # Email categorization logic
└── scripts/
    └── parse_email_metadata.py # Extract sender, subject, urgency
```

**Metadata:**
```yaml
---
name: process-emails
description: Process emails from Gmail Watcher, categorize by priority
  (urgent/normal/low), draft appropriate responses using templates, flag
  items requiring immediate attention. Use when processing emails, checking
  inbox, handling Gmail notifications, or user mentions "email", "inbox",
  "gmail", "messages".
user-invocable: true
allowed-tools: [Read, Write, Edit, Grep, Glob]
---
```

**Body Steps:**
1. Check /Needs_Action for EMAIL_* files
2. Read email metadata (from, subject, body)
3. Categorize using [priority rules](./reference/priority-rules.md)
4. For urgent emails:
   - Flag in Dashboard
   - Create approval request if response needed
5. For normal emails:
   - Draft response using [templates](./reference/email-templates.md)
   - Create approval request in /Pending_Approval
6. Log all actions to Dashboard.md

**Trigger Phrases:**
- "process emails"
- "check my inbox"
- "handle email from [person]"
- "what emails need attention"
- "respond to emails"

**Reference Files:**

`email-templates.md`:
- Client inquiry template
- Invoice request template
- Meeting scheduling template
- Generic professional response
- Urgent matter escalation

`priority-rules.md`:
- Keywords indicating urgency
- VIP sender list
- Auto-approve vs requires approval
- Escalation criteria

`categorization.md`:
- Client communications
- Internal team
- Sales/leads
- Administrative
- Spam/low-priority

---

### Skill #3: post-to-linkedin (Silver Tier)

**Purpose:** Automatically generate and post business updates to LinkedIn for lead generation.

**Dependencies:**
- LinkedIn API integration or MCP Server
- Business_Goals.md (for content themes)
- Company_Handbook.md (for brand voice)

**Complete Structure:**
```
post-to-linkedin/
├── SKILL.md
├── reference/
│   ├── post-templates.md       # Business update templates
│   ├── content-guidelines.md   # Brand voice, tone, topics
│   └── hashtag-strategy.md     # Industry-relevant hashtags
└── scripts/
    └── linkedin_api_helper.py  # MCP server integration
```

**Metadata:**
```yaml
---
name: post-to-linkedin
description: Generate and post business updates to LinkedIn for sales generation.
  Creates professional posts about projects, achievements, industry insights.
  Use when user mentions "post to linkedin", "share on linkedin", "create linkedin
  post", "social media update", or scheduling automatic business updates.
user-invocable: true
allowed-tools: [Read, Write, Bash]
context: fork
---
```

**Body Steps:**
1. Check Business_Goals.md for active projects
2. Review recent completed tasks in /Done
3. Generate post content using [templates](./reference/post-templates.md)
4. Follow [content guidelines](./reference/content-guidelines.md)
5. Add relevant hashtags from [strategy](./reference/hashtag-strategy.md)
6. Create approval request in /Pending_Approval/LINKEDIN_POST_[date].md
7. Once approved, call LinkedIn MCP to publish
8. Log post to Dashboard.md

**Trigger Phrases:**
- "post to linkedin"
- "share on linkedin"
- "create linkedin post about [topic]"
- "social media update"
- "generate business post"

**Reference Files:**

`post-templates.md`:
- Project milestone announcement
- Client success story
- Industry insight/tip
- Service offering highlight
- Behind-the-scenes work

`content-guidelines.md`:
- Brand voice (professional, approachable, expert)
- Topics to cover/avoid
- Length guidelines (150-300 words optimal)
- Call-to-action patterns
- Emoji usage (minimal, professional)

`hashtag-strategy.md`:
- Industry-specific hashtags
- Trending professional topics
- Brand hashtags
- Location-based tags

---

### Skill #4: create-plan (Silver Tier)

**Purpose:** Generate structured Plan.md files for complex tasks requiring multi-step reasoning.

**Dependencies:**
- Company_Handbook.md (for planning standards)

**Structure (2-Part Sufficient):**
```
create-plan/
├── SKILL.md
└── reference/              # Optional
    └── plan-template.md    # Could be inline in SKILL.md
```

**Metadata:**
```yaml
---
name: create-plan
description: Create structured Plan.md files for complex multi-step tasks.
  Analyzes task requirements, breaks down into actionable steps, identifies
  dependencies, estimates complexity. Use when task requires planning, user
  asks to "create a plan", "plan this task", "break this down", or task has
  multiple components.
user-invocable: true
allowed-tools: [Read, Write, Glob]
---
```

**Body Steps:**
1. Analyze task from Needs_Action file
2. Break down into 3-7 actionable steps
3. Identify dependencies between steps
4. Flag steps requiring human approval
5. Create /Plans/PLAN_[task-name]_[date].md with:
   - Objective
   - Background/Context
   - Step-by-step checklist
   - Approval requirements
   - Success criteria
6. Update Dashboard with plan creation

**Trigger Phrases:**
- "create a plan"
- "plan this task"
- "break this down"
- "what are the steps"
- "generate plan.md"

**Plan.md Template (Inline):**
```markdown
---
created: [timestamp]
status: pending_approval / in_progress / completed
task_source: [source file]
---

## Objective
[Clear statement of what needs to be accomplished]

## Background
[Context, why this task matters]

## Steps
- [ ] Step 1: Description (Est: 10 min)
- [ ] Step 2: Description (Est: 20 min) [REQUIRES APPROVAL]
- [ ] Step 3: Description (Est: 15 min)

## Dependencies
- Step 2 depends on Step 1 completion
- External: Requires API access

## Approval Requirements
Steps requiring human approval: 2

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Notes
[Any additional context]
```

---

### Skill #5: handle-approval (Silver Tier)

**Purpose:** Manage human-in-the-loop approval workflow for sensitive actions.

**Dependencies:**
- /Pending_Approval, /Approved, /Rejected folders
- Company_Handbook.md (for approval thresholds)

**Complete Structure:**
```
handle-approval/
├── SKILL.md
├── reference/
│   ├── approval-thresholds.md  # What requires approval
│   ├── approval-template.md    # Format for approval requests
│   └── security-rules.md       # Payment limits, sensitive actions
└── scripts/
    └── check_approval_status.py # Monitor approval folders
```

**Metadata:**
```yaml
---
name: handle-approval
description: Manage human-in-the-loop approval workflow for sensitive actions
  like payments, email sending, social media posts. Creates approval requests,
  monitors approval status, executes approved actions, logs all decisions. Use
  when action requires approval, user mentions "check approvals", "pending
  approval", "approve this", or before executing sensitive operations.
user-invocable: true
allowed-tools: [Read, Write, Bash, Glob]
---
```

**Body Steps:**
1. **When creating approval request:**
   - Determine action type (payment/email/social/file)
   - Check [approval thresholds](./reference/approval-thresholds.md)
   - Create APPROVAL_[type]_[description]_[date].md in /Pending_Approval
   - Use [standard template](./reference/approval-template.md)
   - Include: action details, reason, risks, deadline
   - Log request to Dashboard

2. **When checking approvals:**
   - Scan /Approved folder for new files
   - Validate approval format
   - Execute approved action via MCP
   - Move file to /Done
   - Log execution to Dashboard

3. **When handling rejections:**
   - Scan /Rejected folder
   - Log rejection reason
   - Archive in /Done with rejection note
   - Update Dashboard

**Trigger Phrases:**
- "check approvals"
- "handle pending approvals"
- "what needs approval"
- "approve this action"
- "check approval status"

**Reference Files:**

`approval-thresholds.md`:
```markdown
# Approval Thresholds

## Email Actions
- **Auto-approve:** Replies to known contacts < 200 words
- **Require approval:** New contacts, bulk sends, attachments

## Payments
- **Auto-approve:** Recurring payments < $50
- **Require approval:** All new payees, any payment > $100

## Social Media
- **Auto-approve:** None (all posts require approval)
- **Require approval:** All LinkedIn/Twitter/Facebook posts

## File Operations
- **Auto-approve:** Create/read in vault
- **Require approval:** Delete, move outside vault, system files

## Sensitive Data
- **Require approval:** Any action involving passwords, API keys, PII
```

`approval-template.md`:
```markdown
---
type: approval_request
action: [payment/email/social/file/other]
created: [timestamp]
expires: [24 hours from creation]
priority: [low/normal/high/urgent]
status: pending
---

## Action Summary
[One-line description]

## Details
- **Action Type:** [Type]
- **Target:** [Email address / Amount / Platform]
- **Reason:** [Why this action is needed]

## Parameters
- Parameter 1: Value
- Parameter 2: Value

## Risks & Considerations
- Risk 1: Description
- Risk 2: Description

## To Approve
Move this file to `/Approved` folder.

## To Reject
Move this file to `/Rejected` folder and add reason at bottom.

---
## Execution Log
[Filled after approval/rejection]
```

`security-rules.md`:
```markdown
# Security Rules for Approvals

## Never Auto-Approve
1. Financial transactions to new recipients
2. Changes to security settings
3. Deletion of important files
4. Public social media posts
5. Sharing of credentials or sensitive data

## Required Validation
- Verify recipient identity (email/payment)
- Check for typos in amounts/addresses
- Validate against Business_Goals.md
- Ensure within budget thresholds

## Expiration Policy
- Payment approvals: 24 hours
- Email approvals: 48 hours
- Social posts: 72 hours
- Expired requests auto-archive

## Audit Requirements
- Log all approval decisions
- Track approval response time
- Monthly review of auto-approve rules
```

---

## Complete Skill Structure

### Directory Tree (Bronze + Silver)

```
.claude/skills/
│
├── process-tasks/              # ✅ BRONZE (Enhanced for Silver)
│   ├── SKILL.md
│   └── reference/
│       └── task-templates.md
│
├── process-emails/             # 🔴 SILVER - NEW
│   ├── SKILL.md
│   ├── reference/
│   │   ├── email-templates.md
│   │   ├── priority-rules.md
│   │   └── categorization.md
│   └── scripts/
│       └── parse_email_metadata.py
│
├── post-to-linkedin/           # 🔴 SILVER - NEW
│   ├── SKILL.md
│   ├── reference/
│   │   ├── post-templates.md
│   │   ├── content-guidelines.md
│   │   └── hashtag-strategy.md
│   └── scripts/
│       └── linkedin_api_helper.py
│
├── create-plan/                # 🔴 SILVER - NEW
│   ├── SKILL.md
│   └── reference/              # Optional
│       └── plan-template.md
│
└── handle-approval/            # 🔴 SILVER - NEW
    ├── SKILL.md
    ├── reference/
    │   ├── approval-thresholds.md
    │   ├── approval-template.md
    │   └── security-rules.md
    └── scripts/
        └── check_approval_status.py
```

### File Count Summary

| Tier | Total Skills | SKILL.md Files | Reference Files | Script Files | Total Files |
|------|-------------|----------------|-----------------|--------------|-------------|
| Bronze | 1 | 1 | 0 | 0 | 1 |
| Silver | 5 | 5 | 13 | 3 | 21 |

---

## Build Order Recommendations

### Phase 1: Foundation (Critical Path)
**Priority:** Critical
**Time:** 4-6 hours

1. **handle-approval** (Build First)
   - Required by all other skills
   - Foundation for safety
   - Create all 3 parts (metadata, body, reference files)
   - Test with dummy approval requests

2. **create-plan** (Build Second)
   - Needed for complex task decomposition
   - Simpler 2-part structure
   - Test with multi-step task scenarios

### Phase 2: External Integration (Sequential)
**Priority:** High
**Time:** 8-12 hours

3. **process-emails** (Build Third)
   - Depends on: Gmail Watcher + Email MCP Server
   - Build Gmail Watcher first (Python script)
   - Set up Email MCP Server
   - Then create skill with all 3 parts
   - Test with sample emails

### Phase 3: Social Media (Medium)
**Priority:** Medium
**Time:** 4-6 hours

4. **post-to-linkedin** (Build Fourth)
   - Depends on: LinkedIn API/MCP integration
   - Set up LinkedIn API access
   - Create skill with templates
   - Test in sandbox mode (dry-run)

### Phase 4: Enhancement (Low)
**Priority:** Low
**Time:** 1-2 hours

5. **Enhance process-tasks** (Build Last)
   - Add reference folder
   - Add task-templates.md
   - Minimal changes to existing working skill

---

## Dependencies Matrix

| Skill | Depends On | Must Build First |
|-------|-----------|------------------|
| handle-approval | Folder structure | None (build first) |
| create-plan | handle-approval | handle-approval |
| process-emails | Gmail Watcher, Email MCP, handle-approval | handle-approval, Gmail Watcher |
| post-to-linkedin | LinkedIn API/MCP, handle-approval | handle-approval, LinkedIn integration |
| process-tasks (enhance) | None | All others (build last) |

---

## Skills vs. Other Components

### What Are NOT Skills

**Watcher Scripts** (Perception Layer)
- `filesystem_watcher.py` ✅ Bronze
- `gmail_watcher.py` 🔴 Silver - Needed
- `whatsapp_watcher.py` 🔴 Silver - Optional
- These are **Python scripts** that run continuously
- They **create files** in /Needs_Action
- Skills **process** what watchers detect

**MCP Servers** (Action Layer)
- Email MCP Server 🔴 Silver - Needed
- LinkedIn API MCP 🔴 Silver - Needed
- Browser MCP 🟡 Gold - Future
- These are **external tools** Claude calls
- Skills **use** MCP servers to execute actions
- Separate from skill system

**Obsidian Vault Files** (Memory Layer)
- Dashboard.md ✅ Bronze
- Company_Handbook.md ✅ Bronze
- Business_Goals.md 🔴 Silver - Needed
- These are **data/config** files
- Skills **read** and **update** these files
- Not part of skill system

---

## Testing Strategy

### Per-Skill Testing

1. **Metadata Testing**
   - Verify skill appears in `/skills` command
   - Test auto-activation with trigger phrases
   - Confirm description clarity

2. **Body Testing**
   - Run skill with sample input
   - Verify step-by-step execution
   - Check error handling

3. **Reference File Testing**
   - Ensure links work in SKILL.md
   - Verify Claude loads reference files on-demand
   - Test script execution

### Integration Testing

1. **End-to-End Workflow**
   - Watcher detects event → File in Needs_Action
   - Skill auto-activates → Processes task
   - Creates approval request → Human approves
   - Action executes → Logs to Dashboard

2. **Skill Interaction**
   - process-emails calls handle-approval
   - create-plan calls handle-approval
   - post-to-linkedin calls handle-approval

---

## Success Metrics

### Bronze Tier
- ✅ 1 skill working with 70-80% auto-activation
- ✅ Can process file-based tasks
- ✅ Updates Dashboard correctly

### Silver Tier (Target)
- 5 skills with 75-85% auto-activation
- Email processing automated
- LinkedIn posting with approval
- Human-in-the-loop workflow operational
- Plan generation for complex tasks
- All AI functionality as Agent Skills ✅

---

## Next Steps

### Immediate Actions
1. Create `/Pending_Approval`, `/Approved`, `/Rejected` folders
2. Create `Business_Goals.md` in vault root
3. Build **handle-approval** skill (all 3 parts)
4. Test approval workflow with dummy request

### Week 1 Goals
- ✅ handle-approval skill complete and tested
- ✅ create-plan skill complete and tested
- ✅ Gmail Watcher implemented
- ✅ Email MCP Server configured

### Week 2 Goals
- ✅ process-emails skill complete
- ✅ LinkedIn API/MCP integration
- ✅ post-to-linkedin skill complete
- ✅ Scheduling system (cron/Task Scheduler)

### Week 3 Goals
- ✅ All 5 skills tested end-to-end
- ✅ Silver Tier documentation complete
- ✅ Demo video recorded
- ✅ Submit Silver Tier completion

---

## Resources

### Official Documentation
- [Claude Code Skills](https://code.claude.com/docs/en/skills)
- [Agent Skills Overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [MCP Protocol](https://modelcontextprotocol.io/)

### Hackathon Resources
- [Hackathon Document](../hackathon.md)
- [Bronze Tier Completion](../progress/bronze-tier-completion.md)
- [Project README](../README.md)
- [Company Handbook](../Company_Handbook.md)

### Research Meetings
- **Every Wednesday 10:00 PM**
- Zoom: https://us06web.zoom.us/j/87188707642
- Passcode: 744832

---

**Document Status:** ✅ Complete
**Ready for Silver Tier Implementation:** Yes
**Next Action:** Build `handle-approval` skill

---

*Generated: 2026-01-11*
*Project: Autonomous FTE - Personal AI Employee*
*Tier: Bronze → Silver Transition*
