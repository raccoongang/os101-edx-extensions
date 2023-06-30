"""
Admin registration for user extensions.
"""


from django.contrib import admin

from .models import ExtendedUserProfile


@admin.register(ExtendedUserProfile)
class ExtendedUserProfileAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'middle_name',
    ]
    search_fields = ('user__username',)
