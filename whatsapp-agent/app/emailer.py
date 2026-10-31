"""Plain-text e-mail to the owner over SMTP (escalations, leads, daily digest)."""

from __future__ import annotations

import smtplib
from email.message import EmailMessage

from .config import Settings


def send_email(settings: Settings, subject: str, body: str) -> None:
    s = settings
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = s.smtp_from or s.smtp_user
    msg["To"] = s.smtp_to
    msg.set_content(body)
    if s.smtp_use_ssl:
        server: smtplib.SMTP = smtplib.SMTP_SSL(s.smtp_host, s.smtp_port, timeout=20)
    else:
        server = smtplib.SMTP(s.smtp_host, s.smtp_port, timeout=20)
        server.starttls()
    with server:
        if s.smtp_user:
            server.login(s.smtp_user, s.smtp_password)
        server.send_message(msg)
