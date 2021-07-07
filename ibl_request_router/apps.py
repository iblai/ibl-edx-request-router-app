from django.apps import AppConfig
from openedx.core.djangoapps.plugins.constants import SettingsType

try:
    from edx_django_utils.plugins.constants import PluginURLs, PluginSettings
    from openedx.core.djangoapps.plugins.constants import ProjectType
except ImportError:
    from openedx.core.djangoapps.plugins.constants import  (
        ProjectType, PluginURLs, PluginSettings
    )


class RequestRouterConfig(AppConfig):
    name = 'ibl_request_router'
    verbose_name = "IBL Request Router"

    plugin_app = {
        PluginURLs.CONFIG: {
            ProjectType.LMS: {
                PluginURLs.NAMESPACE: 'ibl_request_router',
                PluginURLs.APP_NAME: 'ibl_request_router',
                PluginURLs.REGEX: r'',
                PluginURLs.RELATIVE_PATH: 'urls'
            },
        },
        PluginSettings.CONFIG: {
            ProjectType.LMS: {
                SettingsType.COMMON: {
                    PluginSettings.RELATIVE_PATH: 'settings'
                }
            },
            ProjectType.CMS: {
                SettingsType.COMMON: {
                    PluginSettings.RELATIVE_PATH: 'settings'
                }
            }
        }

    }

