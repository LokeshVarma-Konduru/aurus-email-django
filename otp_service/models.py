"""
OTP Model — stores generated OTPs with expiry tracking
"""
import random
import string
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.conf import settings


def generate_otp_code():
    """Generate a secure 6-digit numeric OTP."""
    return ''.join(random.choices(string.digits, k=settings.OTP_LENGTH))


class OTPRecord(models.Model):

    STATUS_PENDING  = 'pending'
    STATUS_VERIFIED = 'verified'
    STATUS_EXPIRED  = 'expired'
    STATUS_CHOICES  = [
        (STATUS_PENDING,  'Pending'),
        (STATUS_VERIFIED, 'Verified'),
        (STATUS_EXPIRED,  'Expired'),
    ]

    email      = models.EmailField(db_index=True)
    code       = models.CharField(max_length=10, default=generate_otp_code)
    status     = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    verified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'OTP Record'
        verbose_name_plural = 'OTP Records'

    def save(self, *args, **kwargs):
        # Auto-set expiry on first save
        if not self.pk:
            self.expires_at = timezone.now() + timedelta(
                minutes=settings.OTP_EXPIRY_MINUTES
            )
        super().save(*args, **kwargs)

    def is_expired(self):
        """True if OTP has passed its expiry time."""
        return timezone.now() > self.expires_at

    def is_valid(self):
        """True if OTP is pending AND not expired."""
        return self.status == self.STATUS_PENDING and not self.is_expired()

    def verify(self, code):
        """
        Check the code. Returns (success: bool, message: str).
        Marks record as verified or expired automatically.
        """
        if self.is_expired():
            self.status = self.STATUS_EXPIRED
            self.save(update_fields=['status'])
            return False, 'OTP has expired. Please request a new one.'

        if self.status == self.STATUS_VERIFIED:
            return False, 'OTP has already been used.'

        if self.status == self.STATUS_EXPIRED:
            return False, 'OTP has expired.'

        if self.code != code:
            return False, 'Invalid OTP. Please try again.'

        # ✅ Valid
        self.status     = self.STATUS_VERIFIED
        self.verified_at = timezone.now()
        self.save(update_fields=['status', 'verified_at'])
        return True, 'OTP verified successfully.'

    def __str__(self):
        return f'{self.email} | {self.code} | {self.status}'
