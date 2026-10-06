#!/usr/bin/env sh
# Expose ./skills to agents that auto-discover skills (no file duplication).
# Claude Code reads .claude/skills, Codex and other agents read .agents/skills.
# macOS/Linux (and WSL). On Windows use setup.ps1 instead.
set -e
cd "$(dirname "$0")"
for target in .claude/skills .agents/skills; do
  mkdir -p "$(dirname "$target")"
  if [ -L "$target" ]; then
    rm "$target"                       # refresh a stale or dangling link
  elif [ -e "$target" ]; then
    echo "skipped $target (a real directory already exists; remove it to link)" >&2
    continue
  fi
  ln -s "../skills" "$target"          # relative link: survives moving the repo
  echo "linked $target -> skills"
done
