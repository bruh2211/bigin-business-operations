<#
.SYNOPSIS
    Universal 1-Click Remote & Local Installer for Zoho Bigin Business Operations Skill.
    Works directly via GitHub:
      irm https://raw.githubusercontent.com/bruh2211/bigin-business-operations/main/install.ps1 | iex
#>

param(
    [string]$RepoUrl = "https://github.com/bruh2211/bigin-business-operations.git"
)

$ErrorActionPreference = "Stop"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Installing Zoho Bigin Business Operations Skill via GitHub" -ForegroundColor Cyan
Write-Host "Universal Target: Antigravity 2.0 & Claude Code" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$BaseStorageDir = "$HOME\.agents\skills"
$CanonicalDir = Join-Path $BaseStorageDir "bigin-business-operations"
$GeminiSkillsDir = "$HOME\.gemini\config\skills"
$ClaudeSkillsDir = "$HOME\.claude\skills"
$GeminiTarget = Join-Path $GeminiSkillsDir "bigin-business-operations"
$ClaudeTarget = Join-Path $ClaudeSkillsDir "bigin-business-operations"

# 1. Ensure canonical skill folder exists (clone if running via web)
if ($PSScriptRoot -and (Test-Path "$PSScriptRoot\SKILL.md")) {
    $SourceDir = $PSScriptRoot
    Write-Host "[LOCAL] Using local source directory: $SourceDir" -ForegroundColor White
} else {
    Write-Host "[REMOTE] Downloading skill repository to: $CanonicalDir" -ForegroundColor White
    New-Item -ItemType Directory -Force -Path $BaseStorageDir | Out-Null
    if (Test-Path $CanonicalDir) {
        Write-Host "[GIT] Existing directory found. Pulling latest updates..." -ForegroundColor Yellow
        git -C $CanonicalDir pull
    } else {
        git clone $RepoUrl $CanonicalDir
    }
    $SourceDir = $CanonicalDir
}

# 2. Ensure parent directories exist
New-Item -ItemType Directory -Force -Path $GeminiSkillsDir, $ClaudeSkillsDir | Out-Null

# 3. Create Junction for Antigravity 2.0
if (Test-Path $GeminiTarget) {
    Write-Host "[OK] Antigravity 2.0 link verified at: $GeminiTarget" -ForegroundColor Yellow
} else {
    cmd /c "mklink /J `"$GeminiTarget`" `"$SourceDir`""
    Write-Host "[SUCCESS] Created Antigravity junction: $GeminiTarget" -ForegroundColor Green
}

# 4. Create Junction for Claude Code
if (Test-Path $ClaudeTarget) {
    Write-Host "[OK] Claude Code link verified at: $ClaudeTarget" -ForegroundColor Yellow
} else {
    cmd /c "mklink /J `"$ClaudeTarget`" `"$SourceDir`""
    Write-Host "[SUCCESS] Created Claude Code junction: $ClaudeTarget" -ForegroundColor Green
}

Write-Host "`n Skill successfully installed for both Antigravity 2.0 and Claude Code!" -ForegroundColor Green
Write-Host "Your co-worker can now ask either AI assistant:" -ForegroundColor White
Write-Host "  'Help me design and create a customer onboarding pipeline in Bigin'" -ForegroundColor Cyan
Write-Host "  'Review Bigin subscription limits and configure stages'" -ForegroundColor Cyan
