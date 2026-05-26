#!/usr/bin/env bash
set -euo pipefail

REPO_URL="https://github.com/alvax64/tasktree"
SKILL_NAME="tasktree"
REF="${TASKTREE_REF:-main}"
AGENT="${TASKTREE_AGENT:-codex}"
DEST=""
FORCE=0

for arg in "$@"; do
  case "$arg" in
    --agent=*)
      AGENT="${arg#--agent=}"
      ;;
    --dest=*)
      DEST="${arg#--dest=}"
      ;;
    --force)
      FORCE=1
      ;;
    --ref=*)
      REF="${arg#--ref=}"
      ;;
    *)
      echo "Unknown argument: $arg" >&2
      echo "Usage: install.sh [--agent=codex|claude|claude-project] [--dest=/path/to/skills/tasktree] [--force] [--ref=vX.Y.Z]" >&2
      exit 2
      ;;
  esac
done

if [ -z "$DEST" ]; then
  case "$AGENT" in
    codex)
      DEST="${CODEX_HOME:-$HOME/.codex}/skills/$SKILL_NAME"
      ;;
    claude)
      DEST="$HOME/.claude/skills/$SKILL_NAME"
      ;;
    claude-project)
      DEST="$PWD/.claude/skills/$SKILL_NAME"
      ;;
    *)
      echo "Unknown agent: $AGENT" >&2
      echo "Use --dest=/path/to/skills/tasktree for custom agents." >&2
      exit 2
      ;;
  esac
fi

SKILLS_DIR="$(dirname "$DEST")"

if ! command -v git >/dev/null 2>&1; then
  echo "git is required to install tasktree" >&2
  exit 1
fi

mkdir -p "$SKILLS_DIR"

if [ -e "$DEST" ]; then
  if [ "$FORCE" -ne 1 ]; then
    echo "tasktree is already installed at $DEST" >&2
    echo "Run with --force to replace it, or update manually with:" >&2
    echo "  cd \"$DEST\" && git pull" >&2
    exit 1
  fi
  rm -rf "$DEST"
fi

git clone --branch "$REF" "$REPO_URL" "$DEST"

echo "Installed tasktree to $DEST"
echo "Restart your agent to pick up the new skill."
