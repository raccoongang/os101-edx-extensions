from django.conf import settings
from lms.djangoapps.courseware.courses import get_courses, sort_by_announcement, sort_by_start_date
from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers


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
