# PCS Vector — Deployment Guide (Streamlit Community Cloud)

This guide walks you through deploying PCS Vector with working Stripe payments and Grok report generation.

---

## Prerequisites

- [GitHub](https://github.com) account
- [Streamlit Community Cloud](https://share.streamlit.io) account (free)
- [Stripe](https://dashboard.stripe.com) account (test mode for MVP)
- [xAI](https://console.x.ai) Grok API key

---

## 1. Prepare the repository

### Project structure (deploy root)

```
pcs-vector/
├── app.py                  # Main entry point (set this in Streamlit Cloud)
├── requirements.txt
├── .streamlit/
│   ├── config.toml         # Theme & server settings
│   └── secrets.toml.example
├── components/
├── services/
└── views/
```

### Push to GitHub

```bash
cd pcs-vector
git init
git add .
git commit -m "Initial PCS Vector deployment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/pcs-vector.git
git push -u origin main
```

**Important:** `secrets.toml` is gitignored. Never commit API keys.

---

## 2. Deploy to Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
2. Click **Create app**.
3. Select your repository: `YOUR_USERNAME/pcs-vector`.
4. Set **Main file path** to: `app.py`
5. Choose **main** branch (or your deploy branch).
6. Click **Deploy**.

The first build installs dependencies from `requirements.txt` and may take 2–5 minutes.

---

## 3. Configure secrets on Streamlit Cloud

After the first deploy, open your app → **⚙️ Settings** → **Secrets** and paste:

```toml
[stripe]
publishable_key = "pk_test_YOUR_PUBLISHABLE_KEY"
secret_key = "sk_test_YOUR_SECRET_KEY"

[grok]
api_key = "xai-YOUR_GROK_API_KEY"

[pcs_vector]
app_url = "https://YOUR-APP-NAME.streamlit.app"
```

### Where to find keys

| Secret | Source |
|--------|--------|
| `stripe.publishable_key` | [Stripe Dashboard → API keys](https://dashboard.stripe.com/test/apikeys) |
| `stripe.secret_key` | Same page (keep secret) |
| `grok.api_key` | [xAI Console](https://console.x.ai) |
| `pcs_vector.app_url` | Your live Streamlit URL (copy from browser after deploy) |

Click **Save**. The app will reboot automatically.

---

## 4. Update Stripe redirect URLs (critical)

Stripe Checkout redirects users back to `pcs_vector.app_url` after payment.

1. Copy your live URL exactly, e.g. `https://pcs-vector-abc123.streamlit.app`
2. Paste it as `pcs_vector.app_url` in Streamlit Secrets
3. **Reboot** the app (Settings → Reboot app) if you change secrets after initial deploy

The app also attempts runtime URL detection on Streamlit Cloud, but **explicit `app_url` is strongly recommended** for reliable payment redirects.

---

## 5. Verify the payment flow

Use Stripe **test mode** keys and test card:

| Field | Value |
|-------|-------|
| Card number | `4242 4242 4242 4242` |
| Expiry | Any future date |
| CVC | Any 3 digits |

### Test checklist

- [ ] Home page loads
- [ ] Input form saves and redirects to Stripe Checkout
- [ ] Successful payment returns to app with success screen
- [ ] Grok report generates with loading indicator
- [ ] PDF download works
- [ ] Cancelled payment shows retry banner with saved form data

---

## 6. Local development

```bash
cd pcs-vector
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit secrets.toml with your keys
streamlit run app.py
```

Local URL defaults to `http://localhost:8501` for Stripe redirects.

---

## 7. Pre-launch checklist

Before going live, complete every item in **[PRELAUNCH.md](PRELAUNCH.md)**.

---

## 8. Production considerations

### Before going live

- [ ] Switch Stripe to **live** keys (`pk_live_…`, `sk_live_…`)
- [ ] Use a production Grok API key with appropriate rate limits
- [ ] Set `pcs_vector.app_url` to your production Streamlit URL
- [ ] Test the full payment flow end-to-end in live mode with a real card
- [ ] Review Stripe Dashboard for successful payments

### Security

- All secrets live in Streamlit Cloud **Secrets** (or local `secrets.toml`)
- No API keys in source code
- Payment is re-verified with Stripe before report generation and PDF export
- `secrets.toml` is in `.gitignore`

### Limitations (MVP)

- Session state is per-browser-session — users who clear cookies after payment may need support
- No webhook-based receipt storage yet (verification uses Checkout Session retrieve)
- Grok generation can take 15–30 seconds; loading UI handles this

### Monitoring

- **Streamlit Cloud** → App → **Manage app** → Logs (runtime errors)
- **Stripe Dashboard** → Payments (checkout completions)
- Sidebar shows configuration warnings if secrets are missing

---

## 9. Troubleshooting

| Issue | Fix |
|-------|-----|
| "Stripe secret key not found" | Add secrets in Streamlit Cloud Settings → Secrets |
| Payment succeeds but redirect fails | Set `pcs_vector.app_url` to exact live URL (no trailing slash) |
| "Grok API key not found" | Add `[grok] api_key` to secrets |
| Report never generates | Check Streamlit logs; verify Grok key and network access |
| App build fails | Confirm `requirements.txt` and `app.py` path in deploy settings |

---

## 10. Re-deploying updates

Push changes to GitHub — Streamlit Cloud rebuilds automatically:

```bash
git add .
git commit -m "Your update message"
git push
```

Secrets persist across deploys unless you change them in the dashboard.