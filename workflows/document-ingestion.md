# 📋 Workflow: Google Workspace Document Ingestion to CRM

This runbook guides the agent through fetching business documents from Google Drive, extracting key entities, and writing verified records to Zoho Bigin.

---

## Step 1: Detect Document & Read Content
1. Detect new or updated file in Google Drive watched folder.
2. Download file or export Google Doc to text / PDF.
3. Parse text content using OCR or text extractor.

---

## Step 2: Information Extraction & Schema Validation
Extract key business entities into standard JSON:
- Company Name
- Signatory Name & Email
- Contract / Project Scope
- Financial Terms (Amount, Currency, Milestones)
- Deliverables & Completion Dates

Validate that required fields exist and values are non-zero.

---

## Step 3: Human Verification & Diff Review
Present the extracted proposal to the user:
```markdown
### Extracted Document Proposal
- **Source**: SOW_Globex_Cloud_Migration.pdf
- **Customer**: Globex Corporation
- **Signatory**: Alice Smith (alice@globex.com)
- **Project Value**: $85,000 USD
- **Target Pipeline**: Customer Onboarding -> Enterprise Setup
```
Request confirmation before creating records in Bigin CRM.

---

## Step 4: Write to Bigin CRM & Attach Source Reference
Upon user approval:
1. Search if Company/Contact exists in Bigin. If not, create them.
2. Create Deal record in target Team Pipeline and Sub-pipeline.
3. Attach Google Drive file URL in deal notes for full traceability.
