"""
Common Django settings for credly_integration app.
"""


# pylint: disable=unnecessary-pass,unused-argument
def plugin_settings(settings):
    """
    Set of plugin settings used by the Open Edx platform.

    More info: https://github.com/edx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    settings.INSTALLED_APPS += ["admin_extra_buttons",]
