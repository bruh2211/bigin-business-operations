# 🛰️ Zoho Bigin Business Operations Skill: Team Distribution Guide

This skill is built on the universal `agentskills.io` standard and is designed to work simultaneously across **Google Antigravity 2.0** and **Claude Code**.

---

## 🚀 Direct 1-Line Installation via GitHub (Fastest for Co-workers)

Once pushed to GitHub (`https://github.com/bruh2211/bigin-business-operations`), your co-worker can install it globally with a single terminal command:

### On Windows (PowerShell):
```powershell
irm https://raw.githubusercontent.com/bruh2211/bigin-business-operations/main/install.ps1 | iex
```

### On macOS / Linux (Terminal):
```bash
curl -fsSL https://raw.githubusercontent.com/bruh2211/bigin-business-operations/main/install.sh | bash
```

### What this 1-liner does automatically:
1. Clones the repository into `~/.agents/skills/bigin-business-operations`.
2. Creates an OS junction / symlink into `~/.gemini/config/skills/bigin-business-operations` (**Antigravity 2.0**).
3. Creates an OS junction / symlink into `~/.claude/skills/bigin-business-operations` (**Claude Code**).
4. Running the same command in the future will automatically `git pull` the latest updates.

---

## 📦 Alternative: Zero-Setup via Git Workspace Repository

If you prefer to bundle the skill directly inside a shared project repository:

1. Commit `.agents/skills/bigin-business-operations` and `.claude/skills/bigin-business-operations` to your project repository.
2. When your co-worker runs `git pull`:
   - **Antigravity 2.0** automatically discovers `.agents/skills/`.
   - **Claude Code** automatically discovers `.claude/skills/`.
   - No installation script is needed.
