# Demo Video Script - Silver Tier Autonomous AI Employee

**Target Duration:** 5-10 minutes
**Audience:** Hackathon judges, technical evaluators
**Goal:** Demonstrate working Silver Tier autonomous AI employee system

---

## Video Structure

### Opening (30 seconds)

**On Screen:**
- Project title slide
- "Autonomous AI Employee - Silver Tier Complete"
- Your name/team

**Voiceover Script:**
```
"Hi, I'm [Your Name], and I've built a fully functional Autonomous AI Employee
that operates 24/7, managing emails, creating LinkedIn content, and handling
sensitive decisions with human-in-the-loop approval.

Let me show you how it works."
```

---

## Part 1: System Overview (1 minute)

**Screen Recording:** Show file/folder structure

**Voiceover Script:**
```
"The system follows a local-first architecture built on three pillars:

1. Obsidian serves as the AI's memory and dashboard - everything is stored
   as plain markdown files on my machine.

2. Claude Code acts as the reasoning engine, reading from and writing to
   the Obsidian vault.

3. Python watchers monitor Gmail and the filesystem 24/7, creating tasks
   for the AI to process.

The AI can't take sensitive actions automatically - it creates approval
requests that I review before anything happens. This makes it safe and trustworthy."
```

**Show on Screen:**
- Obsidian vault structure
- Dashboard.md (briefly)
- Folder tree: /Inbox, /Needs_Action, /Pending_Approval, /Approved, /Done

---

## Part 2: Email Automation Demo (2-3 minutes)

### Scene 1: Email Arrives

**Screen Recording:**
1. Show test email in Gmail OR show dummy email file creation
2. Show Gmail watcher detecting it (if running) OR manually create EMAIL_*.md in /Needs_Action

**Voiceover Script:**
```
"Let's demonstrate email processing. A potential client just sent an inquiry
about our services. The Gmail watcher detects this important email and creates
a task file in the Needs_Action folder."
```

### Scene 2: AI Processes Email

**Screen Recording:**
1. Open terminal/Claude Code
2. Type: "Check my pending emails" or "Process tasks"
3. Show `process-emails` skill activating

**Voiceover Script:**
```
"I tell the AI to check pending tasks. The process-emails skill automatically
activates because it recognizes email-related keywords in my request.

Watch as the AI:
- Reads the email content
- Categorizes it as a sales lead with high priority
- Drafts a professional response using our templates
- Creates an approval request"
```

### Scene 3: Review Approval Request

**Screen Recording:**
1. Navigate to /Pending_Approval folder
2. Open the approval file (APPROVAL_EMAIL_*.md)
3. Show the YAML frontmatter and drafted response

**Voiceover Script:**
```
"Here's the approval request. It contains all the metadata - who it's going to,
what the risk level is, when it expires - and the full drafted response.

I can review it, edit the content if needed, and then approve or reject it
simply by moving the file to the appropriate folder. No complicated UI needed -
just drag and drop."
```

### Scene 4: Approve and Execute (Optional)

**Screen Recording:**
1. Move file to /Approved
2. (If email MCP configured) Show execution
3. Show Dashboard updated with log

**Voiceover Script:**
```
"I approve it by moving the file to the Approved folder. The system logs
everything to the Dashboard for a complete audit trail. In production with
the Gmail API configured, this would send the email automatically."
```

---

## Part 3: LinkedIn Content Generation Demo (2-3 minutes)

### Scene 1: Request LinkedIn Post

**Screen Recording:**
1. Open Claude Code
2. Type: "Create a LinkedIn post about completing the Silver Tier hackathon"

**Voiceover Script:**
```
"Now let's see LinkedIn automation. I ask the AI to create a LinkedIn post
about completing this hackathon project."
```

### Scene 2: AI Generates Content

**Screen Recording:**
1. Show `post-to-linkedin` skill activating
2. Show it reading Business_Goals.md (briefly)
3. Show progress messages as it works

**Voiceover Script:**
```
"The post-to-linkedin skill activates and:
- Reads my business goals to understand content themes
- Selects the appropriate template - in this case, 'Project Milestone'
- Generates a professional post following our brand voice guidelines
- Adds strategic hashtags from our library
- Creates an approval request"
```

### Scene 3: Review Generated Post

**Screen Recording:**
1. Navigate to /Pending_Approval
2. Open APPROVAL_LINKEDIN_*.md
3. Show the generated post content
4. Highlight the metadata (word count, hashtags, platform validation)

**Voiceover Script:**
```
"Here's the generated LinkedIn post. The AI followed our brand voice -
professional but approachable, expert without arrogance.

It selected 4 relevant hashtags from our strategy library, kept the length
optimal at 150-300 words, and included a clear call-to-action.

The approval file shows the full post ready for LinkedIn, complete with
metadata and the option for me to edit before posting."
```

