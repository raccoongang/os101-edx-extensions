"""
Admin registration for nasa edx extensions.
"""

from django.contrib import admin

from .models import CertificateExtraData


@admin.register(CertificateExtraData)
class CertificateExtraDataAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'badge_name_override', 'course',
    ]
