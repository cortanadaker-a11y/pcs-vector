# PCS Vector — Pre-Launch Checklist

Use this checklist before sharing PCS Vector publicly or switching Stripe to live mode.

---

## Product & UX

- [ ] Home page clearly explains value, pricing, and what's included
- [ ] Full flow tested: Home → Form → Stripe → Success screen → Report → PDF
- [ ] Cancelled payment shows retry banner; form data preserved
- [ ] FAQ answers common questions (report contents, payment, privacy)
- [ ] Error messages are clear (missing secrets, Grok timeout, payment failure)
- [ ] Mobile layout is acceptable on phone browser

---

## Configuration & Secrets

- [ ] `secrets.toml` is **not** committed to git
- [ ] Streamlit Cloud Secrets configured with all keys:
  - [ ] `[stripe] publishable_key`
  - [ ] `[stripe] secret_key`
  - [ ] `[grok] api_key`
  - [ ] `[pcs_vector] app_url` (exact live URL, no trailing slash)
- [ ] Sidebar shows no "Configuration incomplete" warning in production
- [ ] Grok API key has sufficient quota for expected traffic

---

## Stripe (Test → Live)

- [ ] End-to-end payment tested with test card `4242 4242 4242 4242`
- [ ] Success redirect returns to live `app_url` correctly
- [ ] Cancel redirect shows retry UX on input form
- [ ] Order reference displays on success screen
- [ ] Stripe Dashboard shows completed checkout sessions
- [ ] **Before live:** swap to `pk_live_` / `sk_live_` keys in Streamlit Secrets
- [ ] **Before live:** complete one real small-amount test payment

---

## Report Quality

- [ ] Test report for Fort Liberty (Ft Bragg) — local specifics present
- [ ] Test report for Fort Drum — winter/heating/school notes present
- [ ] PDF downloads correctly and all 8 sections render
- [ ] Regenerate report works after payment verification
- [ ] BAH/housing disclaimer visible (verify with finance office)

---

## Legal & Trust

- [ ] "Not affiliated with the DoD" disclaimer visible
- [ ] Privacy posture documented (session-only data, Stripe for payments)
- [ ] Refund/support contact path defined (email on Stripe receipt or support address)
- [ ] Testimonial/claims on landing page are accurate and defensible

---

## Deployment

- [ ] App deployed to Streamlit Community Cloud from GitHub
- [ ] `requirements.txt` installs cleanly on Cloud
- [ ] App reboots successfully after secrets changes
- [ ] Logs checked for runtime errors after deploy
- [ ] DEPLOYMENT.md steps followed

---

## Launch Day

- [ ] Share link with 2–3 trusted beta users for feedback
- [ ] Monitor Stripe Dashboard for first real payments
- [ ] Monitor Streamlit Cloud logs for Grok/Stripe errors
- [ ] Have plan for support requests (bad report, payment issues)

---

## Post-Launch (Nice to Have)

- [ ] Custom Streamlit subdomain (if desired)
- [ ] Stripe webhook for payment audit trail
- [ ] Email delivery of PDF receipt
- [ ] More installation profiles beyond Bragg/Drum
- [ ] Analytics on conversion (form start → payment → report)