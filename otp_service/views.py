"""
Aurus AI — OTP API Views
POST /api/otp/send/   → generate & email OTP
POST /api/otp/verify/ → validate submitted OTP
GET  /api/otp/health/ → server health check
"""
import logging
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .email_service import send_otp_email
from .models import OTPRecord
from .serializers import SendOTPSerializer, VerifyOTPSerializer

logger = logging.getLogger(__name__)


class SendOTPView(APIView):
    """
    POST /api/otp/send/

    Body:  { "email": "user@example.com" }

    Response (200):
        {
          "success": true,
          "message": "OTP sent to user@example.com",
          "expires_in": 10
        }

    Response (400): validation error
    Response (500): email delivery failure
    """

    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {'success': False, 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        email = serializer.validated_data['email']

        # ── Invalidate any existing pending OTPs for this email ──────────────
        OTPRecord.objects.filter(
            email=email,
            status=OTPRecord.STATUS_PENDING
        ).update(status=OTPRecord.STATUS_EXPIRED)

        # ── Create new OTP record ─────────────────────────────────────────────
        otp_record = OTPRecord.objects.create(email=email)
        logger.info("OTP generated for %s: %s", email, otp_record.code)

        # ── Send email with embedded logo ─────────────────────────────────────
        result = send_otp_email(email, otp_record.code)

        if not result['success']:
            # Delete the record so user can retry cleanly
            otp_record.delete()
            return Response(
                {'success': False, 'message': result['message']},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {
                'success':    True,
                'message':    f'OTP sent to {email}',
                'expires_in': 10,   # minutes
            },
            status=status.HTTP_200_OK
        )


class VerifyOTPView(APIView):
    """
    POST /api/otp/verify/

    Body:  { "email": "user@example.com", "code": "993773" }

    Response (200):
        { "success": true, "message": "OTP verified successfully." }

    Response (400):
        { "success": false, "message": "Invalid OTP. Please try again." }
    """

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {'success': False, 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        email = serializer.validated_data['email']
        code  = serializer.validated_data['code']

        # ── Find most recent pending OTP for this email ───────────────────────
        otp_record = (
            OTPRecord.objects
            .filter(email=email, status=OTPRecord.STATUS_PENDING)
            .order_by('-created_at')
            .first()
        )

        if not otp_record:
            return Response(
                {
                    'success': False,
                    'message': 'No active OTP found for this email. Please request a new one.',
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # ── Delegate verification to the model ────────────────────────────────
        success, message = otp_record.verify(code)

        http_status = status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST
        return Response({'success': success, 'message': message}, status=http_status)


class HealthCheckView(APIView):
    """
    GET /api/otp/health/
    Simple liveness probe — useful for testing the server is running.
    """

    def get(self, request):
        return Response(
            {
                'status':    'ok',
                'service':   'Aurus AI OTP Service',
                'timestamp': timezone.now().isoformat(),
            },
            status=status.HTTP_200_OK
        )
