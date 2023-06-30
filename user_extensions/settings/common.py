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
