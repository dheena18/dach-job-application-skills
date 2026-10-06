# Expose .\skills to agents that auto-discover skills (no file duplication).
# Claude Code reads .claude\skills, Codex and other agents read .agents\skills.
# Uses directory junctions, which need no admin rights on Windows.
$root = $PSScriptRoot
foreach ($target in @(".claude\skills", ".agents\skills")) {
    $link = Join-Path $root $target
    New-Item -ItemType Directory -Force (Split-Path $link) | Out-Null
    if (-not (Test-Path $link)) {
        New-Item -ItemType Junction -Path $link -Target (Join-Path $root "skills") | Out-Null
    }
    Write-Host "linked $target -> skills"
}
