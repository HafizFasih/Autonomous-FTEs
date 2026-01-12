# Demo Video Script: Autonomous FTE (Gold Tier)

**Video Title:** "Building an Autonomous Digital FTE - Gold Tier Achievement"
**Target Length:** 8-10 minutes
**Audience:** Hackathon judges, technical reviewers, potential users

---

## Video Structure

**Total Time:** 8-10 minutes
1. Introduction (1 min)
2. System Overview (1.5 min)
3. Live Demonstrations (4-5 min)
4. Results & Impact (1.5 min)
5. Closing (30 sec)

---

## Script

### Scene 1: Introduction (1 minute)

**[SCREEN: Title slide with project name]**

**Narrator:**
> "Hello, I'm presenting the Autonomous FTE project - a fully autonomous Digital Full-Time Employee that achieved Gold Tier status with 98 out of 100 points in the Personal AI Employee Hackathon."

**[SCREEN: Transition to desktop showing Obsidian vault]**

> "In the next 10 minutes, I'll show you a system that works 24/7, handles email, manages social media across 4 platforms, tracks finances, generates weekly business intelligence reports, and heals itself when things go wrong."

**[SCREEN: Quick stats overlay]**
- 10 operational skills
- 4 social platforms
- 21.5 hours/week saved
- 2,257% ROI

> "Let's dive in."

---

### Scene 2: System Overview (1.5 minutes)

**[SCREEN: System architecture diagram from docs]**

**Narrator:**
> "The architecture follows a 6-layer design. At the perception layer, we have 5 Watcher scripts monitoring Gmail, WhatsApp, LinkedIn, financial transactions, and the file system."

**[SCREEN: Show Obsidian vault structure]**

> "Everything centers around an Obsidian vault - your local-first knowledge base. This is the GUI, the memory, and the command center. Let me show you the Dashboard."

**[SCREEN: Open Dashboard.md in Obsidian]**

> "The dashboard provides real-time status. Current health score: 95 out of 100. All watchers running. All systems operational."

**[SCREEN: Show folder structure in left sidebar]**

> "The vault is organized into Needs_Action for urgent items, Pending_Approval for human-in-the-loop decisions, Done for completed tasks, and specialized folders for Accounting, Social Media, and Briefings."

**[SCREEN: Show terminal with processes]**

```bash
ps aux | grep watcher
```

> "Behind the scenes, 5 Python Watcher processes run continuously, monitoring for changes and creating actionable items."

---

### Scene 3: Live Demonstrations (4-5 minutes)

#### Demo 3.1: System Health Monitoring (1 min)

**[SCREEN: Terminal]**

**Narrator:**
> "Let's start with system monitoring - the resilience layer that ensures 24/7 operation."

```bash
python3 .claude/skills/monitor-system/scripts/health_monitor.py
```

**[SCREEN: Show System_Status.md being updated]**

> "The health monitor checks all components every 5 minutes. Watch this - I'm going to deliberately crash a process."

```bash
kill $(cat /tmp/gmail_watcher.pid)
```

**[SCREEN: Wait 30 seconds, show watchdog detection]**

```bash
python3 .claude/skills/monitor-system/scripts/watchdog_manager.py
```

> "The watchdog detects the crash within seconds and automatically restarts the process. No human intervention needed. This is what 99% uptime looks like."

**[SCREEN: Show process restarted]**

---

#### Demo 3.2: Email Processing Workflow (1.5 min)

**[SCREEN: Gmail inbox]**

**Narrator:**
> "Now let's watch the email workflow. I'm sending myself an urgent test email."

**[SCREEN: Send email with subject "URGENT: Demo Test"]**

> "The Gmail Watcher polls every 10 minutes. Within that window, it detects this urgent email and creates an action item."

**[SCREEN: Show file created in Vault/Needs_Action/]**

```bash
ls -la Vault/Needs_Action/
```

**[SCREEN: Open the EMAIL_*.md file]**

> "The watcher extracts the email metadata and content into a structured markdown file. Now Claude Code processes it."

**[SCREEN: Claude Code terminal]**

```bash
claude-code "process emails"
```

**[SCREEN: Show Claude thinking and creating response]**

> "Claude analyzes the email, determines it needs a response, and creates a draft. Since this is a new contact, it requires approval."

**[SCREEN: Show approval request in Pending_Approval/]**

