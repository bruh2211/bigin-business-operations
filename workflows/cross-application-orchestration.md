# 📋 Workflow: Cross-Application Orchestration (Sales-to-Payment)

This runbook defines the multi-application operational chain connecting Zoho Bigin, Zoho Books, Google Workspace, WhatsApp, and Zoho People.

---

## 🔄 End-to-End Sales-to-Payment Cycle

```
Bigin Deal Reaches "Proposal Accepted"
    │
    ▼
Step 1: Financial Invoicing (Zoho Books)
    ├── Generate draft invoice with line items & tax rules
    ├── Embed Bigin Deal ID as reference_number
    └── Request human approval before transmission
    │
    ▼
Step 2: Client Notification (WhatsApp / Email)
    ├── Dispatch approved invoice link via WhatsApp Cloud API / Email
    └── Log message dispatch timestamp in Bigin Deal Notes
    │
    ▼
Step 3: Payment Verification & Invariant Check (Zoho Books)
    ├── Poll / listen for payment webhook
    ├── Query GET /api/v3/customerpayments/{id}
    └── Verify: status == "success" AND amount == invoice_total
    │
    ▼
Step 4: Payment Receipt Delivery & CRM Transition
    ├── Download official payment receipt PDF from Zoho Books
    ├── Send receipt to customer
    └── Transition Bigin Deal to "Closed Won / Paid"
    │
    ▼
Step 5: Operational Kickoff & Employee Allocation (Zoho People / Drive)
    ├── Trigger Zoho People / Flow task assignment for technical team
    └── Provision project folder in Google Drive with template files
```
