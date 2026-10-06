# Expose .\skills to agents that auto-discover skills (no file duplication).
# Claude Code reads .claude\skills, Codex and other agents read .agents\skills.
# Uses directory junctions, which need no admin rights on Windows.
$root = $PSScriptRoot
foreach ($target in @(".claude\skills", ".agents\skills")) {
    $link = Join-Path $root $target
    New-Item -ItemType Directory -Force (Split-Path $link) | Out-Null
    $item = Get-Item $link -Force -ErrorAction SilentlyContinue
    if ($item -and $item.LinkType) {
        # refresh a stale or broken junction
        $item.Delete()
        $item = $null
    }
    if ($item) {
        Write-Warning "skipped $target (a real directory already exists; remove it to link)"
        continue
    }
    New-Item -ItemType Junction -Path $link -Target (Join-Path $root "skills") | Out-Null
    Write-Host "linked $target -> skills"
}
