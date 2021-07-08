"""
App Configuration for ibl_request_router
"""


from django.apps import AppConfig


class RequestRouterConfig(AppConfig):
    """
    App Configuration for ibl_request_router
    """
    name = 'ibl_request_router'
    verbose_name = "IBL Request Router"

    plugin_app = {
        'settings_config': {
            'lms.djangoapp': {
                'common': {
                    'relative_path': 'settings.common',
                },
            },
        },
        'settings_config': {
            'cms.djangoapp': {
                'common': {
                    'relative_path': 'settings.common',
                },
            },
        }
    }