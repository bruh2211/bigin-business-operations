# 🎭 Playwright Browser Automation Guide for Zoho Bigin

This guide details the implementation of deterministic Playwright scripts for navigating Zoho Bigin Settings, creating Team Pipelines, and managing stages.

---

## 1. Session Persistence & Authentication

To avoid repeated multi-factor authentication (MFA) prompts, Playwright uses a persistent storage state:

1. **Initial Login & Session Capture**:
   - Run interactive authentication once to generate `auth_state.json`:
   ```bash
   python browser-automation/verified-procedures/pipeline_manager.py --action login
   ```
2. **Re-using Session in Headless Mode**:
   - Subsequent script runs load `auth_state.json` directly into the Playwright browser context, bypassing login screens.

---

## 2. Robust Selector Hierarchy for Zoho Bigin

Zoho Bigin frequently utilizes custom attributes and Ember/React component patterns. Always use this prioritized hierarchy:

1. **Data attributes**: `[data-zcqa="add_team_pipeline"]`, `[data-id="settings-icon"]`
2. **Accessible Role + Name**: `page.get_by_role("button", name="New Team Pipeline")`
3. **Scoped Form Selectors**: `form.pipeline-form input[name="pipeline_name"]`
4. **Resilient Text Matching**: `button:has-text("Save")`, `button:has-text("Next")`

---

## 3. Error Handling & Modal Dismissal

Zoho Bigin occasionally displays onboarding overlays or tip banners. The automation script includes automatic handlers to detect and dismiss them:
```python
async def dismiss_dialogs(page):
    overlays = page.locator(".zp-popover-close, .introjs-skipbutton, .banner-close")
    if await overlays.count() > 0:
        await overlays.first.click()
```