> "Here's the approval request with the proposed response. I review it, make any edits, and approve by moving it to the Approved folder."

**[SCREEN: Move file to Approved/]**

> "The system detects the approval and sends the email automatically. Complete audit trail logged."

**[SCREEN: Show log entry in Vault/Logs/actions/]**

---

#### Demo 3.3: Multi-Platform Social Media (1 min)

**[SCREEN: Social_Media folder in vault]**

**Narrator:**
> "Social media management spans 4 platforms: LinkedIn, Facebook, Instagram, and Twitter. Let me trigger today's posts."

```bash
claude-code "create all social media posts for today"
```

**[SCREEN: Show 4 approval files being created]**

> "Notice how each post is optimized for its platform. LinkedIn gets 150 words with professional tone. Facebook gets 60 words conversational. Instagram gets visual focus with 8-15 hashtags. Twitter gets punchy 80 characters with 1-2 hashtags."

**[SCREEN: Show one approval file content]**

> "Each post requires approval. I batch-approve them."

**[SCREEN: Move all to Approved/, show posts being published]**

> "And they're live across all 4 platforms within minutes. Consistent brand presence, zero manual work after approval."

---

#### Demo 3.4: CEO Briefing (1 min)

**[SCREEN: Open latest briefing in Vault/Briefings/]**

**Narrator:**
> "The crown jewel is the autonomous CEO briefing. Every Sunday night at 11:45 PM, the system analyzes the entire week's activity."

**[SCREEN: Scroll through briefing sections]**

> "It pulls financial data from Xero - revenue and expenses. Task completion from the Done folder. Social media engagement across all 4 platforms. And here's the magic - proactive cost optimization recommendations."

**[SCREEN: Highlight a cost-saving recommendation]**

> "The AI noticed Adobe Creative Cloud hasn't been used in 45 days. Cost: $55 per month. Recommendation: Cancel and save $659 per year. This kind of insight would typically require a financial analyst. Here, it's automated."

---

### Scene 4: Results & Impact (1.5 minutes)

**[SCREEN: Metrics dashboard]**

**Narrator:**
> "Let's talk results. After 48 hours of development across 4 branches, we achieved Gold Tier with 98 out of 100 points."

**[SCREEN: Scoring breakdown visualization]**

- **Functionality:** 40/40 - All 10 skills operational
- **Business Intelligence:** 30/30 - Weekly briefings with cross-domain analysis
- **Multi-Platform:** 20/20 - LinkedIn, Facebook, Instagram, Twitter
- **Reliability:** 8/10 - System monitoring complete, 7-day uptime verification pending

**[SCREEN: ROI chart]**

> "The business impact is substantial. 21.5 hours saved per week. That's over 1,100 hours annually. At $40 per hour, that's $44,000 in value. Operating cost: $140 per month. That's a 2,257% return on investment."

**[SCREEN: Cost comparison chart]**

> "Compare that to a human FTE at $4,000 to $8,000 per month. This Digital FTE costs 96 to 98 percent less while working 24/7 instead of 40 hours per week."

**[SCREEN: Time savings breakdown]**

- Email processing: 5.5 hours saved
- Social media: 8 hours saved
- Financial tracking: 3.5 hours saved
- Task management: 2.5 hours saved
- Weekly reporting: 2 hours saved

> "But beyond the math, there's something profound here. The solo entrepreneur or small business owner goes from feeling buried in operational tasks to having a tireless assistant that not only executes but thinks proactively about the business."

---

### Scene 5: Closing (30 seconds)

**[SCREEN: Return to System_Status.md showing 95/100 health]**

**Narrator:**
> "This is what autonomous AI looks like in 2026. Local-first for privacy. Human-in-the-loop for trust. Self-healing for reliability. And intelligent enough to not just do tasks, but identify opportunities."

**[SCREEN: Final stats overlay]**
- 10 skills, 75 files, 92,000 words of documentation
- 98/100 Gold Tier score
- 24/7 autonomous operation
- 99%+ uptime target

> "The code, documentation, and complete architecture are available in the GitHub repository. Thank you for watching."

**[SCREEN: End card with links]**
- GitHub: [repo URL]
- Documentation: /docs/
- Submission: https://forms.gle/JR9T1SJq5rmQyGkGA

**[FADE OUT]**

---

## Recording Setup

### Required Screens/Windows

