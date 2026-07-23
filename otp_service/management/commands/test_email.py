"""
Management command to test OTP email sending from the terminal.

Usage:
    python manage.py test_email --to loki1432varma@gmail.com
    python manage.py test_email --to yourtest@gmail.com --code 123456
"""
from django.core.management.base import BaseCommand
from otp_service.email_service import send_otp_email


class Command(BaseCommand):
    help = 'Send a test OTP email to verify SMTP + logo embedding'

    def add_arguments(self, parser):
        parser.add_argument(
            '--to',
            type=str,
            required=True,
            help='Recipient email address'
        )
        parser.add_argument(
            '--code',
            type=str,
            default='993773',
            help='OTP code to display in email (default: 993773)'
        )

    def handle(self, *args, **options):
        email = options['to']
        code  = options['code']

        self.stdout.write(f'\n📧 Sending test OTP email to: {email}')
        self.stdout.write(f'   OTP Code: {code}\n')

        result = send_otp_email(email, code)

        if result['success']:
            self.stdout.write(
                self.style.SUCCESS(f'✅ Email sent successfully to {email}!')
            )
            self.stdout.write(
                '\nCheck your inbox and verify:\n'
                '  [ ] Gmail      → logo shows as proper icon\n'
                '  [ ] Zoho Mail  → logo shows (not "Au")\n'
                '  [ ] Outlook    → logo shows (not "A")\n'
            )
        else:
            self.stdout.write(
                self.style.ERROR(f'❌ Failed: {result["message"]}')
            )
            self.stdout.write(
                '\nTroubleshooting:\n'
                '  1. Check EMAIL_HOST_PASSWORD in .env is a Gmail App Password\n'
                '  2. Enable 2FA on Google account: myaccount.google.com/security\n'
                '  3. Generate App Password: myaccount.google.com/apppasswords\n'
                '  4. Make sure logo files are in otp_service/static/images/\n'
            )
