#!/usr/bin/env python3
"""Send a one-page test PDF via the configured SMTP connector.

Usage:
  .venv/bin/python scripts/test_email.py --to you@example.com

Requires [email] in .streamlit/secrets.toml (or PCS_EMAIL_* env vars).
"""

from __future__ import annotations

import argparse
import sys
from io import BytesIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def _minimal_pdf() -> bytes:
    """Tiny valid PDF without heavy dependencies."""
    # Minimal single-page PDF (Hello PCS Vector).
    content = b"""%PDF-1.4
1 0 obj<< /Type /Catalog /Pages 2 0 R >>endobj
2 0 obj<< /Type /Pages /Kids [3 0 R] /Count 1 >>endobj
3 0 obj<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792]
/Contents 4 0 R /Resources<< /Font<< /F1 5 0 R >> >> >>endobj
4 0 obj<< /Length 55 >>stream
BT /F1 18 Tf 72 720 Td (PCS Vector email test) Tj ET
endstream endobj
5 0 obj<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>endobj
xref
0 6
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000266 00000 n 
0000000371 00000 n 
trailer<< /Size 6 /Root 1 0 R >>
startxref
444
%%EOF
"""
    return content


def main() -> None:
    parser = argparse.ArgumentParser(description="Test PCS Vector SMTP email delivery")
    parser.add_argument("--to", required=True, help="Recipient email address")
    args = parser.parse_args()

    from services.email_delivery import (
        EmailDeliveryError,
        get_smtp_config,
        is_email_configured,
        send_report_pdf_email,
    )

    if not is_email_configured():
        print("FAIL: Email is not configured.")
        print("Add an [email] block to .streamlit/secrets.toml — see DEPLOYMENT.md.")
        print("Resend example (recommended):")
        print('  [email]')
        print('  smtp_host = "smtp.resend.com"')
        print('  smtp_port = 587')
        print('  smtp_user = "resend"')
        print('  smtp_password = "re_xxxxxxxx"')
        print('  from_address = "PCS Vector <reports@yourdomain.com>"')
        print('  use_tls = true')
        print("Testing without a domain: from_address = \"PCS Vector <onboarding@resend.dev>\"")
        print("(only works when --to is the email on your Resend account)")
        sys.exit(1)

    cfg = get_smtp_config() or {}
    print(f"SMTP host: {cfg.get('host')}:{cfg.get('port')}")
    print(f"Provider:  {cfg.get('provider')}")
    print(f"SSL/TLS:   use_ssl={cfg.get('use_ssl')} use_tls={cfg.get('use_tls')}")
    print(f"From:      {cfg.get('from_address')}")
    print(f"To:        {args.to}")
    print("Sending test PDF…")

    try:
        send_report_pdf_email(
            args.to,
            _minimal_pdf(),
            order_reference="PCS-TESTEMAIL",
            family_name="Test User",
            pdf_filename="pcs-vector-email-test.pdf",
        )
    except EmailDeliveryError as exc:
        print(f"FAIL: {exc}")
        sys.exit(1)

    print("OK: Test email sent. Check inbox (and spam).")


if __name__ == "__main__":
    main()