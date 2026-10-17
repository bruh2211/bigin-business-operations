# 🛠️ Zoho Bigin & Connected Services MCP Tools Reference

This document defines the Model Context Protocol (MCP) tool schemas for Zoho Bigin, Zoho Books, Google Workspace, and custom browser-automation tools.

---

## 1. Bigin MCP Tool Schemas

These tools allow the AI agent to inspect CRM metadata and manage pipeline records through standardized MCP interfaces.

### `bigin_get_layouts`
Retrieves pipeline layout metadata, active sub-pipelines, sections, and fields.
```json
{
  "name": "bigin_get_layouts",
  "description": "Fetches metadata for all layouts, pipelines, and sub-pipelines in Zoho Bigin.",
  "parameters": {
    "type": "object",
    "properties": {
      "module": {
        "type": "string",
        "description": "Module API name (e.g. 'Pipelines', 'Contacts', 'Accounts').",
        "default": "Pipelines"
      }
    },
    "required": ["module"]
  }
}
```

### `bigin_create_record`
Creates a new record (e.g. Deal, Contact, Task) in Bigin.
```json
{
  "name": "bigin_create_record",
  "description": "Creates a new record within a Bigin module and pipeline.",
  "parameters": {
    "type": "object",
    "properties": {
      "module": {
        "type": "string",
        "description": "Module API name ('Pipelines', 'Contacts', 'Accounts', etc.)."
      },
      "data": {
        "type": "object",
        "description": "Key-value attributes matching the Bigin field API names."
      }
    },
    "required": ["module", "data"]
  }
}
```

### `bigin_update_record`
Updates an existing record (e.g., transition stage or update fields).
```json
{
  "name": "bigin_update_record",
  "description": "Updates an existing record in Bigin by ID.",
  "parameters": {
    "type": "object",
    "properties": {
      "module": {
        "type": "string",
        "description": "Module API name ('Pipelines', 'Contacts', etc.)."
      },
      "record_id": {
        "type": "string",
        "description": "Unique Bigin record ID."
      },
      "data": {
        "type": "object",
        "description": "Fields to update."
      }
    },
    "required": ["module", "record_id", "data"]
  }
}
```

---

## 2. Browser Automation MCP Tools (UI Operations)

Because Bigin's REST API does not support programmatic creation of Team Pipelines and custom stages, the following browser-automation tools are exposed:

### `bigin_inspect_ui_configuration`
Navigates to the Bigin Settings UI using Playwright/Browser Use, extracts the live Team Pipelines, sub-pipelines, stages, and remaining quotas.
```json
{
  "name": "bigin_inspect_ui_configuration",
  "description": "Extracts current Team Pipeline structure and available slots directly from the Bigin settings UI.",
  "parameters": {
    "type": "object",
    "properties": {
      "session_auth_token": {
        "type": "string",
        "description": "Optional active session cookie/storage token."
      }
    }
  }
}
```

### `bigin_create_team_pipeline_ui`
Automates the creation of a new Team Pipeline and its nested sub-pipeline/stages via browser execution.
```json
{
  "name": "bigin_create_team_pipeline_ui",
  "description": "Executes Playwright browser automation to create a verified Team Pipeline, sub-pipeline, and stages in Bigin.",
  "parameters": {
    "type": "object",
    "properties": {
      "pipeline_spec": {
        "type": "object",
        "description": "Validated pipeline specification JSON containing name, sub_pipelines, and stages."
      },
      "dry_run": {
        "type": "boolean",
        "description": "If true, navigates to UI and validates forms without committing.",
        "default": false
      }
    },
    "required": ["pipeline_spec"]
  }
}
```

---

## 3. Zoho Books Financial MCP Tools

### `zoho_books_create_invoice`
Generates a draft or sent invoice in Zoho Books with line items and taxes.
```json
{
  "name": "zoho_books_create_invoice",
  "description": "Creates an invoice in Zoho Books tied to a Bigin deal reference.",
  "parameters": {
    "type": "object",
    "properties": {
      "customer_id": { "type": "string" },
      "reference_number": { "type": "string", "description": "Bigin Deal ID for anti-duplication" },
      "line_items": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "item_id": { "type": "string" },
            "rate": { "type": "number" },
            "quantity": { "type": "number" }
          },
          "required": ["rate", "quantity"]
        }
      }
    },
    "required": ["customer_id", "reference_number", "line_items"]
  }
}
```

### `zoho_books_verify_payment`
Verifies whether a customer payment has actually been recorded, cleared, and reconciled.
```json
{
  "name": "zoho_books_verify_payment",
  "description": "Queries Zoho Books for verified customer payment records matching an invoice or deal.",
  "parameters": {
    "type": "object",
    "properties": {
      "invoice_id": { "type": "string" }
    },
    "required": ["invoice_id"]
  }
}
```
