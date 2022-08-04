from unittest import mock
from requests_mock import ANY as requests_mock_ANY

import pytest
from django.shortcuts import reverse


from .utils import auth_info

MANAGER_BASE_URL = 'https://sleipnir.asgard.local'
MANAGER_BASE_API_URL = MANAGER_BASE_URL + '/api'
HTTP_METHODS = ["get", "post", "put", "delete"]


@pytest.mark.django_db
class TestManagerProxyView:
    endpoint = "knock_knock"
    url_name = "ibl_request_router:manager_proxy_view"

    @pytest.mark.parametrize("http_method", HTTP_METHODS)
    def test_no_endpoint_returns_404(self, http_method, client):
        _, token_header, _ = auth_info()

        resp = client.generic(
            http_method,
            reverse(self.url_name, args=(None,)),
            HTTP_AUTHORIZATION=token_header,
        )

        assert resp.status_code == 404

    @pytest.mark.parametrize("http_method", HTTP_METHODS)
    @mock.patch(
        "ibl_request_router.utils.access.MANAGER_API_UNAUTH_ALLOWLIST",
        ("knock_knock",),
    )
    @mock.patch(
        "ibl_request_router.api.manager.MANAGER_BASE_URL",
        MANAGER_BASE_URL,
    )
    @mock.patch(
        "ibl_request_router.api.manager.MANAGER_BASE_API_URL",
        MANAGER_BASE_API_URL,
    )
    @mock.patch(
        "ibl_request_router.api.manager.MANAGER_AUTH_ENABLED",
        False,
    )
    def test_unprivileged_user_can_access_unauth_endpoints(
        self, http_method, client, requests_mock
    ):
        _, token_header, _ = auth_info()
        requests_mock.request(
            http_method, requests_mock_ANY, json={"detail": "success"}
        )
        resp = client.generic(
            http_method,
            reverse(self.url_name, args=(self.endpoint,)),
            HTTP_AUTHORIZATION=token_header,
        )

        assert resp.status_code == 200
        assert resp.json()["detail"] == "success"
