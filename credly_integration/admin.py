"""
Admin registration for credly integration.
"""

import os

from admin_extra_buttons.api import ExtraButtonsMixin, link
from django.conf import settings
from django.contrib import admin
from django.contrib.sites.models import Site
from django.urls import reverse

from .models import CredlyCourseData


@admin.register(CredlyCourseData)
class CredlyCourseDataAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    """
    Admin config for course credly course data.
    """
    list_display = ('course', 'badge_id',)
    search_fields = ('course',)

    @link(href=None, change_list=True)
    def credly_report(self, button):
        path = reverse("credly_integration:download_report")

        button.label = "Credly Report"
        button.href = os.path.join(settings.LMS_ROOT_URL, path)
