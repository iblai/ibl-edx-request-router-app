# App config

from django.apps import AppConfig

class RequestRouterConfig(AppConfig):
    name = 'ibl_request_router'
    verbose_name = "IBL Request Router"
    
    def ready(self):
        from . import signals
    
