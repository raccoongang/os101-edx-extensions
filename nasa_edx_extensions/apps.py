"""
App configuration for nasa_edx_extensions.
"""

from __future__ import unicode_literals

from django.apps import AppConfig

from openedx.core.djangoapps.plugins.constants import (
    ProjectType, SettingsType, PluginURLs, PluginSettings
)


EXTENSIONS_APP_NAME = 'nasa_edx_extensions'


class NasaEdxExtensionsConfig(AppConfig):
    """
    Nasa EDX Extensions configuration.
    """
    name = EXTENSIONS_APP_NAME
    verbose_name = 'Nasa EDX Extensions'

    # Class attribute that configures and enables this app as a Plugin App.
    plugin_app = {
        PluginURLs.CONFIG: {
            ProjectType.LMS: {
                PluginURLs.NAMESPACE: EXTENSIONS_APP_NAME,
                PluginURLs.APP_NAME: EXTENSIONS_APP_NAME,
                PluginURLs.REGEX: r'^nasa_edx_extensions/',
                PluginURLs.RELATIVE_PATH: 'urls',
            },
            ProjectType.CMS: {
                PluginURLs.NAMESPACE: EXTENSIONS_APP_NAME,
                PluginURLs.APP_NAME: EXTENSIONS_APP_NAME,
                PluginURLs.REGEX: r'^nasa_edx_extensions/',
                PluginURLs.RELATIVE_PATH: 'urls',
            }
        },

        PluginSettings.CONFIG: {
            ProjectType.LMS: {
                SettingsType.COMMON: {
                    PluginSettings.RELATIVE_PATH: 'settings.common',
                },
                SettingsType.TEST: {
                    PluginSettings.RELATIVE_PATH: 'settings.test',
                },
                SettingsType.PRODUCTION: {
                    PluginSettings.RELATIVE_PATH: 'settings.production',
                },
            },
            ProjectType.CMS: {
                SettingsType.COMMON: {
                    PluginSettings.RELATIVE_PATH: 'settings.common',
                },
                SettingsType.TEST: {
                    PluginSettings.RELATIVE_PATH: 'settings.test',
                },
                SettingsType.PRODUCTION: {
                    PluginSettings.RELATIVE_PATH: 'settings.production',
                },
            },
        }
    }
