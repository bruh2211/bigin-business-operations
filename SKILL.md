---
name: bigin-business-operations
description: >-
  Architects, configures, and automates Zoho Bigin as a central CRM and business operations platform.
  Designs Team Pipelines, sub-pipelines, stages, field layouts, and automations. Orchestrates Zoho Books
  financial workflows (invoices, verified receipts), Zoho People HR sync, Google Workspace document ingestion,
  and WhatsApp customer communications. Executes configuration changes via verified browser automation (Playwright/Browser Use)
  and REST APIs with strict financial safeguards and human approval gates. Use when asked to configure Bigin pipelines,
  automate CRM operations, manage Zoho Books invoices/receipts, sync Zoho People, ingest business documents, or audit CRM configuration.
compatibility: Requires Python 3.10+ or Node.js 18+, Playwright or browser-use, Zoho OAuth credentials
metadata:
  version: "1.0.0"
  standard: "agentskills.io"
  systems: "Google Antigravity 2.0 & Claude Code"
---

# 🏢 Zoho Bigin Business Operations Skill (`bigin-business-operations`)

Universal AI agent operating system for **Zoho Bigin CRM**, **Zoho Books**, **Zoho People**, **Google Workspace**, and **WhatsApp Business Operations**.

This skill enables AI coding agents (in both Antigravity 2.0 and Claude Code) to understand, design, configure, audit, and orchestrate Bigin CRM architecture and connected cross-application business workflows.

---

## ⚡ Core Operational Principles

1. **Evidence-Based Execution Mode**:
   - **CRM Structure Configuration** (New Team Pipelines, Sub-pipelines, Custom Stages, Layouts): **UI ONLY**. Executed via deterministic Playwright browser automation or Browser Use. Public REST API does *not* support creating pipeline definitions.
   - **CRM Records & Deals**: Supported via **Bigin REST API v2** (`/bigin/v2/{module}`).
   - **Financial Invoicing & Payment**: Supported via **Zoho Books API v3**.
   - **HR & Employee Sync**: Managed via **Zoho Flow** or **Zoho People API v2** (No native Bigin toggle exists).
   - **Customer Messaging**: Managed via **Bigin WhatsApp Topping** (Cloud API / Twilio) and Email-In.
2. **Financial Safeguard Invariant**:
   - ⚠️ **An invoice is NEVER proof of payment**.
   - A payment receipt is generated **ONLY** after querying the financial system (`GET /api/v3/customerpayments/{id}`) and verifying that the transaction status is cleared and reconciled.
   - Every invoice, estimate, refund, or receipt requires explicit human approval before creation or transmission.
3. **Configuration Safety & Pre-flight Inspection**:
   - Always inspect and snapshot existing configuration before proposing or executing structural changes.
   - Validate proposed pipelines against Zoho subscription limits (Free, Express, Premier, Bigin 360).
   - Never mutate production pipelines without human approval and an exportable rollback definition.

---

## 🧭 Navigation & Progressive Disclosure

Read reference manuals and workflows on-demand to save context:

- **Capability & Architecture Specs**:
  - [Bigin Capabilities & Truth Matrix](./references/bigin-capabilities.md)
  - [Pipelines & Sub-pipelines Architecture](./references/pipelines-and-subpipelines.md)
  - [Workflow Automation & Trigger Engine](./references/workflow-automation.md)
  - [REST API Reference & Endpoints](./references/api-reference.md)
  - [Zoho & Custom MCP Tool Schemas](./references/mcp-tools.md)
  - [Subscription Limits & Edition Constraints](./references/subscription-limits.md)
  - [UI Visual Guide & Screen Wireframes](./references/ui-visual-guide.md)
  - [Business Process Flow Logic Engine](./references/flow-logic-engine.md)
  - [Security, OAuth & Approval Gates](./references/security-and-approvals.md)
- **Integration Handbooks**:
  - [Zoho Books Financial Workflows](./references/zoho-books.md)
  - [Zoho People HR Integration](./references/zoho-people.md)
  - [Email & WhatsApp Business Operations](./references/email-and-whatsapp.md)
  - [Google Workspace & Document Ingestion](./references/google-workspace.md)
- **Step-by-Step Workflows**:
  - [Interactive Guided Builder (Interview & Instructions)](./workflows/interactive-guided-builder.md)
  - [Pipeline Configuration Workflow](./workflows/pipeline-configuration.md)
  - [Invoice & Verified Payment Receipt Workflow](./workflows/invoice-and-receipt.md)
  - [Document Ingestion to CRM Pipeline](./workflows/document-ingestion.md)
  - [Cross-Application Sales-to-Payment Orchestration](./workflows/cross-application-orchestration.md)
- **Browser Automation Strategy & Procedures**:
  - [Browser Use Evaluation & Setup](./browser-automation/browser-use.md)
  - [Playwright Architecture & Deterministic Selectors](./browser-automation/playwright.md)
  - [Verified Browser Execution Scripts](./browser-automation/verified-procedures/pipeline_manager.py)
- **Execution & Validation Tools**:
  - [Pipeline Spec Validator](./scripts/configuration-tools/pipeline_validator.py)
  - [Financial Guard & Anti-Duplicate Verifier](./scripts/configuration-tools/financial_guard.py)
  - [Bigin REST API Client](./scripts/configuration-tools/bigin_api_client.py)
- **Test Suites & Audits**:
  - [Capability Verification Tests](./tests/capability-tests.md)
  - [Configuration Validation Tests](./tests/configuration-validation.md)
  - [End-to-End Integration Tests](./tests/integration-tests.md)

---

## 🛠️ Procedural Execution Rules

When executing any task under this skill, follow this 4-step loop:

### Step 1: Pre-flight Audit & Inspection
- Check current Bigin edition (`Free`, `Express`, `Premier`, `Bigin 360`) and quota usage using `python scripts/configuration-tools/pipeline_validator.py --check-limits`.
- Query current pipeline metadata using `python scripts/configuration-tools/bigin_api_client.py get_layouts`.

### Step 2: Architecture Proposal & Approval Gate
- Generate the proposed Pipeline/Workflow architecture JSON/YAML.
- Present the diff to the user showing added stages, stage classifications (Open, Won, Lost), mandatory fields, and transitions.
- **WAIT** for explicit user confirmation before applying structural changes.

### Step 3: Execution via the Appropriate Channel
- If creating/editing **Pipelines, Sub-pipelines, or Stages**:
  - Run the deterministic Playwright script:
    `python browser-automation/verified-procedures/pipeline_manager.py --action create_pipeline --config proposed_pipeline.json`
- If creating/updating **Deals, Contacts, or Notes**:
  - Use `python scripts/configuration-tools/bigin_api_client.py create_record ...` or MCP tool `bigin_create_record`.
- If creating **Invoices or Receipts**:
  - Validate invoice items and tax calculations with `python scripts/configuration-tools/financial_guard.py`.

### Step 4: Verification & State Assertion
- Re-inspect Bigin UI / API to verify that the newly created pipeline or record exists.
- Return an evidence-backed verification log with timestamps, record IDs, and URL references.
