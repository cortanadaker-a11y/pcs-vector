# PCS Vector — agent instructions

## Auto-deploy for beta testing

**Do not leave fixes local only.** After any code change in this repo:

1. Run `./scripts/deploy.sh "short description of changes"` from the repo root, **or**
2. `git add` + `git commit` (the post-commit hook pushes to `origin/main` automatically).

Streamlit Community Cloud rebuilds on every push to `main` (~2–5 minutes).

- Never commit `.streamlit/secrets.toml` (gitignored).
- Deploy branch: `main`
- Entry point: `app.py`

## Skip auto-push (rare)

```bash
PCS_SKIP_AUTO_PUSH=1 git commit -m "wip"
```