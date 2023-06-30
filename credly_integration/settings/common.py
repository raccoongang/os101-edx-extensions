"""
Common Django settings for credly_integration app.
"""


# pylint: disable=unnecessary-pass,unused-argument
def plugin_settings(settings):
    """
    Set of plugin settings used by the Open Edx platform.

    More info: https://github.com/edx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    settings.OVERRIDE_ADVANCED_SETTINGS_HANDLER = 'credly_integration.overrides.advanced_settings_handler'
