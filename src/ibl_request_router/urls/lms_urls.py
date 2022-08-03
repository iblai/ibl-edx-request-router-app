# URLs
from django.conf.urls import url, include

from ibl_request_router import views
from ibl_request_router.config import (
    MANAGER_PROXY_ENABLED,
    URL_PATTERNS_BEFORE_ROUTER
)


urlpatterns = []

if MANAGER_PROXY_ENABLED:
    for pattern in URL_PATTERNS_BEFORE_ROUTER:
        if pattern.get('namespace'):
            urlpatterns += [
                url(
                    pattern['regex'],
                    include(
                        pattern['url_path'],
                        namespace=pattern.get('namespace')
                    )
                ),
            ]
        else:
            urlpatterns += [
                url(pattern['regex'], include(pattern['url_path'])),
            ]

    urlpatterns += [
        url(
            r'^api/ibl/(?P<endpoint_path>[\w+-/@.~+:]+)$',
            views.manager_proxy_view,
            name="manager_proxy_view"
        )
    ]
