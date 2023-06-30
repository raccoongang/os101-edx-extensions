from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.decorators.cache import cache_control

from django.views.generic import View


from .utils import generate_credly_data_csv


class CredlyReportView(View):
    """
    View for Credly courses report generation.
    """
    http_method_names = ['get']

    @method_decorator(cache_control(no_cache=True, no_store=True, must_revalidate=True))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        GET request handler.

        Collect statistics and make report for Credly course users
        with certificates.

        :returns HttpResponse object.
        """
        content = generate_credly_data_csv()

        response = HttpResponse(content, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="credly_report.csv"'
        return response
