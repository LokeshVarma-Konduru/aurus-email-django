"""
OTP API Serializers — validate incoming request data
"""
from rest_framework import serializers


class SendOTPSerializer(serializers.Serializer):
    """Validates /api/otp/send/ payload."""
    email = serializers.EmailField(
        required=True,
        error_messages={
            'required': 'Email address is required.',
            'invalid':  'Enter a valid email address.',
        }
    )


class VerifyOTPSerializer(serializers.Serializer):
    """Validates /api/otp/verify/ payload."""
    email = serializers.EmailField(
        required=True,
        error_messages={
            'required': 'Email address is required.',
            'invalid':  'Enter a valid email address.',
        }
    )
    code = serializers.CharField(
        required=True,
        min_length=6,
        max_length=6,
        error_messages={
            'required':   'OTP code is required.',
            'min_length': 'OTP must be 6 digits.',
            'max_length': 'OTP must be 6 digits.',
        }
    )

    def validate_code(self, value):
        """Ensure code contains only digits."""
        if not value.isdigit():
            raise serializers.ValidationError('OTP must contain only digits.')
        return value
