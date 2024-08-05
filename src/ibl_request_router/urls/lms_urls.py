# URLs
try:
    from django.urls import re_path as url
except ImportError:
    from django.conf.urls import url
from django.conf.urls import include

from ibl_request_router.views import (
    heartbeat, proxy, token
)
from ibl_request_router.config import (
    MANAGER_PROXY_ENABLED,
    MANAGER_TOKEN_PROXY_ENABLED,
    URL_PATTERNS_BEFORE_ROUTER,
)

urlpatterns = [
    url(
        r"^api/ibl/heartbeat/celery/?$",
        heartbeat.CeleryHeartbeatView.as_view(),
        name="heartbeat_celery_view"
    )
]

if MANAGER_TOKEN_PROXY_ENABLED:
    urlpatterns += [
        url(
            r"^api/ibl/manager/token/proxy/?$",
            token.manager_token_proxy_view,
            name="manager_token_proxy_view",
        ),
        url(
            r"^api/ibl/manager/consolidated-token/proxy/?$",
            token.manager_consolidated_token_proxy_view,
            name="manager_consolidated_token_proxy_view",
        ),
    ]

if MANAGER_PROXY_ENABLED:
    for pattern in URL_PATTERNS_BEFORE_ROUTER:
        if pattern.get("namespace"):
            urlpatterns += [
                url(
                    pattern["regex"],
                    include(pattern["url_path"], namespace=pattern.get("namespace")),
                ),
            ]
        else:
            urlpatterns += [
                url(pattern["regex"], include(pattern["url_path"])),
            ]

    urlpatterns += [
        url(
            r"^api/ibl/(?P<endpoint_path>[\w+-/@.~+:]+)$",
            proxy.manager_proxy_view,
            name="manager_proxy_view",
        )
    ]
