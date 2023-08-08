from django.conf import settings
from django.contrib import messages
from django.utils.translation import gettext as _
from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers
from common.djangoapps import third_party_auth
from common.djangoapps.third_party_auth import pipeline

from .utils import split_full_name
from .models import ExtendedUserProfile


def do_create_account(base_fn, *args, **kwargs):
    """
    Override function do_create_account for adding in User object
    fields 'first_name', 'last_name' and 'middle_name'.

    Returns a tuple (User, UserProfile, Registration).
    """
    user, profile, registration = base_fn(*args, **kwargs)

    first_name, middle_name, last_name = split_full_name(profile.name)

    extended_profile, _ = ExtendedUserProfile.objects.get_or_create(user=user)
    extended_profile.middle_name = middle_name
    extended_profile.save()

    user.first_name = first_name
    user.last_name = last_name
    user.save()

    return user, profile, registration


def authn_field_can_be_saved(prev_fn, self, field):
    """
    Override _field_can_be_saved
    """
    return field in settings.NASA_EXTENDED_PROFILE_FIELDS or prev_fn(self, field)


def modify_error_message_for_fields(add_extension_form_field, field_name, custom_form, field_description, field_type):
    """
    Returns Extension form field values
    """
    field_context = add_extension_form_field(field_name, custom_form, field_description, field_type)
    field_context.update(
        {
            'error_message': field_description.error_messages.get(
                'required', _(f'Enter your {field_description.label.lower()}')
            ) if field_type == 'required' and field_description.label else ''
        }
    )
    return field_context


def third_party_auth_context(*args, **kwargs):
    """
    Override third_party_auth_context.
    """
    request, redirect_to, tpa_hint = (args[1], args[2], args[3])
    context = {
        "currentProvider": None,
        "platformName": configuration_helpers.get_value('PLATFORM_NAME', settings.PLATFORM_NAME),
        "providers": [],
        "secondaryProviders": [],
        "finishAuthUrl": None,
        "errorMessage": None,
        "registerFormSubmitButtonText": _("Create Account"),
        "syncLearnerProfileData": False,
        "pipeline_user_details": {}
    }

    if third_party_auth.is_enabled():
        for enabled in third_party_auth.provider.Registry.displayed_for_login(tpa_hint=tpa_hint):
            info = {
                "id": enabled.provider_id,
                "name": enabled.name,
                "iconClass": enabled.icon_class or None,
                "iconImage": enabled.icon_image.url if enabled.icon_image else None,
                "skipHintedLogin": enabled.skip_hinted_login_dialog,
                "loginUrl": pipeline.get_login_url(
                    enabled.provider_id,
                    pipeline.AUTH_ENTRY_LOGIN,
                    redirect_url=redirect_to,
                ),
                "registerUrl": pipeline.get_login_url(
                    enabled.provider_id,
                    pipeline.AUTH_ENTRY_REGISTER,
                    redirect_url=redirect_to,
                ),
            }
            context["providers" if not enabled.secondary else "secondaryProviders"].append(info)

        running_pipeline = pipeline.get(request)
        if running_pipeline is not None:
            current_provider = third_party_auth.provider.Registry.get_from_pipeline(running_pipeline)
            user_details = running_pipeline['kwargs']['details']
            if user_details:
                context['pipeline_user_details'] = user_details

            if current_provider is not None:
                context["currentProvider"] = current_provider.name
                context["finishAuthUrl"] = pipeline.get_complete_url(current_provider.backend_name)
                context["syncLearnerProfileData"] = current_provider.sync_learner_profile_data

                if current_provider.skip_registration_form:
                    # As a reliable way of "skipping" the registration form, we just submit it automatically
                    context["autoSubmitRegForm"] = True

        # Check for any error messages we may want to display:
        for msg in messages.get_messages(request):
            if msg.extra_tags.split()[0] == "social-auth":
                # msg may or may not be translated. Try translating [again] in case we are able to:
                context["errorMessage"] = _(str(msg))  # pylint: disable=E7610
                break

    return context
