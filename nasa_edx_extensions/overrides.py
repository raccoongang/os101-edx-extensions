from django.conf import settings
from rest_framework.response import Response

from lms.djangoapps.badges.models import BadgeAssertion
from lms.djangoapps.courseware.courses import get_courses, sort_by_announcement, sort_by_start_date
from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers

from edx_badges.models import BadgeStatus
from edx_badges.credly.serializers import BadgeDataModel

from .models import CertificateExtraData


def override_index_django_view(base_fn, *args, **kwargs):
    """
    Overrides django view for `index` page to show only courses with `both` catalog visibility.
    """
    user = kwargs.get("user")

    courses = get_courses(user, filter_={"catalog_visibility": "both"})

    if configuration_helpers.get_value(
        "ENABLE_COURSE_SORTING_BY_START_DATE",
        settings.FEATURES["ENABLE_COURSE_SORTING_BY_START_DATE"],
    ):
        courses = sort_by_start_date(courses)
    else:
        courses = sort_by_announcement(courses)

    return base_fn(*args, **kwargs, extra_context={"courses": courses})


def override_get_certificates(base_fn, self, request, username):  # pylint: disable=unused-argument
    user_certs = []
    if self._viewable_by_requestor(request, username):  # pylint: disable=protected-access
        for badge_assertion in BadgeAssertion.objects.filter(badge_status__state=BadgeStatus.ACCEPTED):
            badge = BadgeDataModel(data=badge_assertion.data)
            badge.is_valid(raise_exception=True)

            user_certs.append({
                'username': username,
                'course_id': None,
                'course_display_name': badge.data.get("badge_template").get("name"),
                'course_organization': None,
                'certificate_type': None,
                'created_date': badge_assertion.created,
                'modified_date': badge_assertion.created,
                'status': None,
                'is_passing': True,
                'download_url': badge_assertion.assertion_url,
                'grade': None,
                'preview_image': badge_assertion.image_url,
            })
        for user_cert in self._get_certificates_for_user(username):  # pylint: disable=protected-access
            certificate_extra = CertificateExtraData.objects.filter(course__id=user_cert.get('course_key')).first()
            course_display_name = (
                certificate_extra.badge_name_override
                if certificate_extra and certificate_extra.badge_name_override
                else user_cert.get('course_display_name')
            )
            user_certs.append({
                'username': user_cert.get('username'),
                'course_id': str(user_cert.get('course_key')),
                'course_display_name': course_display_name,
                'course_organization': user_cert.get('course_organization'),
                'certificate_type': user_cert.get('type'),
                'created_date': user_cert.get('created'),
                'modified_date': user_cert.get('modified'),
                'status': user_cert.get('status'),
                'is_passing': user_cert.get('is_passing'),
                'download_url': user_cert.get('download_url'),
                'grade': user_cert.get('grade'),
                'preview_image': getattr(certificate_extra, 'full_image_url', None),
            })
    return Response(user_certs)
