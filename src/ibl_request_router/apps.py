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
        'url_config': {
            'lms.djangoapp': {
                'namespace': 'ibl_request_router',
                'regex': r'',
                'relative_path': 'urls.lms_urls',
            },
        },
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