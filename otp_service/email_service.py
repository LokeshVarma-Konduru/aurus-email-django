"""
Aurus AI — Email Service
Sends OTP emails with the logo embedded as a base64 data URI
(no attachment chip in Gmail inbox)
"""
import base64
import logging
from pathlib import Path

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)


def _load_logo_data_uri() -> str:
    """
    Load the configured logo file and return it as a base64 data URI.
    Falls back to an empty string if the file can't be found.
    """
    logo_key  = getattr(settings, 'EMAIL_LOGO_KEY', 'logo_white')
    logos     = getattr(settings, 'LOGOS', {})
    logo_path = logos.get(logo_key)

    if not logo_path or not Path(logo_path).exists():
        logger.warning(
            "Logo file not found: %s. Email will send without a logo.", logo_path
        )
        return ''

    with open(logo_path, 'rb') as f:
        data = f.read()

    ext = Path(logo_path).suffix.lower()
    mime_type = {
        '.jpeg': 'image/jpeg',
        '.jpg':  'image/jpeg',
        '.png':  'image/png',
        '.gif':  'image/gif',
        '.webp': 'image/webp',
    }.get(ext, 'image/jpeg')

    base64_string = base64.b64encode(data).decode('ascii')
    return f'data:{mime_type};base64,{base64_string}'


def send_otp_email(email: str, otp_code: str) -> dict:
    """
    Send OTP email to the given address with the Aurus branding.

    The logo is embedded as a base64 data URI directly in the HTML,
    so no attachment appears in the recipient's inbox.

    Returns:
        {'success': True/False, 'message': str}
    """

    subject = f'Your Aurus sign-in code: {otp_code}'

    # ── 1. Render HTML template ───────────────────────────────────────────────
    context = {
        'otp_code':       otp_code,
        'expiry_minutes': getattr(settings, 'OTP_EXPIRY_MINUTES', 10),
        'logo_data_uri':  _load_logo_data_uri(),
        'company_name':   'Aurus AI',
        'portal_name':    'Employee Portal',
    }

    html_body  = render_to_string('emails/otp_email.html', context)
    plain_body = strip_tags(html_body)          # plain-text fallback

    # ── 2. Build and send email message ───────────────────────────────────────
    msg = EmailMultiAlternatives(
        subject    = subject,
        body       = plain_body,                # plain-text part
        from_email = settings.DEFAULT_FROM_EMAIL,
        to         = [email],
    )
    msg.attach_alternative(html_body, 'text/html')

    try:
        msg.send(fail_silently=False)
        logger.info("OTP email sent to %s", email)
        return {'success': True, 'message': 'OTP sent successfully.'}

    except Exception as exc:
        logger.error("Failed to send OTP email to %s: %s", email, exc)
        return {'success': False, 'message': f'Failed to send email: {str(exc)}'}
