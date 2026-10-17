# 🔒 Security, Reliability & Governance Reference

This reference establishes security standards, credential management protocols, audit logging requirements, and human-in-the-loop approval gates.

---

## 1. Mandatory Human Approval Gates

The AI agent must request explicit human approval before executing any of the following operations:

1. **Structural CRM Changes**:
   - Creating a new Team Pipeline or Sub-pipeline.
   - Deleting, renaming, or reordering existing stages.
   - Adding or modifying custom fields in production layouts.
2. **Financial Operations**:
   - Creating or transmitting an Invoice or Quotation to a client.
   - Issuing a Credit Note or Refund.
   - Marking any invoice as written-off or cancelled.
3. **External Communications**:
   - Sending broadcast or automated WhatsApp messages to customer lists.
   - Sending contract sign-off requests.

---

## 2. Credential Security & Environment Variables

- Never hardcode API keys, client secrets, or OAuth refresh tokens in code, configs, or logs.
- All credentials must be sourced from environment variables:
  - `ZOHO_CLIENT_ID`
  - `ZOHO_CLIENT_SECRET`
  - `ZOHO_REFRESH_TOKEN`
  - `ZOHO_ORG_ID` (for Books)
  - `GOOGLE_SERVICE_ACCOUNT_KEY`
- Browser sessions must store cookies and session state in an encrypted local storage directory or ephemeral container.

---

## 3. Idempotency & Audit Logging

Every agent-driven operation must generate an execution log entry:

```json
{
  "timestamp": "2026-10-17T05:58:00Z",
  "operation": "CREATE_TEAM_PIPELINE",
  "execution_method": "PLAYWRIGHT_BROWSER_AUTOMATION",
  "target": "Customer Onboarding & Delivery",
  "status": "SUCCESS",
  "pre_flight_check": "PASSED (Remaining pipelines: 2/5)",
  "approval_obtained": true,
  "artifacts": {
    "screenshot_path": "logs/screenshots/pipeline_created_20261017.png",
    "dom_verification": "DOM element div[data-pipeline-id] found"
  }
}
```
