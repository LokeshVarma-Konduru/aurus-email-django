"""
OTP Service URL Routes

Mounted under /api/ in the root urls.py, so full paths are:
  POST  /api/otp/send/
  POST  /api/otp/verify/
  GET   /api/otp/health/
"""
from django.urls import path
from .views import SendOTPView, VerifyOTPView, HealthCheckView

app_name = 'otp_service'

urlpatterns = [
    path('otp/send/',   SendOTPView.as_view(),   name='send-otp'),
    path('otp/verify/', VerifyOTPView.as_view(),  name='verify-otp'),
    path('otp/health/', HealthCheckView.as_view(), name='health-check'),
]
