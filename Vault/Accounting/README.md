# Accounting Folder Structure

This folder contains all financial records synced from Xero.

**Last Updated:** 2026-01-11

---

## Folder Structure

```
Accounting/
├── Current_Month.md           # Summary of current month's transactions
├── Transactions/              # Individual transaction files
│   └── TRANS_YYYY-MM-DD_[Description].md
├── Invoices/                  # Invoice copies
│   └── INV_[Number]_[Client].pdf
├── Expenses/                  # Expense receipts and details
└── Recommendations/           # Cost optimization suggestions
```

---

## Files

### Current_Month.md
- **Purpose:** Real-time summary of revenue, expenses, and cash flow
- **Updated:** After each `xero_sync.py` run
- **Used by:** Dashboard, CEO briefing

### Transactions/
- **Purpose:** Individual transaction records synced from Xero
- **Filename Format:** `TRANS_YYYY-MM-DD_[Description].md`
- **Contains:** Transaction details, categorization, reconciliation status
- **Created by:** `xero_sync.py`

### Invoices/
- **Purpose:** Copies of invoices created in Xero
- **Filename Format:** `INV_[Number]_[Client].pdf`
- **Created by:** `generate_invoice.py` (after approval)

### Expenses/
- **Purpose:** Expense receipts and categorization details
- **Created by:** Manual upload or expense categorization

### Recommendations/
- **Purpose:** Cost optimization and subscription audit recommendations
- **Created by:** `manage-accounting` skill during financial analysis

---

## Workflow

1. **Daily Sync (6:00 AM):**
   - `xero_sync.py` fetches new transactions from Xero
   - Updates `Current_Month.md`
   - Creates transaction files in `Transactions/`

2. **Auto-Categorization:**
   - `categorize_expense.py` categorizes uncategorized expenses
   - Updates transaction files with category info
   - Flags uncertain transactions for review

3. **Invoice Creation:**
   - `generate_invoice.py` creates approval request
   - After approval, invoice created in Xero
   - Copy saved to `Invoices/`

4. **Weekly Reconciliation:**
   - Match transactions to invoices/bills
   - Identify discrepancies
   - Update reconciliation status

5. **CEO Briefing (Sunday):**
   - Aggregates financial data
   - Generates cost optimization recommendations
   - Feeds into weekly business audit

---

## Usage

### Sync Transactions
```bash
python .claude/skills/manage-accounting/scripts/xero_sync.py
```

### Categorize Expenses
```bash
python .claude/skills/manage-accounting/scripts/categorize_expense.py
```

### Create Invoice
```bash
python .claude/skills/manage-accounting/scripts/generate_invoice.py \
  --client "Client Name" \
  --amount 1500 \
  --description "Services rendered"
```

---

## Integration

**Used by:**
- `generate-ceo-briefing` skill (financial summary)
- `Dashboard.md` (real-time financial status)
- `monitor-system` skill (tracks sync health)

**Requires:**
- Xero MCP server configured and running
- `handle-approval` skill (for invoice approvals)

---

*For detailed documentation, see:*
- `.claude/skills/manage-accounting/SKILL.md`
- `.claude/skills/manage-accounting/reference/`
