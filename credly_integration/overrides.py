import logging
from typing import Dict

import django.utils
from common.djangoapps.edxmako.shortcuts import render_to_response
from common.djangoapps.util.json_request import JsonResponse, JsonResponseBadRequest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
from opaque_keys.edx.keys import CourseKey
from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers
from rest_framework.exceptions import ValidationError
from xmodule.course_module import CourseBlock
from xmodule.modulestore.django import modulestore
from xmodule.tabs import InvalidTabsException
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview

from .models import CredlyCourseData

log = logging.getLogger(__name__)
User = get_user_model()


def advanced_settings_handler(*args, **kwargs):
    """
    Overrides CMS advanced_settings_handler view to update logic
    for adding, getting and updating the Credly Badge Template ID field
    """
    from cms.djangoapps.contentstore.utils import get_proctored_exam_settings_url, reverse_course_url
    from cms.djangoapps.contentstore.views.course import get_course_and_check_access
    from cms.djangoapps.models.settings.course_metadata import CourseMetadata

    request = args[1]
    course_key_string = kwargs.get('course_key_string')
    course_key = CourseKey.from_string(course_key_string)
    with modulestore().bulk_operations(course_key):
        course_module = get_course_and_check_access(course_key, request.user)

        advanced_dict = CourseMetadata.fetch(course_module)
        if settings.FEATURES.get('DISABLE_MOBILE_COURSE_AVAILABLE', False):
            advanced_dict.get('mobile_available')['deprecated'] = True

        if 'text/html' in request.META.get('HTTP_ACCEPT', '') and request.method == 'GET':
            publisher_enabled = configuration_helpers.get_value_for_org(
                course_module.location.org,
                'ENABLE_PUBLISHER',
                settings.FEATURES.get('ENABLE_PUBLISHER', False)
            )
            # gather any errors in the currently stored proctoring settings.
            proctoring_errors = CourseMetadata.validate_proctoring_settings(course_module, advanced_dict, request.user)
            advanced_dict.update({'badge_id': {
                    'deprecated': False,
                    'display_name': 'Credly Badge Template ID',
                    'help': 'This value will be used for the report that can be uploaded into the Credly service',
                    'hide_on_enabled_publisher': False,
                    'value': ''
                }})
            if obj := CredlyCourseData.objects.filter(course=course_key).first():
                advanced_dict['badge_id']['value'] = obj.badge_id

            return render_to_response('settings_advanced.html', {
                'context_course': course_module,
                'advanced_dict': advanced_dict,
                'advanced_settings_url': reverse_course_url('advanced_settings_handler', course_key),
                'publisher_enabled': publisher_enabled,
                'mfe_proctored_exam_settings_url': get_proctored_exam_settings_url(course_module.id),
                'proctoring_errors': proctoring_errors,
            })
        elif 'application/json' in request.META.get('HTTP_ACCEPT', ''):
            if request.method == 'GET':
                return JsonResponse(CourseMetadata.fetch(course_module))
            else:
                try:
                    return JsonResponse(
                        update_course_advanced_settings(course_module, request.json, request.user)
                    )
                except ValidationError as err:
                    return JsonResponseBadRequest(err.detail)


def update_course_advanced_settings(course_module: CourseBlock, data: Dict, user: User) -> Dict:
    """
    Helper function to update course advanced settings from API data.

    This function takes JSON data returned from the API and applies changes from
    it to the course advanced settings.

    Args:
        course_module (CourseBlock): The course run object on which to operate.
        data (Dict): JSON data as found the ``request.data``
        user (User): The user performing the operation

    Returns:
        Dict: The updated data after applying changes based on supplied data.
    """
    from cms.djangoapps.contentstore.views.course import _refresh_course_tabs
    from cms.djangoapps.models.settings.course_metadata import CourseMetadata

    try:
        # validate data formats and update the course module.
        # Note: don't update mongo yet, but wait until after any tabs are changed
        is_valid, errors, updated_data = CourseMetadata.validate_and_update_from_json(
            course_module,
            data,
            user=user,
        )
        if not is_valid:
            raise ValidationError(errors)

        try:
            # update the course tabs if required by any setting changes
            _refresh_course_tabs(user, course_module)
        except InvalidTabsException as err:
            log.exception(str(err))
            response_message = [
                {
                    'message': _('An error occurred while trying to save your tabs'),
                    'model': {'display_name': _('Tabs Exception')}
                }
            ]
            raise ValidationError(response_message) from err

        CredlyCourseData.objects.update_or_create(
            course=CourseOverview.objects.get(id=course_module.id),
            defaults={'badge_id': data['badge_id']['value']}
        )

        # now update mongo
        modulestore().update_item(course_module, user.id)

        return updated_data

    # Handle all errors that validation doesn't catch
    except (TypeError, ValueError, InvalidTabsException) as err:
        raise ValidationError(django.utils.html.escape(str(err))) from err
