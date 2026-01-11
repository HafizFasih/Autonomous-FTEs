### **The Silver Tier Branching Strategy**

You will complete these branches **sequentially** (one after the other).

#### **Branch 1: The Foundation (Phase 1)**

* **Branch Name:** `feat/silver-core-workflows`
* **Standard Title:** "feat: Implement Approval System and Planning capabilities"
* **What goes in here:**
* Creating folders: `/Pending_Approval`, `/Approved`, `/Rejected`.
* Creating file: `Business_Goals.md`.
* **Skill:** `handle-approval` (The critical dependency).
* **Skill:** `create-plan` (Since it relies on the handbook/handover).


* **Why:** This creates the "Safety Layer" required before we let the AI send emails.

#### **Branch 2: The Communication System (Phase 2)**

* **Branch Name:** `feat/email-system`
* **Standard Title:** "feat: Add Gmail Watcher and Email Processing Skills"
* **Dependencies:** Must be branched **after** Branch 1 is merged.
* **What goes in here:**
* **Script:** `gmail_watcher.py`.
* **Config:** Email MCP Server setup.
* **Skill:** `process-emails` (with its 3 parts: metadata, body, templates).


* **Why:** This is a complete vertical slice: "See Email -> Draft Reply -> Request Approval".

#### **Branch 3: The Social System (Phase 3)**

* **Branch Name:** `feat/linkedin-automation`
* **Standard Title:** "feat: Implement LinkedIn Publishing Workflow"
* **What goes in here:**
* **Config:** LinkedIn API/MCP integration.
* **Skill:** `post-to-linkedin`.
* **Refinement:** Updating `Company_Handbook.md` with social media rules.


* **Why:** This is the riskiest feature, so it goes last, isolated in its own branch.
