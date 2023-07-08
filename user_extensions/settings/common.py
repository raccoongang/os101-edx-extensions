"""
Common Django settings for user_extensions app.
"""


# pylint: disable=unnecessary-pass,unused-argument
def plugin_settings(settings):
    """
    Set of plugin settings used by the Open Edx platform.

    More info: https://github.com/edx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    settings.OVERRIDE_DO_CREATE_ACCOUNT = 'user_extensions.overrides.do_create_account'
    if settings.FEATURES.get("ENABLE_NASA_EXTENDED_REG_FORM", True):
        settings.ENABLE_DYNAMIC_REGISTRATION_FIELDS = True
        settings.REGISTRATION_EXTENSION_FORM = 'user_extensions.forms.ExtendedUserProfileForm'
        settings.NASA_EXTENDED_PROFILE_FIELDS = [
            "orcid_id",
            "subscribe_to_emails",
            "science_community",
            "career_stage",
            "extended_gender",
            "race_ethnicity",
        ]
        settings.NASA_EXTENDED_PROFILE_EXTRA_FIELDS = {
            'orcid_id': 'required',
            'subscribe_to_emails': 'required',
            'science_community': 'required',
            'career_stage': 'required',
            'extended_gender': 'required',
            'race_ethnicity': 'required',
            "country": "optional",
        }
        settings.REGISTRATION_EXTRA_FIELDS.update(settings.NASA_EXTENDED_PROFILE_EXTRA_FIELDS)
        settings.REGISTRATION_FIELD_ORDER += settings.NASA_EXTENDED_PROFILE_FIELDS

        settings.OVERRIDE_NASA_PROFILE_FIELDS = "user_extensions.overrides.authn_field_can_be_saved"
        settings.FIX_REQUIRED_ERROR_MESSAGE = "user_extensions.overrides.modify_error_message_for_fields"
