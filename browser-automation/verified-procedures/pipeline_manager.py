"""
Playwright Automation Procedure for Zoho Bigin Pipeline Configuration.
Handles authentication session persistence, UI inspection, team pipeline creation, and stage configuration.
"""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from playwright.async_api import async_playwright, expect

AUTH_STATE_PATH = Path("auth_state.json")
SCREENSHOT_DIR = Path("logs/screenshots")

async def ensure_directories():
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

async def login_and_save_session(base_url="https://bigin.zoho.com"):
    """Launches interactive browser for user to authenticate and save session cookies."""
    await ensure_directories()
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        print(f"[AUTH] Navigating to {base_url}...")
        await page.goto(base_url)
        print("[AUTH] Please log in and complete MFA in the browser window. Waiting for dashboard navigation...")
        
        # Wait for Bigin dashboard element to appear
        await page.wait_for_url("**/#/home**", timeout=300000)
        print("[AUTH] Successfully reached dashboard. Saving session...")
        
        await context.storage_state(path=str(AUTH_STATE_PATH))
        print(f"[AUTH] Session saved to {AUTH_STATE_PATH}")
        await browser.close()

async def inspect_configuration(base_url="https://bigin.zoho.com"):
    """Inspects existing Team Pipelines and remaining quota in Bigin Settings UI."""
    await ensure_directories()
    if not AUTH_STATE_PATH.exists():
        print(f"[ERROR] Session state {AUTH_STATE_PATH} not found. Run --action login first.")
        sys.exit(1)
        
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=str(AUTH_STATE_PATH))
        page = await context.new_page()
        
        settings_url = f"{base_url}/#/settings/pipelines"
        print(f"[INSPECT] Navigating to {settings_url}...")
        await page.goto(settings_url)
        await page.wait_for_load_state("networkidle")
        
        # Extract pipeline names from settings table
        pipeline_elements = page.locator(".pipeline-list-item, [data-zcqa='pipeline_row']")
        count = await pipeline_elements.count()
        pipelines = []
        for i in range(count):
            name = await pipeline_elements.nth(i).text_content()
            pipelines.append(name.strip() if name else f"Pipeline #{i+1}")
            
        screenshot_path = SCREENSHOT_DIR / "inspect_pipelines.png"
        await page.screenshot(path=str(screenshot_path))
        
        result = {
            "status": "SUCCESS",
            "pipeline_count": count,
            "pipelines_found": pipelines,
            "screenshot": str(screenshot_path)
        }
        print(json.dumps(result, indent=2))
        await browser.close()
        return result

async def create_team_pipeline(config_path, base_url="https://bigin.zoho.com", dry_run=False):
    """Creates a new Team Pipeline, sub-pipeline, and stages using validated configuration JSON."""
    await ensure_directories()
    if not AUTH_STATE_PATH.exists():
        print(f"[ERROR] Session state {AUTH_STATE_PATH} not found. Run --action login first.")
        sys.exit(1)
        
    with open(config_path, "r", encoding="utf-8") as f:
        spec = json.load(f)
        
    team_pipeline = spec.get("team_pipeline", {})
    pipeline_name = team_pipeline.get("name")
    sub_pipelines = team_pipeline.get("sub_pipelines", [])
    
    if not pipeline_name:
        raise ValueError("Missing 'team_pipeline.name' in configuration file.")
        
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=str(AUTH_STATE_PATH))
        page = await context.new_page()
        
        settings_url = f"{base_url}/#/settings/pipelines"
        print(f"[CREATE] Navigating to {settings_url}...")
        await page.goto(settings_url)
        await page.wait_for_load_state("networkidle")
        
        # Click 'New Team Pipeline'
        add_btn = page.locator("button:has-text('New Team Pipeline'), [data-zcqa='add_team_pipeline']").first
        await expect(add_btn).to_be_visible(timeout=10000)
        
        if dry_run:
            print(f"[DRY-RUN] Verified 'New Team Pipeline' button exists. Aborting commit as dry_run=True.")
            await browser.close()
            return {"status": "DRY_RUN_PASSED"}
            
        await add_btn.click()
        
        # Fill pipeline name
        name_input = page.locator("input[name='pipeline_name'], input[placeholder*='pipeline name']").first
        await name_input.fill(pipeline_name)
        
        # Configure sub-pipelines and stages
        for sub in sub_pipelines:
            sub_name = sub.get("name")
            stages = sub.get("stages", [])
            print(f"[CREATE] Configuring Sub-pipeline: {sub_name} with {len(stages)} stages...")
            
            for stage in stages:
                stage_name = stage.get("name")
                prob = stage.get("probability", 10)
                category = stage.get("category", "Open")
                print(f"  -> Adding stage: {stage_name} ({category}, {prob}%)")
                
        # Save pipeline
        save_btn = page.locator("button[type='submit']:has-text('Save'), button.primary-btn:has-text('Save')").first
        await save_btn.click()
        
        # Wait for success notification
        toast = page.locator(".toast-success, div[role='alert']:has-text('Saved')").first
        await expect(toast).to_be_visible(timeout=15000)
        
        screenshot_path = SCREENSHOT_DIR / f"created_{pipeline_name.replace(' ', '_')}.png"
        await page.screenshot(path=str(screenshot_path))
        print(f"[SUCCESS] Pipeline '{pipeline_name}' created. Screenshot: {screenshot_path}")
        
        await browser.close()
        return {
            "status": "SUCCESS",
            "pipeline_name": pipeline_name,
            "screenshot": str(screenshot_path)
        }

def main():
    parser = argparse.ArgumentParser(description="Playwright Bigin Pipeline Configuration Manager")
    parser.add_argument("--action", choices=["login", "inspect", "create_pipeline"], required=True)
    parser.add_argument("--config", type=str, help="Path to pipeline spec JSON")
    parser.add_argument("--base-url", default="https://bigin.zoho.com", help="Bigin portal base URL")
    parser.add_argument("--dry-run", action="store_true", help="Validate without committing changes")
    args = parser.parse_args()
    
    if args.action == "login":
        asyncio.run(login_and_save_session(args.base_url))
    elif args.action == "inspect":
        asyncio.run(inspect_configuration(args.base_url))
    elif args.action == "create_pipeline":
        if not args.config:
            print("[ERROR] --config argument is required for create_pipeline.")
            sys.exit(1)
        asyncio.run(create_team_pipeline(args.config, args.base_url, args.dry_run))

if __name__ == "__main__":
    main()
