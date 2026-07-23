"""
Aurus AI — Root URL Configuration
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('otp_service.urls')),  # All OTP endpoints under /api/
]
