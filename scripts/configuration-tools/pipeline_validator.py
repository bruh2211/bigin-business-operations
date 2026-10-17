"""
Pipeline Specification Validator & Quota Verifier.
Validates proposed Bigin pipeline architecture against Zoho subscription constraints and structural invariants.
"""

import argparse
import json
import sys
from pathlib import Path

PLAN_LIMITS = {
    "free": {"max_pipelines": 1, "max_sub_pipelines": 1, "max_stages": 25, "max_custom_fields": 5},
    "express": {"max_pipelines": 3, "max_sub_pipelines": 15, "max_stages": 25, "max_custom_fields": 10},
    "premier": {"max_pipelines": 5, "max_sub_pipelines": 25, "max_stages": 25, "max_custom_fields": 25},
    "360": {"max_pipelines": 15, "max_sub_pipelines": 75, "max_stages": 25, "max_custom_fields": 50}
}

VALID_CATEGORIES = {"Open", "Closed Won", "Closed Lost"}

def validate_pipeline_spec(spec_data, plan="premier"):
    plan_rules = PLAN_LIMITS.get(plan.lower(), PLAN_LIMITS["premier"])
    errors = []
    warnings = []
    
    tp = spec_data.get("team_pipeline")
    if not tp:
        return False, ["Missing root 'team_pipeline' object."], []
        
    pipeline_name = tp.get("name")
    if not pipeline_name or len(pipeline_name.strip()) < 3:
        errors.append("Pipeline name must be at least 3 characters long.")
        
    sub_pipelines = tp.get("sub_pipelines", [])
    if not sub_pipelines:
        errors.append("At least one sub-pipeline must be defined.")
        
    for sub in sub_pipelines:
        sub_name = sub.get("name", "Unnamed Sub-pipeline")
        stages = sub.get("stages", [])
        
        if len(stages) > plan_rules["max_stages"]:
            errors.append(f"Sub-pipeline '{sub_name}' has {len(stages)} stages, exceeding plan limit of {plan_rules['max_stages']}.")
            
        has_won = False
        has_lost = False
        
        for stage in stages:
            s_name = stage.get("name")
            category = stage.get("category")
            prob = stage.get("probability", 0)
            
            if not s_name:
                errors.append(f"In '{sub_name}': Found a stage with missing name.")
            if category not in VALID_CATEGORIES:
                errors.append(f"In '{sub_name}': Stage '{s_name}' has invalid category '{category}'. Must be one of {list(VALID_CATEGORIES)}.")
                
            if category == "Closed Won":
                has_won = True
                if prob != 100:
                    warnings.append(f"Stage '{s_name}' is Closed Won but has probability {prob}% (recommended: 100%).")
            elif category == "Closed Lost":
                has_lost = True
                if prob != 0:
                    warnings.append(f"Stage '{s_name}' is Closed Lost but has probability {prob}% (recommended: 0%).")
            else:
                if prob <= 0 or prob >= 100:
                    warnings.append(f"Open stage '{s_name}' has probability {prob}% (recommended: 10-90%).")
                    
        if not has_won:
            warnings.append(f"Sub-pipeline '{sub_name}' has no 'Closed Won' stage.")
        if not has_lost:
            warnings.append(f"Sub-pipeline '{sub_name}' has no 'Closed Lost' stage.")
            
    custom_fields = tp.get("custom_fields", [])
    if len(custom_fields) > plan_rules["max_custom_fields"]:
        errors.append(f"Pipeline specifies {len(custom_fields)} custom fields, exceeding plan limit of {plan_rules['max_custom_fields']}.")
        
    is_valid = len(errors) == 0
    return is_valid, errors, warnings

def main():
    parser = argparse.ArgumentParser(description="Zoho Bigin Pipeline Specification Validator")
    parser.add_argument("--validate", type=str, help="Path to pipeline JSON spec to validate")
    parser.add_argument("--plan", choices=["free", "express", "premier", "360"], default="premier", help="Bigin subscription tier")
    parser.add_argument("--check-limits", action="store_true", help="Print limit table for all editions")
    args = parser.parse_args()
    
    if args.check_limits:
        print("=== Zoho Bigin Subscription Limit Matrix ===")
        print(json.dumps(PLAN_LIMITS, indent=2))
        sys.exit(0)
        
    if not args.validate:
        parser.print_help()
        sys.exit(1)
        
    path = Path(args.validate)
    if not path.exists():
        print(f"[ERROR] Specification file {path} not found.")
        sys.exit(1)
        
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    is_valid, errors, warnings = validate_pipeline_spec(data, args.plan)
    
    print(f"\n--- Validation Report for: {path.name} (Plan: {args.plan.upper()}) ---")
    if is_valid:
        print("[SUCCESS] STATUS: VALID. Ready for browser deployment.")
    else:
        print("[ERROR] STATUS: INVALID. Fix errors before deployment.")
        for err in errors:
            print(f"  [ERROR] {err}")
            
    if warnings:
        print("\n[WARNINGS]:")
        for w in warnings:
            print(f"  [WARN] {w}")
            
    sys.exit(0 if is_valid else 1)

if __name__ == "__main__":
    main()
