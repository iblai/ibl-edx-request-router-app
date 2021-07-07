from django.apps import AppConfig

try:
    from edx_django_utils.plugins.constants import PluginURLs
    from openedx.core.djangoapps.plugins.constants import ProjectType
except ImportError:
    from openedx.core.djangoapps.plugins.constants import  (
        ProjectType, PluginURLs
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
        }
    }

