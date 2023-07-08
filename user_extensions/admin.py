"""
Admin registration for user extensions.
"""

from django.contrib import admin
from .models import ExtendedUserProfile

@admin.register(ExtendedUserProfile)
class ExtendedUserProfileAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'middle_name', 'orcid_id', 'subscribe_to_emails', 'science_community', 'career_stage', 'extended_gender', 'race_ethnicity'
    ]
    search_fields = ('user__username',)