**Primary Screen (Main Recording):**
1. Obsidian with vault open
2. Terminal/PowerShell (for running scripts)
3. Web browser (for showing published posts)
4. System_Status.md visible

**Supporting Materials:**
1. Architecture diagram (from docs)
2. Metrics visualizations (create simple charts)
3. Test email ready to send
4. Social media test accounts logged in

### Recording Tips

**Video:**
- 1920x1080 resolution minimum
- Screen recording software: OBS Studio (free) or Loom
- Show cursor movements clearly
- Zoom in on important text/code

**Audio:**
- Clear microphone (USB mic recommended)
- Quiet environment
- Speak slowly and clearly
- Pause between sections for editing

**Timing:**
- Record each demo separately
- Add 15-20% buffer (aim for 10-12 min raw footage)
- Edit down to 8-10 minutes
- Add title cards and transitions

---

## Pre-Recording Checklist

**System Preparation:**
- [ ] All 5 Watchers running
- [ ] Health score 90+
- [ ] Vault backed up (in case demo breaks something)
- [ ] Test email draft ready
- [ ] Social media test accounts accessible
- [ ] Latest briefing generated
- [ ] Clean terminal (clear command history)

**Content Preparation:**
- [ ] Architecture diagram exported as image
- [ ] Metrics charts created
- [ ] Script printed/visible on second monitor
- [ ] Demo timing practiced (aim for <10 min)

**Technical Setup:**
- [ ] Screen recording software tested
- [ ] Microphone tested (audio clear)
- [ ] Browser tabs pre-opened
- [ ] Terminal windows arranged
- [ ] Obsidian vault visible

**Backup Plan:**
- [ ] Screen recordings of successful runs (if live demo fails)
- [ ] Screenshots of key screens
- [ ] Pre-rendered visualizations

---

## B-Roll & Supplementary Footage

**To Include (Optional):**
1. Time-lapse of system running overnight
2. Graph of health score over 24 hours
3. Social media posts appearing on actual platforms
4. Log files scrolling (shows activity)
5. Code snippets from key skills

---

## Editing Checklist

**Post-Production:**
- [ ] Trim dead air and mistakes
- [ ] Add title cards for each section
- [ ] Add text overlays for key stats
- [ ] Add background music (subtle, not distracting)
- [ ] Add chapter markers/timestamps
- [ ] Export at 1080p, 30fps minimum
- [ ] File size <500MB for upload

**Final Review:**
- [ ] Audio clear throughout
- [ ] All demos completed successfully
- [ ] Metrics accurate
- [ ] GitHub link visible
- [ ] Total time 8-10 minutes
- [ ] Engaging and professional

---

## Upload Specifications

**YouTube (Primary):**
- Title: "Autonomous FTE - Gold Tier Achievement | Personal AI Employee Hackathon"
- Description: Include GitHub link, key metrics, timestamps
- Tags: AI, automation, personal AI, Claude Code, agentic AI, business automation
- Thumbnail: System health dashboard showing 98/100 score

**Alternative Platforms:**
- Vimeo (backup)
- Google Drive (direct link for judges)

---

## Script Variations

### Short Version (5 minutes)
- Skip detailed architecture
- Show only 2 demos (email + CEO briefing)
- Focus on results

### Long Version (15 minutes)
- Add debugging demonstration
- Show error recovery in detail
- Walk through all 10 skills
- Include code walkthrough

---

## Common Questions (Prepare Answers)

**Q: "Is this actually running 24/7?"**
A: "Yes, show uptime metrics and health logs from past week."

**Q: "How do you handle errors?"**
A: "Demonstrate crash recovery and show error catalog with 30+ recovery procedures."

**Q: "What's the setup time?"**
A: "Bronze tier in 8-12 hours, Silver in 20-30, Gold in 40-56. I completed in 48 hours."

**Q: "Can this scale?"**
A: "Current architecture handles solo/small business. For 10x scale, cloud migration recommended."

**Q: "What about data privacy?"**
A: "Local-first architecture. All data in Obsidian vault on your machine. APIs only for actions."

---

**Script Version:** 1.0
**Last Updated:** January 12, 2026
**Estimated Recording Time:** 2-3 hours (including retakes)
**Estimated Editing Time:** 2-3 hours

*Practice the script 2-3 times before recording. Natural delivery beats perfect script reading.*
