"""Ubicquia extensions urls."""
from django.conf.urls import url
from .views import CredlyReportView


urlpatterns = [
    url(
        r'^/download_report/$',
        CredlyReportView.as_view(),
        name='download_report'
    ),
]
