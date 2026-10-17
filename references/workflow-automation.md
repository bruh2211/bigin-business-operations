# ⚡ Workflow Automation & Trigger Engine

This document details Bigin's native workflow capabilities, trigger types, actions, integration webhooks, and orchestration patterns.

---

## 1. Native Workflow Architecture

In Zoho Bigin, automated workflows listen to record events and execute immediate or scheduled actions:

```
Trigger Event (Record Creation, Edit, Stage Transition, Field Change, Date/Time)
    │
    ▼
Criteria / Condition Evaluation (e.g., Amount > $10,000 AND Region == 'EMEA')
    │
    ├── True ──► Immediate Actions
    │             ├── Field Updates (e.g., Lead Status -> Contacted)
    │             ├── Email Notifications (Using pre-approved templates)
    │             ├── Task & Activity Assignment (Task for Account Owner)
    │             └── Outbound Webhooks (Notify external microservices)
    │
    └── False ─► Scheduled Actions / Fallback Branch
```

---

## 2. Trigger Types & Scenarios

| Trigger Type | When It Fires | Ideal Use Case |
| :--- | :--- | :--- |
| **On Record Creation** | When a new Deal, Contact, or Company is created. | Auto-assigning lead owner; sending welcome email sequence. |
| **On Edit / Field Update** | When a specific field changes (e.g., Stage changes to "Closed Won"). | Triggering financial document creation; notifying operations team. |
| **On Stage Transition** | Specifically when a deal is dragged or updated to a new stage. | Sending contract documents; creating onboarding checklist. |
| **Date/Time Trigger** | Relative to a date field (e.g., 3 days before `Closing_Date`). | Automated follow-up reminder; contract expiration warning. |

---

## 3. Webhooks & Custom Functions

Webhooks allow Bigin to communicate with external agents, backend servers, or Zoho Flow:

### Outbound Webhook Specification
When Bigin fires a webhook on a stage transition (e.g., deal marked `Closed Won`), the payload typically provides:

```json
{
  "event": "stage_update",
  "module": "Pipelines",
  "record_id": "481000000184712",
  "deal_name": "Globex Annual Subscription",
  "pipeline_name": "SaaS Sales Pipeline",
  "sub_pipeline": "Direct Sales",
  "stage": "Closed Won",
  "amount": 12000.00,
  "closing_date": "2026-10-17",
  "contact": {
    "name": "Jane Doe",
    "email": "jane@globex.com",
    "phone": "+14155552671"
  },
  "company": {
    "name": "Globex Corp",
    "id": "481000000184001"
  }
}
```

---

## 4. Automation Quotas & Subscription Constraints

| Limit Dimension | Free Tier | Express Tier | Premier Tier | Bigin 360 Tier |
| :--- | :--- | :--- | :--- | :--- |
| **Workflow Rules per Module** | 3 | 10 | 30 | 50 |
| **Email Notifications / Day** | 50 | 500 | 1,000 | 2,500 |
| **Webhooks per Day** | 0 (Unsupported) | 1,000 calls | 5,000 calls | 10,000 calls |
| **Scheduled Workflows** | Not available | Supported (Daily) | Supported (Hourly) | Supported |

---

## 5. Duplicate Prevention & Idempotency Rules

When setting up cross-application automations (e.g., Bigin triggering Zoho Books invoices):
1. **Idempotency Key Tagging**: Always write the originating `Bigin_Record_ID` into the target system's reference field (e.g., `reference_number` in Zoho Books).
2. **Pre-check Existence**: Before creating an invoice or external task, query the external system for existing records containing `reference_number == Bigin_Record_ID`.
3. **Locking Mechanism**: When an event triggers an asynchronous background workflow, immediately update a custom Bigin field `Workflow_Status = "IN_PROGRESS"` to prevent concurrent duplicate invocations.
