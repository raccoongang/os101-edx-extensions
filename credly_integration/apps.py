"""
App configuration for credly integration.
"""

from __future__ import unicode_literals

from django.apps import AppConfig

from openedx.core.djangoapps.plugins.constants import (
    ProjectType, SettingsType, PluginSettings
)


EXTENSIONS_APP_NAME = 'credly_integration'


class CredlyIntegraionConfig(AppConfig):
    """
    Nasa Tops credly integration configuration.
    """
    name = EXTENSIONS_APP_NAME
    verbose_name = 'Credly Integration'

    # Class attribute that configures and enables this app as a Plugin App.
    plugin_app = {
        PluginSettings.CONFIG: {
            ProjectType.CMS: {
                SettingsType.COMMON: {
                    PluginSettings.RELATIVE_PATH: 'settings.common',
                },
                SettingsType.PRODUCTION: {
                    PluginSettings.RELATIVE_PATH: 'settings.common',
                },
            },
        }
    }
