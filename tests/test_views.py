from unittest import mock

import pytest
from django.shortcuts import reverse

from .utils import auth_info

http_methods = ["get", "post", "put", "delete"]


@pytest.mark.django_db
class TestManagerProxyView:
    endpoint = "/knock_knock/"
    url_name = "ibl_request_router:manager_proxy_view"

    @pytest.mark.parametrize("http_method", http_methods)
    def test_no_endpoint_returns_404(self, http_method, client):
        _, token_header, _ = auth_info()

        resp = client.generic(
            http_method,
            reverse(self.url_name, args=(None,)),
            HTTP_AUTHORIZATION=token_header,
        )

        assert resp.status_code == 404

    @pytest.mark.parametrize("http_method", http_methods)
    @mock.patch(
        "ibl_request_router.utils.access.MANAGER_API_UNAUTH_ALLOWLIST", ("/knock_knock/", )
    )
    def test_unprivileged_user_can_access_unauth_endpoints(
        self, http_method, client, requests_mock
    ):
        _, token_header, _ = auth_info()
        requests_mock.request(http_method, self.endpoint, json={"detail": "success"})
        resp = client.generic(
            http_method,
            reverse(self.url_name, args=(self.endpoint,)),
            HTTP_AUTHORIZATION=token_header,
        )

        assert resp.status_code == 200
        assert resp.json()["detail"] == "success"
