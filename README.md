# PCS Vector

Personalized PCS strategic plans for CONUS Army families — **$25 per report**.

Built with Streamlit, Stripe Checkout, Grok AI, and ReportLab PDF export.

## Features

- Guided input form with option buckets
- Stripe Checkout payment gating
- AI-generated 8-section PCS strategic plan
- Professional PDF download
- Optimized for Fort Liberty (Ft Bragg) and Fort Drum

## Quick start (local)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Add your Stripe and Grok keys to secrets.toml
streamlit run app.py
```

## Deploy to Streamlit Cloud

See **[DEPLOYMENT.md](DEPLOYMENT.md)** for full step-by-step instructions including secrets configuration and Stripe redirect setup.

## Configuration

All secrets are loaded from `.streamlit/secrets.toml` (local) or **Streamlit Cloud App Secrets** (production). See `.streamlit/secrets.toml.example`.

---

PCS Vector is an independent planning tool. Not affiliated with the U.S. Department of Defense.