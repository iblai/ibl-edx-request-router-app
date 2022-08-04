from unittest import mock
from urllib.parse import urljoin

import pytest
from django.shortcuts import reverse

from ibl_request_router.config import MANAGER_BASE_API_URL

from .utils import auth_info

HTTP_METHODS = ["get", "post", "put", "delete"]
URL_PREFIX = MANAGER_BASE_API_URL + "/ibl/"


@pytest.mark.django_db
class TestManagerProxyView:
    endpoint = "knock_knock/"
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
    def test_unprivileged_user_can_access_unauth_endpoints(
        self, http_method, client, requests_mock
    ):
        _, token_header, _ = auth_info()
        requests_mock.request(
            http_method, urljoin(URL_PREFIX, self.endpoint), json={"detail": "success"}
        )
        resp = client.generic(
            http_method,
            reverse(self.url_name, args=(self.endpoint,)),
            HTTP_AUTHORIZATION=token_header,
        )

        assert resp.status_code == 200
        assert resp.json()["detail"] == "success"
