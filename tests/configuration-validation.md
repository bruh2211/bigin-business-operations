# 🧪 Configuration Validation Test Plan

Validates pipeline JSON specifications against schema invariants, plan limits, stage rules, and classification logic.

---

## Test Cases

### TC-VAL-01: Valid Premier Pipeline Specification
- **Input**:
  ```json
  {
    "team_pipeline": {
      "name": "Customer Onboarding",
      "sub_pipelines": [
        {
          "name": "Standard",
          "stages": [
            { "name": "Kickoff", "probability": 20, "category": "Open" },
            { "name": "Completed", "probability": 100, "category": "Closed Won" },
            { "name": "Aborted", "probability": 0, "category": "Closed Lost" }
          ]
        }
      ]
    }
  }
  ```
- **Execution**: `python scripts/configuration-tools/pipeline_validator.py --validate sample.json --plan premier`
- **Expected Result**: Exits 0, reporting `STATUS: VALID`.

---

### TC-VAL-02: Exceeded Stage Limit (>25 Stages)
- **Input**: Sub-pipeline containing 26 stages.
- **Expected Result**: Validation fails with `Sub-pipeline has 26 stages, exceeding plan limit of 25.`

---

### TC-VAL-03: Invalid Stage Category
- **Input**: Stage with category `"In Progress"` instead of `"Open"`, `"Closed Won"`, or `"Closed Lost"`.
- **Expected Result**: Validation fails with `Invalid category 'In Progress'.`
