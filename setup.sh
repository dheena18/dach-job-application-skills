#!/usr/bin/env sh
# Expose ./skills to agents that auto-discover skills (no file duplication).
# Claude Code reads .claude/skills, Codex and other agents read .agents/skills.
set -e
cd "$(dirname "$0")"
for target in .claude/skills .agents/skills; do
  mkdir -p "$(dirname "$target")"
  [ -e "$target" ] || ln -s "$(pwd)/skills" "$target"
  echo "linked $target -> skills"
done
