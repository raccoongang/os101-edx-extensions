from django.conf import settings
from django.utils.translation import gettext as _

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
