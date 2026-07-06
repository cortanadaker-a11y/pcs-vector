#!/usr/bin/env bash
# Commit all changes and push to GitHub → Streamlit Cloud rebuilds automatically.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

BRANCH="${DEPLOY_BRANCH:-main}"
REMOTE="${DEPLOY_REMOTE:-origin}"

if ! git rev-parse --git-dir >/dev/null 2>&1; then
  echo "Not a git repository: $ROOT" >&2
  exit 1
fi

CURRENT="$(git branch --show-current)"
if [[ "$CURRENT" != "$BRANCH" ]]; then
  echo "On branch '$CURRENT'; switch to '$BRANCH' before deploying." >&2
  exit 1
fi

if git diff --quiet && git diff --cached --quiet && [[ -z "$(git status -u --porcelain)" ]]; then
  echo "Nothing to deploy — working tree clean."
  exit 0
fi

MSG="${1:-Auto-deploy: $(date -u '+%Y-%m-%d %H:%M UTC')}"

git add -A
# Respect .gitignore; secrets.toml stays untracked.
git commit -m "$MSG"
git push "$REMOTE" "$BRANCH"

echo "Deployed to $REMOTE/$BRANCH — Streamlit Cloud will rebuild in ~2–5 min."