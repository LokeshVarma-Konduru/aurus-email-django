from django.contrib import admin
from .models import OTPRecord


@admin.register(OTPRecord)
class OTPRecordAdmin(admin.ModelAdmin):
    list_display  = ('email', 'code', 'status', 'created_at', 'expires_at', 'verified_at')
    list_filter   = ('status',)
    search_fields = ('email',)
    readonly_fields = ('code', 'created_at', 'expires_at', 'verified_at')
    ordering = ('-created_at',)
