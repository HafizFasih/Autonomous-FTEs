# Autonomous FTE - Bronze Tier Achievement

This project implements a Personal AI Employee system using Claude Code and Obsidian as part of Hackathon 0.

## Project Status: ✅ Bronze Tier Complete

### Requirements Met

1. **✅ Obsidian Vault with Core Files**
   - `Dashboard.md` - Activity logging with timestamps
   - `Company_Handbook.md` - AI behavior rules

2. **✅ Basic Folder Structure**
   - `/Inbox` - Drop zone for new files
   - `/Needs_Action` - Tasks awaiting processing
   - `/Done` - Completed tasks

3. **✅ Working File System Watcher**
   - `filesystem_watcher.py` - Monitors Inbox folder
   - Automatically creates metadata files in Needs_Action
   - Uses Python watchdog library

4. **✅ Claude Code Integration**
   - Successfully reads from vault
   - Successfully writes to vault
   - Processes tasks and moves files
   - Updates Dashboard with activity logs

5. **✅ Agent Skills Implementation**
   - `.claude/skills/process-tasks/SKILL.md` - Task processing skill
   - Automates the complete workflow

## How to Use

### 1. Start the File Watcher
```bash
python filesystem_watcher.py
```

### 2. Drop a Task
Place a file in the `Inbox/` folder with your task request.

### 3. Process Tasks
In Claude Code, run:
```
/process-tasks
```

Claude will automatically:
- Read all files in Needs_Action
- Complete the requested tasks
- Move files to Done
- Update Dashboard with logs

## Architecture

```
Inbox/ → Watcher detects → Needs_Action/ → Claude processes → Done/
                                                    ↓
                                            Dashboard.md updated
```

## Tech Stack
- **Brain**: Claude Code
- **Memory**: Obsidian (Markdown files)
- **Watcher**: Python + watchdog library
- **Automation**: Agent Skills

## Next Steps (Silver Tier)
- Add Gmail Watcher
- Add WhatsApp Watcher
- Implement MCP servers for external actions
- Add human-in-the-loop approval workflow
- Set up scheduling (cron/Task Scheduler)
