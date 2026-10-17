#!/usr/bin/env bash
# Universal 1-Line Remote & Local Installer for Zoho Bigin Business Operations Skill.
# Works directly via GitHub:
#   curl -fsSL https://raw.githubusercontent.com/bruh2211/bigin-business-operations/main/install.sh | bash

set -e

REPO_URL="${1:-https://github.com/bruh2211/bigin-business-operations.git}"

echo "=========================================================="
echo "Installing Zoho Bigin Business Operations Skill via GitHub"
echo "Universal Target: Antigravity 2.0 & Claude Code"
echo "=========================================================="

BASE_STORAGE_DIR="$HOME/.agents/skills"
CANONICAL_DIR="$BASE_STORAGE_DIR/bigin-business-operations"
GEMINI_SKILLS_DIR="$HOME/.gemini/config/skills"
CLAUDE_SKILLS_DIR="$HOME/.claude/skills"
GEMINI_TARGET="$GEMINI_SKILLS_DIR/bigin-business-operations"
CLAUDE_TARGET="$CLAUDE_SKILLS_DIR/bigin-business-operations"

# Check if running locally or piped via curl
if [ -n "$BASH_SOURCE" ] && [ -f "$(dirname "${BASH_SOURCE[0]}")/SKILL.md" ]; then
    SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    echo "[LOCAL] Using local source directory: $SOURCE_DIR"
else
    echo "[REMOTE] Downloading skill repository to: $CANONICAL_DIR"
    mkdir -p "$BASE_STORAGE_DIR"
    if [ -d "$CANONICAL_DIR/.git" ]; then
        echo "[GIT] Existing directory found. Pulling latest updates..."
        git -C "$CANONICAL_DIR" pull
    else
        git clone "$REPO_URL" "$CANONICAL_DIR"
    fi
    SOURCE_DIR="$CANONICAL_DIR"
fi

# Ensure parent directories exist
mkdir -p "$GEMINI_SKILLS_DIR" "$CLAUDE_SKILLS_DIR"

# Link for Antigravity 2.0
if [ -e "$GEMINI_TARGET" ]; then
    echo "[OK] Antigravity 2.0 link verified at: $GEMINI_TARGET"
else
    ln -s "$SOURCE_DIR" "$GEMINI_TARGET"
    echo "[SUCCESS] Created Antigravity symlink: $GEMINI_TARGET"
fi

# Link for Claude Code
if [ -e "$CLAUDE_TARGET" ]; then
    echo "[OK] Claude Code link verified at: $CLAUDE_TARGET"
else
    ln -s "$SOURCE_DIR" "$CLAUDE_TARGET"
    echo "[SUCCESS] Created Claude Code symlink: $CLAUDE_TARGET"
fi

echo ""
echo "Skill successfully installed for both Antigravity 2.0 and Claude Code!"
echo "Your co-worker can now ask either AI assistant:"
echo "  'Help me design and create a customer onboarding pipeline in Bigin'"
