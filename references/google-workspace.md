# 📁 Google Workspace & Document Ingestion Reference

This document outlines the architecture for ingesting business documents from Google Drive, extracting structured operational data, and safely writing to Bigin CRM.

---

## 1. Document Ingestion Pipeline

```
Business Document Arrives (Google Drive Folder: /Contracts/Incoming)
    │
    ▼
File Fetch & Format Conversion (PDF, Google Doc, XLSX)
    │
    ▼
Information Extraction Engine (OCR / LLM Structured Extraction)
    ├── Customer Organization & Signatory Name
    ├── Project Scope / Deliverables
    ├── Commercial Terms (Contract Value, Currency, Milestone Dates)
    └── Compliance / Expiration Dates
    │
    ▼
Validation & Anomaly Check (Currency validity, Amount > 0, Dates in future)
    │
    ▼
Human Approval Gate (Display extracted diff for user confirmation)
    │
    ▼
Record Upsert in Zoho Bigin (Deals, Contacts, Notes, Attached Drive URL)
```

---

## 2. Extraction Schema Specification

When extracting data from documents, the agent must conform to this schema before submitting for human approval:

```json
{
  "source_document": {
    "file_id": "1A2B3C4D5E6F7G8H9I0",
    "filename": "SOW_Globex_Cloud_Migration_2026.pdf",
    "drive_link": "https://drive.google.com/file/d/1A2B3C4D5E6F7G8H9I0/view"
  },
  "extracted_data": {
    "company_name": "Globex Corporation",
    "signatory_name": "Alice Smith",
    "signatory_email": "alice@globex.com",
    "project_name": "Cloud Infrastructure Migration",
    "total_value": 85000.00,
    "currency": "USD",
    "target_start_date": "2026-11-01",
    "target_completion_date": "2027-04-30",
    "payment_milestones": [
      { "milestone": "Kickoff", "percentage": 30, "amount": 25500.00 },
      { "milestone": "Phase 1 Delivery", "percentage": 40, "amount": 34000.00 },
      { "milestone": "Final Acceptance", "percentage": 30, "amount": 25500.00 }
    ]
  },
  "validation_status": "VALID",
  "missing_fields": []
}
```

---

## 3. Google Workspace OAuth Scopes

- Google Drive Read: `https://www.googleapis.com/auth/drive.readonly`
- Google Sheets Read/Write: `https://www.googleapis.com/auth/spreadsheets`
- Gmail Send (for approved alerts): `https://www.googleapis.com/auth/gmail.send`
