"""
App configuration for credly integration.
"""

from __future__ import unicode_literals

from django.apps import AppConfig

from openedx.core.djangoapps.plugins.constants import (
    ProjectType, SettingsType, PluginURLs, PluginSettings
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
        PluginURLs.CONFIG: {
            ProjectType.LMS: {
                PluginURLs.NAMESPACE: EXTENSIONS_APP_NAME,
                PluginURLs.APP_NAME: EXTENSIONS_APP_NAME,
                PluginURLs.REGEX: r'^credly-integration',
                PluginURLs.RELATIVE_PATH: 'urls',
            },
            ProjectType.CMS: {
                PluginURLs.NAMESPACE: EXTENSIONS_APP_NAME,
                PluginURLs.APP_NAME: EXTENSIONS_APP_NAME,
                PluginURLs.REGEX: r'^credly-integration',
                PluginURLs.RELATIVE_PATH: 'urls',
            }
        },
        PluginSettings.CONFIG: {
            ProjectType.CMS: {
                SettingsType.COMMON: {
                    PluginSettings.RELATIVE_PATH: 'settings.common',
                },
            },
            ProjectType.LMS: {
                SettingsType.COMMON: {
                    PluginSettings.RELATIVE_PATH: 'settings.common',
                },
            },
        }
    }
