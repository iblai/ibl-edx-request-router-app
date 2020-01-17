# URLs
from django.conf import settings
from django.conf.urls import url

from ibl_request_router import views


MANAGER_PROXY_ENABLED = getattr(settings, "MANAGER_PROXY_ENABLED", True)


urlpatterns = []

if MANAGER_PROXY_ENABLED:
    urlpatterns += [
        url(
            r'^api/ibl/(?P<endpoint_path>[\w+-/@.~]+)$',
            views.manager_proxy_view,
            name="manager_proxy_view"
        )
    ]
