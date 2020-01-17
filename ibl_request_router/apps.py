# App config

from django.apps import AppConfig

class RequestRouterConfig(AppConfig):
    name = 'dl_request_router'
    verbose_name = "DL Request Router"
    
    def ready(self):
        from . import signals
    
