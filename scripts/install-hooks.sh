#!/usr/bin/env bash
# One-time setup: enable auto-push after every commit on main.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

chmod +x "$ROOT/scripts/deploy.sh"
chmod +x "$ROOT/.githooks/post-commit"

git config core.hooksPath .githooks

echo "Git hooks installed (core.hooksPath=.githooks)"
echo "  • Every commit on main auto-pushes to GitHub → Streamlit Cloud rebuilds"
echo "  • Manual deploy: ./scripts/deploy.sh \"your message\""
echo "  • Skip auto-push once: PCS_SKIP_AUTO_PUSH=1 git commit ..."