### Scene 4: Quality Standards

**Screen Recording:**
1. Open `.claude/skills/post-to-linkedin/reference/content-guidelines.md` (briefly scroll)
2. Show brand voice section
3. Show quality checklist

**Voiceover Script:**
```
"The AI follows comprehensive content guidelines that ensure every post
maintains our brand voice and meets quality standards. This isn't random
AI generation - it's template-driven content with strict quality controls."
```

---

## Part 4: Safety & Approval System Demo (1-2 minutes)

### Scene 1: Show handle-approval Skill

**Screen Recording:**
1. Open `.claude/skills/handle-approval/SKILL.md` (briefly)
2. Open `reference/approval-thresholds.md`
3. Highlight "Never Auto-Approve" section

**Voiceover Script:**
```
"Safety is built into the architecture. The handle-approval skill manages all
sensitive actions. Look at these thresholds - emails to new contacts, all
social media posts, any payments over $100 - they ALL require human approval.

There's a 'Never Auto-Approve' list with zero tolerance. The AI physically
cannot send an email, post to social media, or make a payment without my
explicit approval."
```

### Scene 2: Dashboard Audit Trail

**Screen Recording:**
1. Open Dashboard.md
2. Scroll through activity log
3. Highlight timestamps, actions, and status

**Voiceover Script:**
```
"Every action is logged to the Dashboard with timestamps, status, and full
details. This creates a complete audit trail. If something goes wrong, I can
trace exactly what happened and when."
```

---

## Part 5: Technical Architecture (1 minute)

**Screen Recording:**
1. Show `.claude/skills/` directory structure
2. Briefly show one skill file structure (3-part: SKILL.md + reference/ + scripts/)
3. Show watchers directory
4. Show scripts

**Voiceover Script:**
```
"The system follows Claude Code's official best practices. Each skill has a
3-part structure:
- SKILL.md under 500 lines
- Reference files with detailed guidelines loaded on-demand
- Scripts for external integrations

All 5 skills follow this pattern, making the system maintainable and extensible.

The watchers run continuously monitoring inputs. The scripts handle external
APIs like Gmail and LinkedIn. Everything is modular and testable."
```

---

## Part 6: Testing & Validation (30 seconds)

**Screen Recording:**
1. Run dry-run test: `python linkedin_api_helper.py --approval-file "path" --dry-run --json`
2. Show JSON output with success status

**Voiceover Script:**
```
"Every component has a dry-run mode for safe testing. Here's the LinkedIn
helper script validating a post without actually publishing it. This prevented
countless mistakes during development and makes the system safe to iterate on."
```

---

## Part 7: Results & Statistics (1 minute)

**Screen Recording:**
1. Show `SILVER-TIER-COMPLETE.md` (scroll through statistics section)
2. Highlight key numbers

**Voiceover Script:**
```
"Here are the results:
- 5 production-ready skills
- 13 comprehensive reference files
- 6 functional automation scripts
- Nearly 14,000 lines of code and documentation
- All completed in about 15 hours

More importantly, the system is actually useful:
- Email processing time: 2 hours down to 20 minutes per day
- Zero missed messages with 24/7 monitoring
- Professional LinkedIn content without the writing struggle
- Complete control with human-in-the-loop approval

This isn't theoretical - it's production-ready."
```

---

## Closing (30 seconds)

**Screen Recording:**
- Show final folder structure
- Show all 5 skills in `.claude/skills/`
- End on Dashboard.md showing successful operations

**Voiceover Script:**
```
"I've built a fully autonomous AI employee that operates 24/7, maintains
professional standards, and keeps humans firmly in control of sensitive
decisions.

It's local-first for privacy, follows all Claude Code best practices, and
includes comprehensive documentation for every component.

Silver Tier: Complete. Thank you for watching!"
```

**End Screen:**
- GitHub repository link
- "Silver Tier - 100% Complete"
- Contact information (optional)

---

## Recording Tips

### Technical Setup

1. **Screen Resolution:** 1920x1080 or 1280x720 (720p minimum)
2. **Screen Recording Software:**
   - Windows: OBS Studio (free) or Camtasia
   - Mac: QuickTime or ScreenFlow
   - Linux: SimpleScreenRecorder or OBS Studio

3. **Audio:**
   - Use a decent microphone (even phone earbuds are better than laptop mic)
   - Record in a quiet room
   - Test audio levels before full recording

### Recording Strategy

**Option A: Single Take (Harder but Faster)**
- Rehearse the full script 2-3 times
- Record everything in one go
- Requires good preparation

**Option B: Scene-by-Scene (Easier, More Time)**
- Record each part separately
- Edit together in video editor (DaVinci Resolve is free)
- Easier to fix mistakes
- Can re-record any section

