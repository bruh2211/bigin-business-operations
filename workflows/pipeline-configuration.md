# 📋 Workflow: Bigin Pipeline Architecture & Configuration

This guide provides the operational runbook for designing, proposing, executing, and verifying Team Pipeline and sub-pipeline configurations in Zoho Bigin.

---

## Step 1: Pre-flight Audit
1. Run inspection command to read current organization structure and remaining quotas:
   ```bash
   python scripts/configuration-tools/pipeline_validator.py --check-limits
   ```
2. Verify that:
   - Organization has not reached its Team Pipeline limit.
   - Proposed sub-pipeline stage count is $\le 25$.
   - Proposed custom field count conforms to the plan tier.

---

## Step 2: Architecture Proposal Specification
1. Draft the pipeline specification in JSON (e.g. `proposed_pipeline.json`).
2. Run validation against schema:
   ```bash
   python scripts/configuration-tools/pipeline_validator.py --validate proposed_pipeline.json
   ```
3. Present the proposal clearly to the user, highlighting:
   - Pipeline Name & Description
   - Sub-pipeline names & stage names
   - Stage classifications (Open, Won, Lost)
   - Mandatory fields upon stage transition
4. **Obtain explicit user confirmation to proceed.**

---

## Step 3: Browser Automation Execution
1. Launch the verified Playwright automation procedure:
   ```bash
   python browser-automation/verified-procedures/pipeline_manager.py --action create_pipeline --config proposed_pipeline.json
   ```
2. The automation will:
   - Open Bigin Settings > Pipelines.
   - Click "New Team Pipeline".
   - Enter pipeline name and configure permissions.
   - Create the sub-pipeline and iteratively configure each stage, probability, and category.
   - Capture DOM snapshots and screenshots for audit verification.

---

## Step 4: Verification & Handover
1. Query Bigin UI or layout metadata to verify that the new pipeline is visible and operational.
2. Produce an execution report with the verified pipeline ID and snapshot URLs.
