# 🏗️ Bigin Pipeline & Sub-pipeline Architecture

This document details the architectural hierarchy, entity relationships, constraints, and configuration mechanisms for Zoho Bigin Team Pipelines and Sub-pipelines.

---

## 1. Architectural Hierarchy

```
Zoho Bigin Organization
└── Team Pipelines (Dedicated operational silos: Sales, Onboarding, Support, Procurement)
    ├── Permissions & Role Access (Admins, Standard Users, Custom Profiles)
    ├── Custom Fields & Layouts (Fields unique to this Team Pipeline)
    └── Sub-pipelines (Specific tracks, e.g., "Enterprise Sales", "Self-Serve", "Partner Deals")
        └── Stages (Max 25 per Sub-pipeline)
            ├── Display Name (e.g., "Qualification", "Proposal Sent", "Contract Signed")
            ├── Probability % (0% to 100%)
            ├── Classification Category:
            │   ├── Open (In-flight records)
            │   ├── Closed Won (Successfully converted)
            │   └── Closed Lost (Disqualified / abandoned)
            └── Stage Transition Rules & Required Fields
```

---

## 2. Entity Relationships & Technical Schema

### Sub-pipeline Record Mapping
Every deal or operational card created in Bigin belongs to a specific Team Pipeline and Sub-pipeline:

```json
{
  "Deal_Name": "Acme Global Rollout",
  "Amount": 45000.00,
  "Pipeline": "Enterprise Sales Pipeline",
  "Sub_Pipeline": "Direct Enterprise",
  "Stage": "Proposal / Quote",
  "Closing_Date": "2026-11-30",
  "Contact_Name": {
    "id": "481000000123456"
  },
  "Account_Name": {
    "id": "481000000123789"
  }
}
```

### Stage Classification Rules
When designing pipeline stages, enforce strict semantic mapping:
- **`Open` Stages**: Must have probability between $10\%$ and $90\%$. Used for active operational tracking.
- **`Closed Won` Stages**: Must have probability $100\%$. Triggers downstream financial fulfillment (e.g., generating Zoho Books invoices or receipts).
- **`Closed Lost` Stages**: Must have probability $0\%$. Requires a mandatory `Lost Reason` picklist (e.g., "Budget Constraints", "Competitor Selected", "Feature Gap").

---

## 3. Plan Restrictions & Capacity Limits

Before proposing a new pipeline configuration, verify that the organization does not exceed its subscription ceiling:

| Feature / Limit | Free Tier | Express Tier | Premier Tier | Bigin 360 Tier |
| :--- | :--- | :--- | :--- | :--- |
| **Team Pipelines** | 1 (Fixed) | 3 | 5 | 15 (4 default included) |
| **Additional Team Pipelines** | Not available | $5/month add-on | $5/month add-on | Included / add-on |
| **Sub-pipelines** | 1 | 15 | 25 | 75 |
| **Stages per Sub-pipeline** | Max 25 | Max 25 | Max 25 | Max 25 |
| **Custom Fields per Pipeline** | 5 | 10 | 25 | 50 |
| **Total Record Limit** | 500 records | 50,000 records | 100,000 records | 500,000 records |
| **Workflow Rules per Module**| 3 | 10 | 30 | 50 |

---

## 4. Pipeline Design Specification Standard (JSON)

When an AI agent designs a pipeline, it must generate this standardized JSON schema for human review before initiating browser execution:

```json
{
  "$schema": "https://agentskills.io/schemas/bigin-pipeline.json",
  "team_pipeline": {
    "name": "Customer Onboarding & Delivery",
    "description": "Post-sales delivery, customer technical setup, and kickoff",
    "access_roles": ["Administrator", "Standard"],
    "sub_pipelines": [
      {
        "name": "Enterprise Setup",
        "default": true,
        "stages": [
          {
            "name": "Kickoff Scheduled",
            "probability": 20,
            "category": "Open",
            "mandatory_fields_on_entry": ["Kickoff_Date", "Technical_Lead"]
          },
          {
            "name": "Integration & Provisioning",
            "probability": 50,
            "category": "Open",
            "mandatory_fields_on_entry": ["API_Access_Granted"]
          },
          {
            "name": "UAT & Client Sign-off",
            "probability": 80,
            "category": "Open",
            "mandatory_fields_on_entry": ["Sign_off_Document_URL"]
          },
          {
            "name": "Live in Production",
            "probability": 100,
            "category": "Closed Won",
            "mandatory_fields_on_entry": ["Go_Live_Date"]
          },
          {
            "name": "Implementation Cancelled",
            "probability": 0,
            "category": "Closed Lost",
            "mandatory_fields_on_entry": ["Cancellation_Reason"]
          }
        ]
      }
    ],
    "custom_fields": [
      {
        "label": "Technical Lead",
        "type": "lookup",
        "target_module": "Users",
        "required": true
      },
      {
        "label": "Go Live Date",
        "type": "date",
        "required": false
      }
    ]
  }
}
```

---

## 5. UI Automation Selectors & Targets

For browser automation tools (Playwright / Browser Use), target these stable UI anchors in Zoho Bigin:

1. **Navigation to Pipelines**:
   - URL: `https://bigin.zoho.com/#/settings/pipelines`
   - Settings Gear: `button[data-id="settings-icon"]`, `a[href*="settings"]`
   - Pipelines Submenu: `a[data-zcqa="pipelines_settings"]`, text: `"Pipelines"`
2. **Team Pipeline Creation**:
   - Add Pipeline Button: `button:has-text("New Team Pipeline")`, `button[data-zcqa="add_team_pipeline"]`
   - Pipeline Name Input: `input[name="pipeline_name"]`, `input[placeholder="Enter pipeline name"]`
3. **Stage Management Table**:
   - Add Stage Button: `button:has-text("Add Stage")`, `span.add-stage-btn`
   - Stage Name Input: `input.stage-name-input`
   - Category Dropdown: `select[name="stage_type"]`, option values: `open`, `won`, `lost`
   - Probability Input: `input[name="probability"]`
4. **Save & Commit**:
   - Save Button: `button[type="submit"]:has-text("Save")`, `button.primary-btn:has-text("Save")`
   - Confirmation Toast: `.toast-success`, `div[role="alert"]:has-text("Saved successfully")`