**Recommended: Option B for first-time demo videos**

### Before Recording Checklist

- [ ] Close unnecessary applications
- [ ] Disable notifications (Windows: Focus Assist, Mac: Do Not Disturb)
- [ ] Clean up desktop and taskbar
- [ ] Prepare all files/folders you'll show
- [ ] Test screen recording software
- [ ] Test audio levels
- [ ] Have water nearby for voiceover
- [ ] Browser bookmarks cleaned up (if showing browser)

### During Recording

- **Speak Clearly:** Enunciate, don't rush
- **Pace Yourself:** Pause between major points
- **Mouse Movements:** Slow and deliberate (fast mouse is hard to follow)
- **Highlights:** Use cursor to point at important text
- **Zoom In:** If showing code or small text, zoom in (Ctrl + or Cmd +)

### Quick Edits (If Needed)

**Free Tools:**
- **DaVinci Resolve** (Windows/Mac/Linux) - Professional grade, free
- **Shotcut** (Windows/Mac/Linux) - Simpler, still powerful
- **iMovie** (Mac) - Built-in, easy to use

**Basic Editing:**
1. Cut out mistakes/long pauses
2. Add title screen at start
3. Add closing screen at end
4. Optional: Add text overlays for key points
5. Optional: Background music (keep very quiet, don't distract)

### Export Settings

- **Format:** MP4 (H.264 codec)
- **Resolution:** 1920x1080 or 1280x720
- **Frame Rate:** 30 fps
- **Audio:** AAC, 128 kbps or higher
- **Target File Size:** Under 500 MB if possible (YouTube/Google Drive friendly)

---

## Alternative: Live Demo (Risky but Impressive)

If you're confident, you can do a live screen recording with real-time narration:

**Advantages:**
- More authentic
- Shows real system performance
- No editing needed

**Disadvantages:**
- One mistake = start over
- No post-production polish
- Higher stress

**Only recommended if:**
- You've rehearsed extensively
- System is 100% stable
- You're comfortable with public speaking

---

## Upload & Share

### Upload Platforms (Choose One)

1. **YouTube (Unlisted)** - Recommended
   - Easy to share via link
   - No file size limits
   - Good quality
   - Link: Include in hackathon submission

2. **Google Drive**
   - If judges need direct file
   - Set permissions to "Anyone with link"
   - Less professional than YouTube

3. **Vimeo**
   - Professional appearance
   - Good quality
   - Free tier has limits

### Final Checklist Before Submission

- [ ] Video renders correctly (watch full video)
- [ ] Audio is clear throughout
- [ ] All important text is readable
- [ ] No personal information visible (emails, API keys, etc.)
- [ ] Title screen shows project name and your name
- [ ] End screen has contact info
- [ ] Video length: 5-10 minutes (check requirement)
- [ ] File uploaded and link works
- [ ] Link added to hackathon submission form

---

## Example Timeline (8-Minute Video)

| Section | Duration | Start | End |
|---------|----------|-------|-----|
| Opening | 0:30 | 0:00 | 0:30 |
| System Overview | 1:00 | 0:30 | 1:30 |
| Email Demo | 2:30 | 1:30 | 4:00 |
| LinkedIn Demo | 2:30 | 4:00 | 6:30 |
| Safety System | 0:45 | 6:30 | 7:15 |
| Results & Stats | 0:45 | 7:15 | 8:00 |
| Closing | 0:30 | 8:00 | 8:30 |
| **TOTAL** | **8:30** | | |

---

## Pro Tips

1. **Show, Don't Tell:** Visuals are more powerful than narration
2. **Keep Mouse Slow:** Fast mouse movements are hard to follow
3. **Highlight Text:** Use cursor to guide viewer's eye
4. **Pause on Important Screens:** Let viewers read for 2-3 seconds
5. **Use Zooms Sparingly:** Only for small/important text
6. **Test on Mobile:** Many judges might watch on phones
7. **Subtitle Optional:** Helps accessibility but takes time
8. **Energy in Voice:** Sound enthusiastic (but not over-the-top)

---

## What NOT to Show

- ❌ Long loading times (edit them out)
- ❌ Errors or broken features (unless showing error handling)
- ❌ Irrelevant files or applications
- ❌ Personal emails or sensitive data
- ❌ Long code sections (show structure, not every line)
- ❌ You fumbling with files (edit out mistakes)

---

## Backup Plan

If demo video is taking too long, submit with:
- Detailed written documentation (you already have this ✓)
- Screenshots showing key features
- Promise to add video within X days

**But video is highly recommended - it's much more impressive than docs alone.**

---

*Good luck with your demo! Remember: The system works, you just need to show it clearly.* 🎥
